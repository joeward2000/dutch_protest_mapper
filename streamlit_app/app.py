import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import datetime, date
import os

# Page configuration
st.set_page_config(
    page_title="Netherlands Protests Map",
    page_icon="🗺️",
    layout="wide"
)

@st.cache_data
def load_protest_data():
    """Load and prepare protest data."""
    data_path = "./data/processed/protests_nl_cleaned_v2.csv"
    
    if not os.path.exists(data_path):
        st.error(f"Data file not found at {data_path}")
        st.stop()
    
    try:
        df = pd.read_csv(data_path)
        
        # Ensure required columns exist
        required_cols = ['longitude', 'latitude', 'year', 'event_type', 'province', 'cluster_theme']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
            st.stop()
        
        # Remove rows with missing coordinates or year
        df = df.dropna(subset=['longitude', 'latitude', 'year'])
        df['year'] = df['year'].astype(int)
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

def create_map(filtered_data):
    """Create pydeck heatmap visualization."""
    
    if len(filtered_data) == 0:
        st.warning("No protests found for the selected filters.")
        return None
    
    # Calculate center point for initial view
    center_lat = filtered_data['latitude'].mean()
    center_lon = filtered_data['longitude'].mean()
    
    # Create the heatmap layer
    layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_data,
        get_position=['longitude', 'latitude'],
        get_weight=1,
        radius_pixels=50,
    )
    
    # Set the viewport
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=7,
        bearing=0,
        pitch=0,
    )
    
    # Create the deck
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
    )
    
    return deck

def main():
    st.title("🗺️ Netherlands Protests Heatmap")
    st.markdown("Heatmap showing protest density across the Netherlands, 2020-2024 (Data source: ACLED)")
    
    # Load data
    with st.spinner("Loading protest data..."):
        df = load_protest_data()
    if df.empty:
        st.warning("No valid protest data found.")
        return
    
    # === Sidebar filters ===
    # 1. Year filter - collapsible
    with st.sidebar.expander("📅 Year Filter", expanded=True):
        available_years = sorted(df['year'].unique())
        selected_years = []
        for year in range(2020, 2025):
            if year in available_years:
                if st.checkbox(str(year), value=True, key=f"year_{year}"):
                    selected_years.append(year)
            else:
                st.checkbox(f"{year} (no data)", value=False, disabled=True, key=f"year_{year}_nodata")
    
    # 2. Event Type filter - collapsible
    with st.sidebar.expander("🏛️ Event Type Filter", expanded=True):
        event_types = sorted(df['event_type'].unique())
        selected_event_types = []
        for et in event_types:
            if st.checkbox(et, value=True, key=f"event_type_{et}"):
                selected_event_types.append(et)
    
    # 3. Province filter - collapsible
    with st.sidebar.expander("📍 Province Filter", expanded=True):
        provinces = sorted(df['province'].unique())
        selected_provinces = []
        for prov in provinces:
            if st.checkbox(prov, value=True, key=f"province_{prov}"):
                selected_provinces.append(prov)
    
    # 4. Clusters filter - collapsible
    with st.sidebar.expander("🏷️ Theme/Cluster Filter", expanded=True):
        clusters = sorted(df['cluster_theme'].unique())
        selected_clusters = []
        for cluster in clusters:
            if st.checkbox(cluster, value=True, key=f"cluster_{cluster}"):
                selected_clusters.append(cluster)
    
    # Show total available (before filtering)
    st.sidebar.write(f"**Total Protests:** {len(df)}")
    
    # === Apply filters ===
    # Start with year filter
    if selected_years:
        filtered_df = df[df['year'].isin(selected_years)].copy()
    else:
        filtered_df = df.iloc[0:0]  # empty
    
    # Then event_type
    if selected_event_types:
        filtered_df = filtered_df[filtered_df['event_type'].isin(selected_event_types)]
    else:
        filtered_df = filtered_df.iloc[0:0]
    
    # Then province
    if selected_provinces:
        filtered_df = filtered_df[filtered_df['province'].isin(selected_provinces)]
    else:
        filtered_df = filtered_df.iloc[0:0]
    
    # Then clusters
    if selected_clusters:
        filtered_df = filtered_df[filtered_df['cluster_theme'].isin(selected_clusters)]
    else:
        filtered_df = filtered_df.iloc[0:0]
    
    # === Summary metrics ===
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Protests in Selection", len(filtered_df))
    with col2:
        st.metric("Years Selected", len(selected_years))
    with col3:
        if len(selected_years) > 0:
            avg_per_year = len(filtered_df) / len(selected_years)
            st.metric("Avg. Protests/Year", f"{avg_per_year:.0f}")
        else:
            st.metric("Avg. Protests/Year", "0")
    with col4:
        st.metric("Themes Selected", len(selected_clusters))
    
    # === Map ===
    if not filtered_df.empty:
        with st.spinner("Rendering heatmap..."):
            deck = create_map(filtered_df)
            if deck:
                st.pydeck_chart(deck)
    else:
        st.warning("No protests match the selected filters. Please adjust your selections.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "*Use the sidebar to filter protests by year, event type, province, and theme. "
        "The heatmap intensity shows areas with higher concentrations of protests.*"
    )

if __name__ == "__main__":
    main()