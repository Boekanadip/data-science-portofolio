import pandas as pd

def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    
    # Drop missing values
    df.dropna(inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Create TotalRevenue column
    df['TotalRevenue'] = df['Quantity'] * df['UnitPrice']

    return df

if __name__ == "__main__":
    df_clean = load_and_clean_data("data/Online_Retail.xlxs")
    df_clean.to_csv("data/Online_Retail.xlxs", index=False)
    print("Data berhasil dibersihkan dan disimpan.")
