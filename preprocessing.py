import pandas as pd
import glob # For file handling so we can load all CSV files in the data folder
import os

# Load all 12 CSV files from the data folder and combine them
csv_files = glob.glob(os.path.join('data', '*.csv'))

df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

print("=== SHAPE (rows, columns) ===")
print(df.shape)

print("\n=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== COLUMN DATA TYPES ===")
print(df.dtypes)

print("\n=== GENERAL INFO ===")
print(df.info())

print("\n=== STATISTICS ===")
print(df.describe())

print("\n=== MISSING VALUES PER COLUMN ===")
print(df.isnull().sum())

numeric_fill_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3',
                     'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']

df[numeric_fill_cols] = df.groupby('station')[numeric_fill_cols].transform(
    lambda x: x.ffill().bfill()
)

# ── CLEAN CATEGORICAL COLUMN 
df['wd'] = df.groupby('station')['wd'].transform(
    lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 'N')
)

# ── CONFIRM CLEANING 
print("\n=== MISSING VALUES AFTER CLEANING ===")
print(df.isnull().sum())

print("\n=== SHAPE AFTER CLEANING ===")
print(df.shape)

# ── OUTLIER HANDLING 

outlier_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3',
                'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']

print("=== OUTLIER BOUNDS PER COLUMN ===")

for col in outlier_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers_count = ((df[col] < lower) | (df[col] > upper)).sum()
    print(f"{col}: lower={lower:.2f}, upper={upper:.2f}, outliers found={outliers_count}")

    # Cap the outliers
    df[col] = df[col].clip(lower=lower, upper=upper)

print("\n=== STATISTICS AFTER OUTLIER CAPPING ===")
print(df[outlier_cols].describe())

# ── 24-HOUR MOVING AVERAGE ────────────────────────────────────────

# Sort by station and time to ensure correct rolling order
df = df.sort_values(['station', 'year', 'month', 'day', 'hour']).reset_index(drop=True)

# Create 24-hour MA for PM2.5 and PM10, grouped by station
df['PM2.5_24hr_MA'] = df.groupby('station')['PM2.5'].transform(
    lambda x: x.rolling(window=24, min_periods=1).mean()
)

df['PM10_24hr_MA'] = df.groupby('station')['PM10'].transform(
    lambda x: x.rolling(window=24, min_periods=1).mean()
)

print("=== NEW MOVING AVERAGE COLUMNS ===")
print(df[['station', 'year', 'month', 'day', 'hour', 
          'PM2.5', 'PM2.5_24hr_MA', 
          'PM10', 'PM10_24hr_MA']].head(30))

# Save the cleaned DataFrame to a CSV file for easy opening
output_path = 'cleaned_combined_processed.csv'
df.to_csv(output_path, index=False)
print(f"\n=== CLEANED DATA SAVED ===\nSaved to: {os.path.abspath(output_path)}")
print("\n=== PREVIEW OF SAVED FILE ===")
print(df.head())

def get_cleaned_data():
    return df