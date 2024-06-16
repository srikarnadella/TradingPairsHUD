import tkinter as tk
from tkinter import ttk, Label, Entry, Button
from tkinter.font import Font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
from datetime import datetime, timedelta

# Global variables
figsize = (8, 6)
xaxislabelsize = 8
xaxislabelangle = 30
startdate = '2020-01-01'
wrap_length = 300
ratio_threshold = 0.05
numYears = 1
h_space = 0.5

def get_trading_advice(ratio, historicalratio, stock1, stock2):
    if ratio >= historicalratio + ratio_threshold * historicalratio:
        return f"Go Short {stock1} and Go Long {stock2}"
    elif ratio <= historicalratio - ratio_threshold * historicalratio:
        return f"Go Long {stock1} and Go Short {stock2}"
    else:
        return "Hold"

def fetch_historical_data(stocks, start_date, end_date):
    data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']
    return data

def plot_pair(stock1, stock2):
    stocks = [stock1, stock2]
    enddate = datetime.today().strftime('%Y-%m-%d')
    data = fetch_historical_data(stocks, start_date=startdate, end_date=enddate)
    
    fig = Figure(figsize=figsize, dpi=100)
    plot = fig.add_subplot(2, 1, 1)
    data.plot(ax=plot)
    plot.set_title(f'{stock1} vs {stock2}')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')
    plot.xaxis.set_tick_params(rotation=xaxislabelangle, labelsize=xaxislabelsize)
    
    rsi = calculate_rsi(data[stock1])
    plot_rsi = fig.add_subplot(2, 1, 2)
    plot_rsi.plot(rsi.index, rsi, label='RSI', color='g')
    plot_rsi.axhline(y=70, color='r', linestyle='--', label="Overbought (70)")
    plot_rsi.axhline(y=30, color='r', linestyle='--', label="Oversold (30)")
    plot_rsi.set_title('RSI (14 days)')
    plot_rsi.set_xlabel('Date')
    plot_rsi.set_ylabel('RSI')
    plot_rsi.legend(loc='lower right')
    fig.subplots_adjust(left=0.1, right=0.9, hspace=h_space)
    plot_rsi.xaxis.set_tick_params(rotation=xaxislabelangle, labelsize=xaxislabelsize)

    years_ago = (datetime.today() - timedelta(days=numYears * 365)).strftime('%Y-%m-%d')
    years_ago_data = fetch_historical_data(stocks, start_date=years_ago, end_date=enddate)
    if not data.empty and not years_ago_data.empty:
        historical_ratio = years_ago_data[stock1] / years_ago_data[stock2]
        current_values = data.iloc[-1]
        current_ratio = current_values[stock1] / current_values[stock2]
        advice = get_trading_advice(current_ratio, historical_ratio.mean(), stock1, stock2)
        text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
               f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
               f"{stock1 + ':':<18} {current_values[stock1]:.2f}\n" \
               f"{stock2 + ':':<18} {current_values[stock2]:.2f}\n\n" \
               f"Ratio Threshold: {ratio_threshold}\n" \
               f"Trading Advice:\n{advice}"
        
        label = Label(frame, text=text, justify='left', font=font, padx=10, pady=10, wraplength=wrap_length)
        label.pack(side='left', anchor='nw')
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

root = tk.Tk()
root.title("Custom Stock Pair Analysis")

font = Font(weight='bold')

label1 = Label(root, text="Enter Stock 1:")
label1.pack(pady=5)
entry1 = Entry(root)
entry1.pack()

label2 = Label(root, text="Enter Stock 2:")
label2.pack(pady=5)
entry2 = Entry(root)
entry2.pack()

frame = ttk.Frame(root, relief="sunken")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def plot_button():
    stock1 = entry1.get().strip().upper()
    stock2 = entry2.get().strip().upper()
    if stock1 and stock2:
        plot_pair(stock1, stock2)
    else:
        label = Label(frame, text="Please enter both stocks.", justify='left', font=font, padx=10, pady=10)
        label.pack(side='left', anchor='nw')

button = Button(root, text="Plot", command=plot_button)
button.pack(pady=10)

# Fit window to screen size
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}")

root.mainloop()
