# Sensor Data Analysis Web App

This Flask-based web app performs analysis on time-series sensor data provided in `Sample_Data.csv`. It calculates:

- Moving averages (1000, 5000, and 5-day windows)
- Local peaks and lows
- Downward slope accelerations
- Instances where voltage drops below 20

It also generates a plot and provides downloadable CSVs for all processed results.

---

## 📊 Features

- 📈 Automatically analyzes uploaded sensor data
- 🗂️ Generates CSVs for:
  - Peaks
  - Lows
  - Voltage < 20
  - Downward acceleration
- 🖼️ Saves a visual chart of the data and moving averages

---

## 🌐 Web Routes

| URL Path                             | What it Does                                      |
|--------------------------------------|---------------------------------------------------|
| `/`                                  | Runs full analysis and generates plot/CSVs        |
| `/download/peaks.csv`                | Downloads CSV of local peaks                     |
| `/download/lows.csv`                 | Downloads CSV of local lows                      |
| `/download/voltage_below_20.csv`     | Downloads CSV where voltage dropped below 20     |
| `/download/downward_acceleration.csv`| Downloads CSV of downward slope accelerations    |
| `/static/plot.png`                   | Opens the generated plot image                   |

---
