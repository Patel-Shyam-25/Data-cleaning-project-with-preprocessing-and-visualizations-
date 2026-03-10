# Beijing Air Quality — Data Preprocessing

A data preprocessing pipeline applied to the **Beijing Multi-Site Air Quality Dataset** from the UCI Machine Learning Repository. This project cleans, transforms, and visualizes hourly air quality readings collected across 12 monitoring stations in Beijing from 2013 to 2017.

---

## 📁 Project Structure

```
project/
│
├── data/                          # Raw CSV files (12 stations)
│   └── PRSA_Data_*.csv
│
├── output/                        # Generated plots
│   ├── plot1_avg_pm25_by_station.png
│   ├── plot2_pm25_raw_vs_ma.png
│   └── plot3_pm25_by_hour.png
│
├── preprocessing.py               # Data loading, cleaning, outlier handling, feature engineering
├── visualizations.py              # Data visualizations
└── README.md
```
## 🛠️ Tools & Libraries

| Tool | Purpose |
|------|---------|
| Python 3 | Core programming language |
| pandas | Data loading, cleaning, and transformation |
| glob / os | Loading multiple CSV files from a directory |
| matplotlib | Data visualization |
| seaborn | Enhanced chart styling |
---

## 📊 Dataset

- **Source:** [UCI Machine Learning Repository — Dataset ID 501](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data)
- **Size:** 420,768 rows × 18 columns
- **Coverage:** 12 monitoring stations, March 2013 – February 2017
- **Features:** PM2.5, PM10, SO2, NO2, CO, O3, temperature, pressure, dew point, rainfall, wind speed, wind direction

---

## ⚙️ Preprocessing Pipeline

### 1. Handling Missing Values
- **Numeric columns** (PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, WSPM): Forward fill then backward fill, grouped by station. This preserves the temporal continuity of time-series data better than mean/median imputation.
- **Categorical column** (`wd` — wind direction): Filled with the mode per station, since string categories cannot be averaged mathematically.

### 2. Handling Outliers
- Detected using the **IQR method** (flag values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR)
- Handled using **Winsorization (capping)** — clipping to boundary values rather than dropping rows, preserving real extreme pollution events

### 3. Feature Engineering
- Created `PM2.5_24hr_MA` and `PM10_24hr_MA` — 24-hour rolling averages grouped by station to smooth short-term fluctuations and reveal longer-term trends

---

## 📈 Visualizations

| Plot | Description |
|------|-------------|
| Average PM2.5 by Station | Bar chart comparing mean PM2.5 across all 12 stations |
| Raw PM2.5 vs 24hr Moving Average | Line chart showing how the MA smooths noisy hourly readings |
| Average PM2.5 by Hour of Day | Line chart revealing daily pollution patterns across all stations |

---


---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

**2. Install dependencies**
```bash
pip install pandas matplotlib seaborn
```

**3. Download the dataset**

Download the CSV files from the [UCI Repository](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data) and place them in the `data/` folder.

**4. Run preprocessing**
```bash
python preprocessing.py
```

**5. Generate visualizations**
```bash
python visualizations.py
```

---
