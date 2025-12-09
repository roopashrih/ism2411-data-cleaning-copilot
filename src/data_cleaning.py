# The purpose of this script is to clean the raw sales dataset.

import pandas as pd

# Load the raw sales data
def load_data(file_path: str):
    return pd.read_csv(file_path)

# Standardize column names to lowercase and underscores to make it easier to reference them in code.
def clean_column_names(df):
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
    return df

# Strip leading/trailing whitespace from product names and categories because extra spaces cause duplicates.
def strip_whitespace(df):
    df['prodname'] = df['prodname'].astype(str).str.strip() 
    df['category'] = df['category'].astype(str).str.strip()
    return df

# Convert to numeric value to ensure calculations can be done. 
def convert_to_numeric(df):
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
    return df

# Handles missing values in the DataFrame by dropping rows with critical missing data.
def handle_missing_values(df):
    df = df.dropna(subset=['prodname', 'price', 'qty'])
    df['category'] = df['category'].fillna('Unknown')
    return df


# Removes rows with invalid values such as negative prices or quantities.
def remove_invalid_rows(df):
    filtered = df[(df['price'] >= 0) & (df['qty'] >= 0) & (df['total_sales'] >= 0)] 
    filtered = filtered.reset_index(drop=True) 
    return filtered

# Main cleaning function
if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = convert_to_numeric(df_clean)
    df_clean = handle_missing_values(df_clean)
    df_clean.to_csv(cleaned_path, index=False)

    df_clean['total_sales'] = df_clean['price'] * df_clean['qty']
    df_clean = remove_invalid_rows(df_clean)

    print("Cleaning complete. First few rows:")
    print(df_clean.head())
