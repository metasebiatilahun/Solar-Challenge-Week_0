import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def load_all_countries():
    """
    Load all country data files and return combined dataset
    Returns:
        tuple: (data_dict, all_data) where data_dict is individual country DataFrames
               and all_data is combined DataFrame
    """
    countries = {
        "Benin": "../data/benin-malanville_clean.csv",
        "Sierra Leone": "../data/sierraleone-bumbuna_clean.csv", 
        "Togo": "../data/togo-dapaong_qc_clean.csv"
    }
    
    dfs = {}
    for country, path in countries.items():
        try:
            if os.path.exists(path):
                df = pd.read_csv(path)
                # Convert timestamp if exists
                if 'Timestamp' in df.columns:
                    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                # Add country column
                df['Country'] = country
                dfs[country] = df
        except Exception as e:
            print(f"Error loading {country}: {str(e)}")
    
    # Combine all data
    if dfs:
        all_data = pd.concat(dfs.values(), ignore_index=True)
        return dfs, all_data
    else:
        return {}, pd.DataFrame()

def create_boxplot(data, countries, metric):
    """
    Create a boxplot comparing selected metric across countries
    
    Args:
        data: Combined DataFrame with all country data
        countries: List of selected countries
        metric: The metric to compare (GHI, DNI, etc.)
    
    Returns:
        matplotlib figure object or None if no data
    """
    if metric not in data.columns:
        return None
    
    # Prepare data for boxplot - remove NaN values
    plot_data = []
    labels = []
    
    for country in countries:
        country_data = data[data['Country'] == country][metric]
        # Remove NaN values
        country_data_clean = country_data.dropna()
        if len(country_data_clean) > 0:
            plot_data.append(country_data_clean)
            labels.append(country)
    
    if not plot_data:
        return None
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(plot_data, labels=labels)
    
    # Set labels and title
    unit = 'W/m²' if metric in ['GHI', 'DNI', 'DHI'] else 'Units'
    ax.set_ylabel(f"{metric} ({unit})")
    ax.set_title(f"{metric} Distribution by Country")
    ax.grid(True, alpha=0.3)
    
    return fig

def create_ranking_chart(ranking_data):
    """
    Create a bar chart showing country ranking by GHI
    
    Args:
        ranking_data: Series with country names as index and GHI values
    
    Returns:
        matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    
    countries = ranking_data.index
    values = ranking_data.values
    
    # Create color palette
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    bars = ax.bar(countries, values, color=colors[:len(countries)])
    ax.set_ylabel('Average GHI (W/m²)')
    ax.set_title('Country Ranking by Solar Potential')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.xticks(rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    return fig

def create_scatter_plot(data, countries, x_metric, y_metric, x_label, y_label, title):
    """
    Create a scatter plot comparing two metrics
    
    Args:
        data: Combined DataFrame
        countries: List of selected countries
        x_metric: Metric for x-axis
        y_metric: Metric for y-axis
        x_label: Label for x-axis
        y_label: Label for y-axis
        title: Plot title
    
    Returns:
        matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Color palette for countries
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, country in enumerate(countries):
        country_data = data[data['Country'] == country]
        color = colors[i % len(colors)]
        ax.scatter(country_data[x_metric], country_data[y_metric], 
                  alpha=0.6, label=country, s=30, color=color)
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

def create_time_series_plot(data, countries):
    """
    Create a time series plot of monthly average GHI
    
    Args:
        data: Combined DataFrame with Timestamp column
        countries: List of selected countries
    
    Returns:
        matplotlib figure object
    """
    # Extract month from timestamp
    data_copy = data.copy()
    data_copy['Month'] = data_copy['Timestamp'].dt.month
    
    # Calculate monthly averages
    monthly_ghi = data_copy.groupby(['Country', 'Month'])['GHI'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Color palette
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, country in enumerate(countries):
        country_data = monthly_ghi[monthly_ghi['Country'] == country]
        color = colors[i % len(colors)]
        ax.plot(country_data['Month'], country_data['GHI'], 
                marker='o', label=country, linewidth=2, color=color, markersize=6)
    
    ax.set_xlabel('Month')
    ax.set_ylabel('Average GHI (W/m²)')
    ax.set_title('Monthly Average GHI Trends')
    ax.set_xticks(range(1, 13))
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

def get_summary_statistics(data, countries, metric):
    """
    Calculate summary statistics for selected countries and metric
    
    Args:
        data: Combined DataFrame
        countries: List of selected countries
        metric: The metric to analyze
    
    Returns:
        DataFrame with summary statistics
    """
    if metric not in data.columns:
        return pd.DataFrame()
    
    filtered_data = data[data['Country'].isin(countries)]
    summary_stats = filtered_data.groupby('Country')[metric].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(2)
    
    return summary_stats