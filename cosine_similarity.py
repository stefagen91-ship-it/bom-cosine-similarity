import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/sample_bom.csv")

# Keep product names and select features (all columns except 'Product')
product_names = df["Product"].values
X = df.drop(columns=["Product"])

# Scale features (cosine is scale-invariant re: vector length, but scaling helps when ranges differ)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Cosine similarity
sim_matrix = cosine_similarity(X_scaled)
sim_df = pd.DataFrame(sim_matrix, index=product_names, columns=product_names)

# Show matrix
print("Cosine Similarity Matrix (rounded):")
print(sim_df.round(2))

# Save similarity matrix to CSV
sim_df.round(4).to_csv("cosine_similarity_matrix.csv", index=True)

# Heatmap (matplotlib only)
plt.figure(figsize=(6, 5))
plt.imshow(sim_df, interpolation="nearest")
plt.title("Product Similarity (Cosine)")
plt.xticks(ticks=np.arange(len(product_names)), labels=product_names, rotation=45, ha="right")
plt.yticks(ticks=np.arange(len(product_names)), labels=product_names)
plt.colorbar(label="Similarity")
plt.tight_layout()
plt.savefig("cosine_similarity_heatmap.png", dpi=200)

print("Saved: cosine_similarity_matrix.csv, cosine_similarity_heatmap.png")

# Simple recommendation function: top-N similar items
def recommend(product, sim_df, top_n=3):
    if product not in sim_df.columns:
        raise ValueError(f"Product '{product}' not found. Available: {list(sim_df.columns)}")
    scores = sim_df[product].sort_values(ascending=False)
    return scores.iloc[1: top_n+1]  # exclude self

print("Top-2 similar to 'Bag_A':")
print(recommend("Bag_A", sim_df, top_n=2))
