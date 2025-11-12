# # import streamlit as st

# # st.title("Hello, Streamlit!")
# # st.write("This is a simple Streamlit application.")

# # st.sidebar.header("Sidebar")
# # st.sidebar.write("This is the sidebar content.")


# # favorite_color = st.selectbox(
# #     "What's your favorite color?",
# #     ["Red", "Green", "Blue", "Yellow", "Other"])

# # app.py

# import streamlit as st
# import pandas as pd
# import plotly.express as px

# #st.set_page_config(layout="wide")
# st.title("📈 Company Performance Comparator")
# st.write("Upload sales data for two companies to compare them side-by-side.")

# # --- File Uploaders in Sidebar ---
# st.sidebar.header("Upload Your Data")

# # Create two columns for the file uploaders
# col1, col2, col3 = st.sidebar.columns(3)

# with col1:
#     uploaded_file_1 = st.file_uploader("Upload Company A's CSV", type="csv", key="file1")

# with col2:
#     uploaded_file_2 = st.file_uploader("Upload Company B's CSV", type="csv", key="file2")
# with col3:
#     uploaded_file_2 = st.file_uploader("Upload Company C's CSV", type="csv", key="file3")


# # Check if both files have been uploaded before proceeding
# if uploaded_file_1 is not None and uploaded_file_2 is not None:
#     try:
#         # Read each CSV file into a separate DataFrame
#         df1 = pd.read_csv(uploaded_file_1)
#         df2 = pd.read_csv(uploaded_file_2)

#         # --- THE CRUCIAL STEP: COMBINING DATA ---
#         # Add a new column to each DataFrame to identify the company
#         df1['Company'] = 'Company A'
#         df2['Company'] = 'Company B'

#         # Combine the two DataFrames into a single one
#         df_combined = pd.concat([df1, df2], ignore_index=True)

#         st.sidebar.success("Files uploaded and combined successfully!")

#     except Exception as e:
#         st.error(f"Error processing files: {e}")
#         st.stop()


#     # --- DISPLAY THE DASHBOARD ---
#     st.header("Side-by-Side Performance")

#     # --- 1. Key Performance Indicators (KPIs) ---
#     st.subheader("Overall Totals")
    
#     # Create two columns for the KPIs
#     kpi_col1, kpi_col2 = st.columns(2)
    
#     with kpi_col1:
#         total_revenue_A = df1['Revenue'].sum()
#         st.metric(label="Company A Total Revenue", value=f"${total_revenue_A:,}")

#     with kpi_col2:
#         total_revenue_B = df2['Revenue'].sum()
#         st.metric(label="Company B Total Revenue", value=f"${total_revenue_B:,}")

#     # --- 2. Comparative Bar Chart ---
#     st.subheader("Monthly Revenue Comparison")
    
#     # Let the user select which metric to plot
#     metric_to_plot = st.selectbox("Select a metric to compare:", ['Revenue', 'Units Sold'])
    
#     fig = px.bar(
#         df_combined,
#         x='Month',
#         y=metric_to_plot,
#         color='Company',        
#         barmode='group',        # This places bars side-by-side
#         title=f"Monthly {metric_to_plot} Comparison"
#     )
#     st.plotly_chart(fig, use_container_width=True)
    
#     # --- 3. Data Preview ---
#     with st.expander("Show Combined Data"):
#         st.dataframe(df_combined)

# # This is the message that shows before files are uploaded
# else:
#     st.info("Please upload both CSV files in the sidebar to begin the comparison.")





import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Solar Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("../data/benin-malanville_clean.csv")   # adjust name if needed
    return df

df = load_data()

# ------------------------------------
# Validate expected columns
# ------------------------------------
expected_cols = [ "GHI", "DNI"]
missing = [c for c in expected_cols if c not in df.columns]

if missing:
    st.error(f"Your dataset is missing required columns: {missing}")
    st.stop()

# ------------------------------------
# Sidebar Controls
# ------------------------------------
st.sidebar.header("Controls")

countries = sorted(df["DNI"].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries", options=countries, default=countries
)

metric = st.sidebar.selectbox(
    "Select Metric to Visualize",
    [c for c in ["GHI", "DNI", "DHI"] if c in df.columns]
)

filtered_df = df[df["DNI"].isin(selected_countries)]

# ------------------------------------
# Title
# ------------------------------------
st.title("Solar Resource Dashboard")

# ------------------------------------
# Boxplot
# ------------------------------------
st.subheader(f"{metric} Distribution by Country")

fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(data=filtered_df, x="DNI", y=metric, ax=ax)
ax.set_title(f"{metric} Comparison")
st.pyplot(fig)

# ------------------------------------
# Top Regions (only if Region exists)
# ------------------------------------
if "Region" in df.columns:
    st.subheader(f"Top Regions by Average {metric}")
    top_regions = (
        filtered_df.groupby(["Country", "Region"], as_index=False)[metric]
        .mean()
        .sort_values(by=metric, ascending=False)
    )
    st.dataframe(top_regions)
else:
    st.info("No 'Region' column found. Skipping region ranking table.")
