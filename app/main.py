import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .utils import load_data, get_top_regions, filter_by_countries

# --- App Title ---
st.set_page_config(page_title="Data Insights Dashboard", layout="wide")
st.title("🌍 Global Insights Dashboard")

# --- Load Data ---
st.sidebar.header("Data Selection")
file_path = st.sidebar.text_input("Enter path to local CSV file", "..data/benin-malanville.csv")

if file_path:
    try:
        df = load_data(file_path)
        st.success("✅ Data loaded successfully!")
        
        # --- Sidebar Filters ---
        countries = st.sidebar.multiselect("Select Countries", df["Country"].unique())
        filtered_df = filter_by_countries(df, countries)
        
        # --- Visualization Section ---
        st.header("📊 Data Visualizations")
        
        plot_type = st.selectbox("Choose plot type", ["Boxplot", "Bar Chart"])
        column = st.selectbox("Select column to visualize", df.select_dtypes("number").columns)
        
        if plot_type == "Boxplot":
            fig, ax = plt.subplots()
            sns.boxplot(data=filtered_df, x="Country", y=column, ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        elif plot_type == "Bar Chart":
            fig, ax = plt.subplots()
            sns.barplot(data=filtered_df, x="Country", y=column, ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # --- Top Regions Table ---
        st.header("🏆 Top Regions by Metric")
        top_n = st.slider("Select Top N Regions", 5, 20, 10)
        top_regions = get_top_regions(df, column, top_n)
        st.dataframe(top_regions)
    
    except Exception as e:
        st.error(f"❌ Failed to load or process data: {e}")
else:
    st.info("👈 Enter a valid local CSV file path to begin.")
