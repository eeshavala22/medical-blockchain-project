import numpy as np
import pandas as pd
from generate_data import generate_hospital_data

# Simulate 40 new patients arriving at Hospital A a month later,
# with a slightly different pattern (e.g. a regional health trend)
np.random.seed(99)
new_patients = generate_hospital_data(40, risk_shift=0.8)
new_patients.to_csv("hospital_A_new.csv", index=False)

print("Generated hospital_A_new.csv:", new_patients.shape)
print(new_patients["Outcome"].value_counts())