import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
import hdbscan

# --- Step 1: Load your CSV ---
df = pd.read_csv('./data/processed/protests_nl_cleaned.csv')
texts = df['notes'].astype(str).tolist()  # Ensure all entries are strings

# --- Step 2: Encode text into embeddings ---
model = SentenceTransformer('all-mpnet-base-v2')
embeddings = model.encode(texts, show_progress_bar=True)

# --- Step 3: Reduce dimensionality with UMAP ---
reducer = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine', random_state=42)
embeddings_umap = reducer.fit_transform(embeddings)

# --- Step 4: Cluster embeddings with HDBSCAN ---
clusterer = hdbscan.HDBSCAN(min_cluster_size=100, metric='euclidean')
cluster_labels = clusterer.fit_predict(embeddings_umap)

# --- Step 5: Add cluster labels to dataframe ---
df['cluster'] = cluster_labels

# --- Step 6: Map clusters to thematic labels ---
cluster_name_map = {
    -1: "Theme Unidentified by Model",
     0: "Farmers Protest",
     1: "Workers Protest",
     2: "Relating to the Israeli/Palestinian Conflict",
     3: "Asylum Policy Protest",
     4: "Climate Protest",
     5: "Coronavirus Protest"
}
df['cluster_theme'] = df['cluster'].map(cluster_name_map).fillna("Unknown Theme")

# --- Step 7: Save clustered data to CSV ---
output_path = './data/processed/protests_nl_cleaned_v2.csv'
df.sort_values('cluster').to_csv(output_path, index=False)

print(f"Clustering complete. Results saved to '{output_path}'.")