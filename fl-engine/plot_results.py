import json
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Chart 1: Federated Learning accuracy over rounds
# ---------------------------------------------------------
with open("fl_history.json") as f:
    fl_hist = json.load(f)

plt.figure(figsize=(8, 5))
plt.plot(fl_hist["rounds"], fl_hist["hospital_A"], marker="o", label="Hospital A")
plt.plot(fl_hist["rounds"], fl_hist["hospital_B"], marker="o", label="Hospital B")
plt.plot(fl_hist["rounds"], fl_hist["hospital_C"], marker="o", label="Hospital C")
plt.plot(fl_hist["rounds"], fl_hist["global_avg"], marker="s", linewidth=2.5,
          color="black", label="Global Model (avg)")
plt.xlabel("Federated Learning Round")
plt.ylabel("Accuracy")
plt.title("Federated Learning: Accuracy per Round (with Differential Privacy)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("chart_fl_accuracy.png", dpi=150)
print("Saved chart_fl_accuracy.png")

# ---------------------------------------------------------
# Chart 2: Incremental Optimization before/after comparison
# ---------------------------------------------------------
with open("incremental_history.json") as f:
    inc_hist = json.load(f)

labels = ["Old Patients", "New Patients"]
before = [inc_hist["old_before"], inc_hist["new_before"]]
after = [inc_hist["old_after"], inc_hist["new_after"]]

x = range(len(labels))
width = 0.35

plt.figure(figsize=(7, 5))
plt.bar([i - width/2 for i in x], before, width, label="Before Update", color="#f4a259")
plt.bar([i + width/2 for i in x], after, width, label="After Update", color="#5b8c5a")
plt.xticks(list(x), labels)
plt.ylabel("Accuracy")
plt.title("Incremental Optimization: Before vs After Update")
plt.ylim(0, 1)
plt.legend()
plt.grid(True, axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("chart_incremental_update.png", dpi=150)
print("Saved chart_incremental_update.png")