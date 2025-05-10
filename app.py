from flask import Flask, send_file
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

app = Flask(__name__)

@app.route('/')
def run_analysis():
    # Load and parse data
    df = pd.read_csv("Sample_Data.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y %H:%M')

    # Compute moving averages
    df['MA_1000'] = df['Values'].rolling(window=min(1000, len(df))).mean()
    df['MA_5000'] = df['Values'].rolling(window=min(5000, len(df))).mean()
    df['MA_5day'] = df.set_index('Timestamp')['Values'].rolling('5D').mean().values

    # Detect features
    df['Peak'] = (df['Values'] > df['Values'].shift(1)) & (df['Values'] > df['Values'].shift(-1))
    df['Low'] = (df['Values'] < df['Values'].shift(1)) & (df['Values'] < df['Values'].shift(-1))
    df['slope'] = df['Values'].diff()
    accelerating_down = (df['slope'].shift(1) < 0) & (df['slope'] < df['slope'].shift(1))

    # Save analysis results
    df[df['Peak']][['Timestamp', 'Values']].to_csv("peaks.csv", index=False)
    df[df['Low']][['Timestamp', 'Values']].to_csv("lows.csv", index=False)
    df[df['Values'] < 20][['Timestamp', 'Values']].to_csv("voltage_below_20.csv", index=False)
    df[accelerating_down][['Timestamp', 'slope']].to_csv("downward_acceleration.csv", index=False)

    # Remove old plots if they exist
    for fname in ["plot.png", "plot_ma5day.png"]:
        if os.path.exists(fname):
            os.remove(fname)

    # Plot all moving averages + original
    plt.figure(figsize=(16, 8))
    plt.plot(df['Timestamp'], df['Values'], label='Original Value', color='blue', linewidth=1)
    plt.plot(df['Timestamp'], df['MA_1000'], label='1000 MA', color='red', linewidth=2)
    plt.plot(df['Timestamp'], df['MA_5000'], label='5000 MA', color='green', linewidth=2)
    plt.plot(df['Timestamp'], df['MA_5day'], label='5-Day MA', color='purple', linewidth=2)

    ax = plt.gca()
    ax.set_xticks(df['Timestamp'][::len(df)//20])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M'))
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig("plot.png")
    plt.close()

    # Plot 5-day MA separately
    plt.figure(figsize=(16, 8))
    plt.plot(df['Timestamp'], df['MA_5day'], label='5-Day MA', color='purple', linewidth=2)
    plt.title("5-Day Moving Average")
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_ma5day.png")
    plt.close()

    return "Analysis complete. View plots at /plot and /plot/ma5day, or download results from /download/{filename}"

@app.route('/download/<filename>')
def download_file(filename):
    if not os.path.exists(filename):
        return f"{filename} not found. Visit / first to generate it.", 404
    return send_file(filename, as_attachment=True)

@app.route('/plot')
def view_plot():
    if not os.path.exists("plot.png"):
        return "plot.png not found. Visit / first to generate it.", 404
    return send_file("plot.png", mimetype='image/png')

@app.route('/plot/ma5day')
def view_ma5day_plot():
    if not os.path.exists("plot_ma5day.png"):
        return "plot_ma5day.png not found. Visit / first to generate it.", 404
    return send_file("plot_ma5day.png", mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
