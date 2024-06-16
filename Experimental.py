import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkinter.font import Font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import yfinance as yf
from datetime import datetime

# Global variables
figsize = (8, 6)  # Adjusted figure size for better visibility
startdate = '2020-01-01'
ratio_threshold = 0.05

def get_trading_advice(ratio, historical_ratio, stock1, stock2):
    if ratio >= historical_ratio + ratio_threshold * historical_ratio:
        return f"Go Short {stock1} and Go Long {stock2}"
    elif ratio <= historical_ratio - ratio_threshold * historical_ratio:
        return f"Go Long {stock1} and Go Short {stock2}"
    else:
        return "Hold"

def fetch_historical_data(stocks, start_date, end_date):
    data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']
    return data

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def plot_pair(canvas, stocks, title):
    data = fetch_historical_data(stocks, start_date=startdate, end_date=datetime.today().strftime('%Y-%m-%d'))
    fig = Figure(figsize=figsize, dpi=100)
    ax1 = fig.add_subplot(211)
    data.plot(ax=ax1)
    ax1.set_title(f'{title[0]} vs {title[1]}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')

    rsi = calculate_rsi(data[stocks[0]])
    ax2 = fig.add_subplot(212)
    ax2.plot(rsi.index, rsi, label='RSI', color='g')
    ax2.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
    ax2.axhline(y=30, color='b', linestyle='--', label='Oversold (30)')
    ax2.set_title('Relative Strength Index (RSI)')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')
    ax2.legend()

    canvas = FigureCanvasTkAgg(fig, master=canvas)
    canvas.draw()
    canvas.get_tk_widget().pack()

def create_scrollable_frame(root):
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    plot_frame = ttk.Frame(canvas)  # Create the frame without bg parameter
    plot_frame.pack(fill=tk.BOTH, expand=True)

    canvas.create_window((0, 0), window=plot_frame, anchor=tk.NW)

    plots = [
        (plot_pair, plot_frame, ['AAPL', 'MSFT'], ['Apple (AAPL)', 'Microsoft (MSFT)']),
        (plot_pair, plot_frame, ['AMZN', 'GOOGL'], ['Amazon (AMZN)', 'Google (GOOGL)']),
        (plot_pair, plot_frame, ['V', 'MA'], ['Visa (V)', 'Mastercard (MA)']),
    ]

    for plot_func, master, stocks, title in plots:
        plot_func(master, stocks, title)

    return canvas

root = tk.Tk()
root.title("Pairs Trading Analysis")
root.geometry("900x600")  # Set initial window size

font_title = Font(family="Helvetica", size=16, weight="bold")
font_label = Font(family="Helvetica", size=12)

header = ttk.Label(root, text="Pairs Trading Analysis", font=font_title)
header.pack(pady=10)

scrollable_frame = create_scrollable_frame(root)
scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()
