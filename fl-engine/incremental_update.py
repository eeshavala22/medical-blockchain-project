import json
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler

from model import DiabetesModel

torch.manual_seed(42)

# ---------------------------------------------------------
# Load the scaler the same way as before (fit on original hospital A)
# ---------------------------------------------------------
scaler = StandardScaler()
raw_a = pd.read_csv("hospital_A.csv").iloc[:, :-1].values
scaler.fit(raw_a)

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    X = df.iloc[:, :-1].values.astype(np.float32)
    y = df.iloc[:, -1].values.astype(np.float32).reshape(-1, 1)
    X = scaler.transform(X)
    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)
    dataset = TensorDataset(X_tensor, y_tensor)
    return DataLoader(dataset, batch_size=8, shuffle=True)

def evaluate(model, data_loader):
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for X, y in data_loader:
            preds = model(X)
            correct += ((preds > 0.5).float() == y).sum().item()
            total += y.size(0)
    return correct / total

# ---------------------------------------------------------
# Load the previously trained global model
# ---------------------------------------------------------
model = DiabetesModel()
model.load_state_dict(torch.load("global_model.pt"))

old_data_loader = load_data("hospital_A.csv")
new_data_loader = load_data("hospital_A_new.csv")

print("=" * 60)
print("BEFORE INCREMENTAL UPDATE")
print("=" * 60)
acc_old_before = evaluate(model, old_data_loader)
acc_new_before = evaluate(model, new_data_loader)
print(f"Accuracy on OLD patients : {acc_old_before:.3f}")
print(f"Accuracy on NEW patients: {acc_new_before:.3f}  <- model hasn't seen these patterns yet")

# ---------------------------------------------------------
# Incremental update with EWC-style regularization
# (penalizes drifting too far from old weights, to avoid forgetting)
# ---------------------------------------------------------
old_params = [p.clone().detach() for p in model.parameters()]

optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = nn.BCELoss()
EWC_LAMBDA = 3.0
EPOCHS = 15

model.train()
for epoch in range(EPOCHS):
    for X, y in new_data_loader:
        optimizer.zero_grad()
        preds = model(X)
        loss = loss_fn(preds, y)

        # Elastic Weight Consolidation penalty: keeps new weights close to old ones
        ewc_penalty = sum(
            ((p - op) ** 2).sum() for p, op in zip(model.parameters(), old_params)
        )
        loss = loss + EWC_LAMBDA * ewc_penalty

        loss.backward()
        optimizer.step()

print("\n" + "=" * 60)
print("AFTER INCREMENTAL UPDATE")
print("=" * 60)
acc_old_after = evaluate(model, old_data_loader)
acc_new_after = evaluate(model, new_data_loader)
print(f"Accuracy on OLD patients : {acc_old_after:.3f}  (was {acc_old_before:.3f}) -> retained old knowledge")
print(f"Accuracy on NEW patients: {acc_new_after:.3f}  (was {acc_new_before:.3f}) -> learned new pattern")

torch.save(model.state_dict(), "global_model.pt")
print("\nUpdated global model saved (incrementally, without full retraining).")

incremental_results = {
    "old_before": acc_old_before,
    "old_after": acc_old_after,
    "new_before": acc_new_before,
    "new_after": acc_new_after,
}
with open("incremental_history.json", "w") as f:
    json.dump(incremental_results, f, indent=2)
print("Saved incremental update results to incremental_history.json")