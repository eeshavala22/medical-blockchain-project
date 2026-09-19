import numpy as np
import pandas as pd

np.random.seed(42)

def generate_hospital_data(n_samples, risk_shift=0.0):
    """
    Generates synthetic patient data resembling the Pima Diabetes dataset structure:
    Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigree, Age -> Outcome
    risk_shift lets each hospital have a slightly different patient population.
    """
    pregnancies = np.random.randint(0, 15, n_samples)
    glucose = np.random.normal(120 + risk_shift * 10, 30, n_samples).clip(50, 200)
    blood_pressure = np.random.normal(70, 12, n_samples).clip(40, 120)
    skin_thickness = np.random.normal(20, 10, n_samples).clip(0, 60)
    insulin = np.random.normal(80, 60, n_samples).clip(0, 400)
    bmi = np.random.normal(32 + risk_shift * 2, 7, n_samples).clip(15, 60)
    pedigree = np.random.normal(0.47, 0.3, n_samples).clip(0.05, 2.5)
    age = np.random.randint(21, 80, n_samples)

    # Create a realistic-ish risk score to derive the outcome label
    risk_score = (
        0.02 * glucose +
        0.015 * bmi +
        0.01 * age +
        0.3 * pedigree +
        0.05 * pregnancies -
        4.5 + risk_shift
    )
    prob = 1 / (1 + np.exp(-risk_score))
    outcome = (prob > 0.5).astype(int)

    df = pd.DataFrame({
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigree": pedigree,
        "Age": age,
        "Outcome": outcome,
    })
    return df

# 3 hospitals with slightly different patient populations (non-IID, like real FL scenarios)
hospital_a = generate_hospital_data(300, risk_shift=0.0)
hospital_b = generate_hospital_data(250, risk_shift=0.5)
hospital_c = generate_hospital_data(350, risk_shift=-0.3)

hospital_a.to_csv("hospital_A.csv", index=False)
hospital_b.to_csv("hospital_B.csv", index=False)
hospital_c.to_csv("hospital_C.csv", index=False)

print("Generated hospital_A.csv:", hospital_a.shape)
print("Generated hospital_B.csv:", hospital_b.shape)
print("Generated hospital_C.csv:", hospital_c.shape)
print("\nOutcome distribution (A):\n", hospital_a["Outcome"].value_counts())