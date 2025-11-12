import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_all_countries, create_boxplot, create_ranking_chart, create_scatter_plot, create_time_series_plot

# Page config
st.set_page_config(page_title="Solar Data Dashboard", layout="wide")

# Title
st.title("Solar Farm Analysis Dashboard")
st.markdown("Compare solar potential across Benin, Sierra Leone, and Togo.")

# Load data using utils function
data_dict, all_data = load_all_countries()

if not data_dict:
    st.error("No data files could be loaded. Please ensure cleaned CSV files are in the data/ folder.")
    st.stop()

# Sidebar filters
st.sidebar.header("📊 Dashboard Controls")

# Country selection
available_countries = list(data_dict.keys())
selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare",
    options=available_countries,
    default=available_countries
)

# Metric selection
available_metrics = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH', 'BP']
selected_metric = st.sidebar.selectbox(
    "Select Solar Metric",
    options=available_metrics,
    index=0
)

# Filter data based on selection
filtered_data = all_data[all_data['Country'].isin(selected_countries)]

# Main content
if selected_countries:
    # Row 1: Distribution and Statistics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"{selected_metric} Distribution Comparison")
        
        # Create boxplot using utils function
        fig = create_boxplot(filtered_data, selected_countries, selected_metric)
        if fig:
            st.pyplot(fig)
        else:
            st.warning(f"No valid data available for {selected_metric} in selected countries.")
    
    with col2:
        st.subheader("📈 Summary Statistics")
        
        # Summary table
        summary_stats = filtered_data.groupby('Country')[selected_metric].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(2)
        
        st.dataframe(summary_stats.style.highlight_max(axis=0, subset=['mean', 'median'], color='#90EE90'))
    
    # Row 2: Ranking
    if 'GHI' in filtered_data.columns:
        st.subheader("🏆 Country Ranking by Average GHI")
        
        ghi_data = filtered_data.groupby('Country')['GHI'].mean().sort_values(ascending=False)
        
        if not ghi_data.empty:
            # Create ranking chart using utils function
            fig2 = create_ranking_chart(ghi_data)
            st.pyplot(fig2)
            
            # Display top performer
            top_country = ghi_data.index[0]
            top_value = ghi_data.iloc[0]
            st.success(f"**{top_country}** has the highest average GHI: **{top_value:.2f} W/m²**")
    
    # Row 3: Additional Insights
    st.subheader("📊 Additional Insights")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Scatter plot: GHI vs Temperature using utils function
        if all(col in filtered_data.columns for col in ['GHI', 'Tamb']):
            fig3 = create_scatter_plot(filtered_data, selected_countries, 'Tamb', 'GHI', 
                                     'Ambient Temperature (°C)', 'GHI (W/m²)', 'GHI vs Temperature')
            st.pyplot(fig3)
    
    with col4:
        # Time series of average GHI by month using utils function
        if all(col in filtered_data.columns for col in ['GHI', 'Timestamp']):
            fig4 = create_time_series_plot(filtered_data, selected_countries)
            st.pyplot(fig4)

else:
    st.warning("Please select at least one country from the sidebar.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Solar Data Discovery Challenge")