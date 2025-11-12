import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV data from a local file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise FileNotFoundError(f"Error loading data: {e}")

def get_top_regions(df: pd.DataFrame, column: str, top_n: int = 10) -> pd.DataFrame:
    """Return top regions by a given column value."""
    return df.nlargest(top_n, column)[["Country", column]]

def filter_by_countries(df: pd.DataFrame, countries: list) -> pd.DataFrame:
    """Filter dataframe by selected countries."""
    if not countries:
        return df
    return df[df["Country"].isin(countries)]
