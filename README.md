# dutch_protest_mapper
A data science project visualizing open-source data from ACLED relating to protests in the Netherlands 2020–2024.

# Data Acquisition
This project uses data from the Armed Conflict Location & Event Data Project (ACLED).

To reproduce:
1. Register for an ACLED account at https://acleddata.com
2. Use the export tool to filter:
   - Country: Netherlands
   - Event type: Protest + Violent demonstration
   - Date range: 01 Jan 2020 – 11 Aug 2024
3. Download as CSV and save to `data/raw/protests_nl_2020_2024.csv`

# Installation
Clone this repo and install dependencies:
```bash
git clone https://github.com/joeward2000/dutch_protest_mapper.git
cd dutch_protest_mapper
pip install -r requirements.txt
```

Key dependencies:
- `pandas`, `numpy` – data wrangling
- `sentence-transformers` – text embeddings
- `umap-learn`, `hdbscan` – clustering
- `streamlit`, `pydeck` – interactive app

# Data Cleaning
Raw data is cleaned in `src/data_clean.py` by:
1. Standardising column names.
2. Keeping only relevant columns (year, event type, province, coordinates, notes).
3. Filtering to events with exact date (`time_precision = 1`) and location (`geo_precision = 1`).
4. Relabelling “Excessive force against protesters” as “Protest with intervention” (single case).
5. Dropping precision columns.
6. Renaming `admin1` → `province` and `sub_event_type` → `event_type`.
7. Saving the cleaned dataset to `data/processed/protests_nl_cleaned.csv`.

# Theme Mapping
`src/theme_mapping.py` adds thematic clustering to protests based on event notes:
1. Text descriptions are embedded using `sentence-transformers` (`all-mpnet-base-v2`).
2. Embeddings are reduced in dimensionality with UMAP.
3. HDBSCAN clusters protests into themes.
4. Clusters are mapped to labels (e.g. Farmers Protest, Climate Protest, Asylum Policy Protest).
5. Final dataset with theme assignments is saved to `data/processed/protests_nl_cleaned_v2.csv`.

# Streamlit App
`src/app.py` provides an interactive map:
- Loads protest data with thematic clusters.
- Sidebar filters by year, event type, province, and theme.
- Displays summary metrics and a protest heatmap using Pydeck.
- Run locally with:
  ```bash
  streamlit run src/app.py
  ```
- Example screenshots of the interactive app:

**All Protests**
![All protests](streamlit_app/screenshots/all_protests.png)

**Corona Protests in Noord Brabant**
![Corona Protests in Noord Brabant](streamlit_app/screenshots/corona_protests_noord_brabant.png)
