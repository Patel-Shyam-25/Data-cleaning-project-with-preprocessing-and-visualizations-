import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the cleaned dataframe from the saved CSV file
df = pd.read_csv('cleaned_combined_processed.csv')

# ── PLOT 1 ────────────────────────────────────────────────────────
station_avg = df.groupby('station')['PM2.5'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x=station_avg.index, y=station_avg.values, hue=station_avg.index, palette='Reds_r', legend=False)
plt.title('Average PM2.5 by Station', fontsize=16)
plt.xlabel('Station', fontsize=12)
plt.ylabel('Average PM2.5 (µg/m³)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('output/plot1_avg_pm25_by_station.png')
plt.show()

# ── PLOT 2 ────────────────────────────────────────────────────────
one_station = df[df['station'] == 'Aotizhongxin'].copy()
one_station['datetime'] = pd.to_datetime(one_station[['year', 'month', 'day', 'hour']])
one_station = one_station.sort_values('datetime')

mask = (one_station['datetime'] >= '2014-01-01') & (one_station['datetime'] <= '2014-03-31')
sample = one_station[mask]

plt.figure(figsize=(14, 5))
plt.plot(sample['datetime'], sample['PM2.5'], color='lightblue', alpha=0.6, label='Raw PM2.5')
plt.plot(sample['datetime'], sample['PM2.5_24hr_MA'], color='darkblue', linewidth=2, label='24hr Moving Average')
plt.title('PM2.5 Raw vs 24-Hour Moving Average (Aotizhongxin, Jan–Mar 2014)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('PM2.5 (µg/m³)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('output/plot2_pm25_raw_vs_ma.png')
plt.show()

# ── PLOT 3 ────────────────────────────────────────────────────────
hourly_avg = df.groupby('hour')['PM2.5'].mean()

plt.figure(figsize=(10, 5))
plt.plot(hourly_avg.index, hourly_avg.values, marker='o', color='darkorange', linewidth=2)
plt.title('Average PM2.5 by Hour of Day (All Stations)', fontsize=14)
plt.xlabel('Hour of Day (0 = Midnight)', fontsize=12)
plt.ylabel('Average PM2.5 (µg/m³)', fontsize=12)
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('output/plot3_pm25_by_hour.png')
plt.show()