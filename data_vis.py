import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

original_data = {
    "Language": ["English", "French", "German", "Hebrew", "Russian"],
    # 'Simple Agreement': [1.00, 1.00, 0.95, 0.70, 0.65],
    # 'VP Coordination (Short)': [1.00, 1.00, 0.97, 0.91, 0.80]
    "Across subject relative clause": [0.88, 0.57, 0.73, 0.61, 0.70],
    "Across prepositional phrase": [0.92, 0.57, 0.95, 0.62, 0.56],
}

replication_data = {
    "Language": ["English", "French", "German", "Hebrew", "Russian"],
    # 'Simple Agreement': [0.78, 0.76, 0.84, 0.72, 0.78],
    # 'VP Coordination (Short)': [0.82, 0.78, 0.90, 0.76, 0.79]
    "Across subject relative clause": [0.55, 0.56, 0.61, 0.64, 0.75],
    "Across prepositional phrase": [0.57, 0.53, 0.75, 0.55, 0.68],
}


original_df = pd.DataFrame(original_data)
replication_df = pd.DataFrame(replication_data)

bar_width = 0.35
index = np.arange(len(original_df["Language"]))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


ax1.bar(
    index,
    original_df["Across subject relative clause"],
    bar_width,
    label="Original",
    color="blue",
    alpha=0.7,
)
ax1.bar(
    index + bar_width,
    replication_df["Across subject relative clause"],
    bar_width,
    label="Replication",
    color="orange",
    alpha=0.7,
)
ax1.set_xlabel("Language")
ax1.set_ylabel("Accuracy")
ax1.set_title("Across subject relative clause: Original vs Replication")
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels(original_df["Language"])
ax1.legend()


ax2.bar(
    index,
    original_df["Across prepositional phrase"],
    bar_width,
    label="Original",
    color="blue",
    alpha=0.7,
)
ax2.bar(
    index + bar_width,
    replication_df["Across prepositional phrase"],
    bar_width,
    label="Replication",
    color="orange",
    alpha=0.7,
)
ax2.set_xlabel("Language")
ax2.set_ylabel("Accuracy")
ax2.set_title("Across prepositional phrase: Original vs Replication")
ax2.set_xticks(index + bar_width / 2)
ax2.set_xticklabels(original_df["Language"])
ax2.legend()


plt.tight_layout()
plt.show()
