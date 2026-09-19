import copy
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from opacus import PrivacyEngine

from model import DiabetesModel

torch.manual_seed(42)

# ---------------------------------------------------------
# STEP 1: Load and preprocess each hospital's data
# ---------------------------------------------------------
def load_hospital_data(csv_path, scaler=None, fit_scaler=False):
    df = pd.read_csv(csv_path)
    X = df.iloc[:, :-1].values.astype(np.float32)
    y = df.iloc[:, -1].values.astype(np.float32).reshape(-1, 1)

    if fit_scaler:
        scaler.fit(X)
    X = scaler.transform(X)

    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)
    dataset = TensorDataset(X_tensor, y_tensor)
    return DataLoader(dataset, batch_size=16, shuffle=True)

# Fit the scaler on hospital A first (in real life, each hospital would
# normalize locally, but we share a scaler here just for simplicity/demo)
scaler = StandardScaler()
raw_a = pd.read_csv("hospital_A.csv").iloc[:, :-1].values
scaler.fit(raw_a)

hospital_files = ["hospital_A.csv", "hospital_B.csv", "hospital_C.csv"]
hospital_loaders = [load_hospital_data(f, scaler=scaler) for f in hospital_files]

# ---------------------------------------------------------
# STEP 2: Local training function with Differential Privacy
# ---------------------------------------------------------
def train_local_model(global_state_dict, data_loader, epochs=3, noise_multiplier=1.0):
    """
    Trains a copy of the global model on one hospital's local data,
    with Differential Privacy noise added via Opacus.
    Returns the updated weights + the privacy budget (epsilon) spent.
    """
    model = DiabetesModel()
    model.load_state_dict(global_state_dict)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.BCELoss()

    privacy_engine = PrivacyEngine()
    model, optimizer, data_loader = privacy_engine.make_private(
        module=model,
        optimizer=optimizer,
        data_loader=data_loader,
        noise_multiplier=noise_multiplier,
        max_grad_norm=1.0,
    )

    model.train()
    for epoch in range(epochs):
        for X, y in data_loader:
            optimizer.zero_grad()
            preds = model(X)
            loss = loss_fn(preds, y)
            loss.backward()
            optimizer.step()

    epsilon = privacy_engine.get_epsilon(delta=1e-5)

    # Opacus wraps the model layers with "_module." prefixes internally;
    # strip that off so the state_dict matches the plain DiabetesModel shape
    clean_state_dict = {
        k.replace("_module.", ""): v for k, v in model.state_dict().items()
    }
    return clean_state_dict, epsilon

# ---------------------------------------------------------
# STEP 3: Federated averaging (FedAvg) — the core FL logic
# ---------------------------------------------------------
def average_weights(state_dicts):
    """Averages a list of model state_dicts into one, parameter by parameter."""
    avg_state = copy.deepcopy(state_dicts[0])
    for key in avg_state.keys():
        for i in range(1, len(state_dicts)):
            avg_state[key] += state_dicts[i][key]
        avg_state[key] = avg_state[key] / len(state_dicts)
    return avg_state

# ---------------------------------------------------------
# STEP 4: Evaluation helper
# ---------------------------------------------------------
def evaluate(state_dict, data_loader):
    model = DiabetesModel()
    model.load_state_dict(state_dict)
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for X, y in data_loader:
            preds = model(X)
            correct += ((preds > 0.5).float() == y).sum().item()
            total += y.size(0)
    return correct / total

# ---------------------------------------------------------
# STEP 5: Run the Federated Learning simulation across rounds
# ---------------------------------------------------------
global_model = DiabetesModel()
global_state = global_model.state_dict()

NUM_ROUNDS = 5
history = {"rounds": [], "hospital_A": [], "hospital_B": [], "hospital_C": [], "global_avg": [], "epsilons": []}

print("=" * 60)
print("STARTING FEDERATED LEARNING SIMULATION")
print("=" * 60)

for round_num in range(1, NUM_ROUNDS + 1):
    local_states = []
    epsilons = []

    for i, loader in enumerate(hospital_loaders):
        local_state, epsilon = train_local_model(global_state, loader, epochs=3)
        local_states.append(local_state)
        epsilons.append(epsilon)

    global_state = average_weights(local_states)

    # Evaluate the new global model on each hospital's own data
    accs = [evaluate(global_state, loader) for loader in hospital_loaders]
    avg_acc = sum(accs) / len(accs)

    print(f"\nRound {round_num}:")
    for i, (acc, eps) in enumerate(zip(accs, epsilons)):
        print(f"  Hospital {chr(65+i)} -> accuracy: {acc:.3f} | privacy budget (epsilon): {eps:.2f}")
    print(f"  Global model average accuracy: {avg_acc:.3f}")

    history["rounds"].append(round_num)
    history["hospital_A"].append(accs[0])
    history["hospital_B"].append(accs[1])
    history["hospital_C"].append(accs[2])
    history["global_avg"].append(avg_acc)
    history["epsilons"].append(epsilons)

print("\n" + "=" * 60)
print("FEDERATED TRAINING COMPLETE")
print("=" * 60)

torch.save(global_state, "global_model.pt")
print("\nSaved trained global model to global_model.pt")

with open("fl_history.json", "w") as f:
    json.dump(history, f, indent=2)
print("Saved training history to fl_history.json")