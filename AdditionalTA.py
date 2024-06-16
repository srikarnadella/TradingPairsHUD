import tkinter as tk
from tkinter import ttk
from tkinter import Label, Text, Scrollbar
from tkinter.font import Font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import yfinance as yf  # Using yfinance for fetching historical stock data
from datetime import datetime, timedelta

# Global variable for figure size
figsize = (6, 5.5)  # Change this to adjust the size of all charts uniformly
xaxislabelsize = 8
xaxislabelangle = 30
#enddate = '2023-01-01'
enddate = datetime.today().strftime('%Y-%m-%d')
startdate = '2020-01-01'
wrap_length = 200
ratio_threshold = 0.05
numYears = 1
h_space = 0.8

def get_trading_advice(ratio, historicalratio, stock1, stock2):
    if ratio >= historicalratio + ratio_threshold*historicalratio:
        return f"Go Short {stock1} and Go Long {stock2}"
    elif ratio <= historicalratio - ratio_threshold*historicalratio:
        return f"Go Long {stock1} and Go Short {stock2}"
    else:
        return "Hold"
    
    
# Function to calculate Relative Strength Index (RSI)
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate Simple Moving Average (SMA)
def calculate_sma(data, window):
    return data.rolling(window=window).mean()

# Fetch historical data for a stock
def fetch_historical_data(stocks, start_date, end_date):
    data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']
    return data

# Function to plot pair 1: AMZN vs GOOGL
def plot_pair1():
    stocks = ['AMZN', 'GOOGL']
    data = fetch_historical_data(stocks, start_date=startdate, end_date=enddate)
    
    fig = Figure(figsize=figsize, dpi=100)
    plot = fig.add_subplot(2, 1, 1)
    data.plot(ax=plot)
    plot.set_title('AMZN vs GOOGL')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')
    plot.xaxis.set_tick_params(rotation=xaxislabelangle, labelsize=xaxislabelsize)
    # Calculate and plot RSI
    rsi = calculate_rsi(data['AMZN'])
    plot_rsi = fig.add_subplot(2, 1, 2)
    plot_rsi.plot(rsi.index, rsi, label='RSI', color='g')
    plot_rsi.axhline(y=70, color='r', linestyle='--',label = "Overbought (70)")  # Overbought threshold
    plot_rsi.axhline(y=30, color='r', linestyle='--',label = "Oversold (30)")  # Oversold threshold
    plot_rsi.set_title('RSI (14 days)')
    plot_rsi.set_xlabel('Date')
    plot_rsi.set_ylabel('RSI')
    plot_rsi.legend(loc='lower right')
    fig.subplots_adjust(left=0.1, right=0.9, hspace=h_space)  # Adjust margins and spacing
    plot_rsi.xaxis.set_tick_params(rotation=xaxislabelangle, labelsize=xaxislabelsize)
    # Display historical ratio, current values, and current ratio in a formatted text box
    years_ago = (datetime.today() - timedelta(days=numYears*365)).strftime('%Y-%m-%d')
    years_ago_data = fetch_historical_data(stocks, start_date=years_ago, end_date=enddate)
    if not data.empty and not years_ago_data.empty:
        historical_ratio = years_ago_data['AMZN'] / years_ago_data['GOOGL']
        current_values = data.iloc[-1]
        current_ratio = current_values['AMZN'] / current_values['GOOGL']
        advice = get_trading_advice(current_ratio, historical_ratio.mean(),'AMZN', 'GOOGL')
        text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
               f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
               f"{'AMZN:':<18} {current_values['AMZN']:.2f}\n" \
               f"{'GOOGL:':<18} {current_values['GOOGL']:.2f}\n\n" \
               f"Ratio Threshold: {ratio_threshold}\n"\
               f"Trading Advice:\n{advice}"
        label = Label(frame1, text=text, justify='left', font=font, padx=10, pady=10, wraplength=wrap_length)
        label.pack(side='left', anchor='nw')  # Pack on the right side
    
    # Plot on canvas
    canvas = FigureCanvasTkAgg(fig, master=frame1)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to plot pair 2: V vs MA
def plot_pair2():
    stocks = ['V', 'MA']
    data = fetch_historical_data(stocks, start_date=startdate, end_date=enddate)
    
    fig = Figure(figsize=figsize, dpi=100)
    
    plot = fig.add_subplot(2, 1, 1)
    plot_rsi = fig.add_subplot(2, 1, 2)

    data.plot(ax=plot)
    plot.set_title('V vs MA')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')
    
    # Calculate RSI and plot
    rsi = calculate_rsi(data['V'])
    plot_rsi.plot(rsi.index, rsi, label='RSI', color='g')
    plot_rsi.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')  # Overbought threshold
    plot_rsi.axhline(y=30, color='b', linestyle='--', label='Oversold (30)')     # Oversold threshold
    plot_rsi.set_title('RSI (14 days)')
    plot_rsi.set_xlabel('Date')
    plot_rsi.set_ylabel('RSI')
    
    plot_rsi.legend(loc='lower right')
    fig.subplots_adjust(left=0.1, right=0.9, hspace=h_space)  # Adjust margins and spacing

    plot_rsi.xaxis.set_tick_params(rotation=45, labelsize=8)  # Adjust tick labels
    
    # Display historical ratio, current values, and current ratio in a formatted text box
    years_ago = (datetime.today() - timedelta(days=numYears*365)).strftime('%Y-%m-%d')
    years_ago_data = fetch_historical_data(stocks, start_date=years_ago, end_date=enddate)
    if not data.empty and not years_ago_data.empty:
        historical_ratio = years_ago_data['V'] / years_ago_data['MA']
        current_values = data.iloc[-1]
        current_ratio = current_values['V'] / current_values['MA']
        advice = get_trading_advice(current_ratio, historical_ratio.mean(),'V', 'MA')
        text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
               f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
               f"{'V:':<18} {current_values['V']:.2f}\n" \
               f"{'MA:':<18} {current_values['MA']:.2f}\n\n" \
               f"Ratio Threshold: {ratio_threshold}\n"\
               f"Trading Advice:\n{advice}"

        # Pack the label on the right side of the frame
        label = Label(frame2, text=text, justify='left', font=font, padx=10, pady=10, wraplength=wrap_length)
        label.pack(side='right', anchor='ne')  # Pack on the right side
    
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to plot pair 3: AAPL vs MSFT
def plot_pair3():
    stocks = ['AAPL', 'MSFT']
    data = fetch_historical_data(stocks, start_date=startdate, end_date=enddate)
    
    fig = Figure(figsize=figsize, dpi=100)
    plot = fig.add_subplot(2, 1, 1)
    data.plot(ax=plot)
    plot.set_title('AAPL vs MSFT')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')
    plot.xaxis.set_tick_params(rotation=xaxislabelangle, labelsize=xaxislabelsize)
    # Calculate and plot RSI
    rsi = calculate_rsi(data['AAPL'])
    plot_rsi = fig.add_subplot(2, 1, 2)
    plot_rsi.plot(rsi.index, rsi, label='RSI', color='g')
    plot_rsi.axhline(y=70, color='r', linestyle='--',label = "Overbought (70)")  # Overbought threshold
    plot_rsi.axhline(y=30, color='r', linestyle='--',label = "Oversold (30)")  # Oversold threshold
    plot_rsi.set_title('RSI (14 days)')
    plot_rsi.set_xlabel('Date')
    plot_rsi.set_ylabel('RSI')
    plot_rsi.legend(loc='lower right')
    fig.subplots_adjust(left=0.1, right=0.9, hspace=h_space)  # Adjust margins and spacing
    plot_rsi.xaxis.set_tick_params(rotation=xaxislabelangle, labelsize=xaxislabelsize)

    # Display historical ratio, current values, and current ratio in a formatted text box
    years_ago = (datetime.today() - timedelta(days=numYears*365)).strftime('%Y-%m-%d')
    years_ago_data = fetch_historical_data(stocks, start_date=years_ago, end_date=enddate)
    if not data.empty and not years_ago_data.empty:
        historical_ratio = years_ago_data['AAPL'] / years_ago_data['MSFT']
        current_values = data.iloc[-1]
        current_ratio = current_values['AAPL'] / current_values['MSFT']
        advice = get_trading_advice(current_ratio, historical_ratio.mean(),'V', 'MA')
        text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
               f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
               f"{'AAPL:':<18} {current_values['AAPL']:.2f}\n" \
               f"{'MSFT:':<18} {current_values['MSFT']:.2f}\n\n" \
               f"Ratio Threshold: {ratio_threshold}\n"\
               f"Trading Advice:\n{advice}"
        label = Label(frame3, text=text, justify='left', font=font, padx=10, pady=10, wraplength=wrap_length)
        label.pack(side='left', anchor='nw')  # Pack on the right side
    
    # Plot on canvas
    canvas = FigureCanvasTkAgg(fig, master=frame3)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to plot pair 4: XOM vs CVX
def plot_pair4():
    stocks = ['XOM', 'CVX']
    data = fetch_historical_data(stocks, start_date=startdate, end_date=enddate)
    
    fig = Figure(figsize=figsize, dpi=100)
    plot = fig.add_subplot(2, 1, 1)
    data.plot(ax=plot)
    plot.set_title('XOM vs CVX')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')
    plot.xaxis.set_tick_params(rotation=xaxislabelangle, labelsize=xaxislabelsize)
   
    # Calculate and plot RSI
    rsi = calculate_rsi(data['XOM'])
    plot_rsi = fig.add_subplot(2, 1, 2)
    plot_rsi.plot(rsi.index, rsi, label='RSI', color='g')
    plot_rsi.axhline(y=70, color='r', linestyle='--',label = "Overbought (70)")  # Overbought threshold
    plot_rsi.axhline(y=30, color='r', linestyle='--',label = "Oversold (30)")  # Oversold threshold
    plot_rsi.set_title('RSI (14 days)')
    plot_rsi.set_xlabel('Date')
    plot_rsi.set_ylabel('RSI')
    plot_rsi.legend(loc='lower right')
    fig.subplots_adjust(left=0.1, right=0.9, hspace=h_space)  # Adjust margins and spacing
    plot_rsi.xaxis.set_tick_params(rotation=xaxislabelangle, labelsize=xaxislabelsize)

    # Display historical ratio, current values, and current ratio in a formatted text box
    years_ago = (datetime.today() - timedelta(days=numYears*365)).strftime('%Y-%m-%d')
    years_ago_data = fetch_historical_data(stocks, start_date=years_ago, end_date=enddate)
    if not data.empty and not years_ago_data.empty:
        historical_ratio = years_ago_data['XOM'] / years_ago_data['CVX']
        current_values = data.iloc[-1]
        current_ratio = current_values['XOM'] / current_values['CVX']
        advice = get_trading_advice(current_ratio, historical_ratio.mean(),'V', 'MA')
        text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
               f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
               f"{'XOM:':<18} {current_values['XOM']:.2f}\n" \
               f"{'CVX:':<18} {current_values['CVX']:.2f}\n\n" \
               f"Ratio Threshold: {ratio_threshold}\n"\
               f"Trading Advice:\n{advice}"
        
        # Pack the label on the right side of the frame
        label = Label(frame4, text=text, justify='left', font=font, padx=10, pady=10, wraplength=wrap_length)
        label.pack(side='right', anchor='ne')  # Pack on the right side
    
    # Plot on canvas
    canvas = FigureCanvasTkAgg(fig, master=frame4)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("Pairs Trading App")

plot_width, plot_height = 600, 500 # Width and height of each plot in pixels
padding = 0 # Padding between plots and window edges

window_width = 2 * plot_width + 2 * padding
window_height = 2 * plot_height + 3 * padding

root.geometry(f"{window_width}x{window_height}")

frame1 = ttk.Frame(root, padding=padding, relief="sunken", width=plot_width, height=plot_height)
frame1.grid(row=0, column=0, padx=padding, pady=padding)

frame2 = ttk.Frame(root, padding=padding, relief="sunken", width=plot_width, height=plot_height)
frame2.grid(row=0, column=1, padx=padding, pady=padding)

frame3 = ttk.Frame(root, padding=padding, relief="sunken", width=plot_width, height=plot_height)
frame3.grid(row=1, column=0, padx=padding, pady=padding)

frame4 = ttk.Frame(root, padding=padding, relief="sunken", width=plot_width, height=plot_height)
frame4.grid(row=1, column=1, padx=padding, pady=padding)

font = Font(weight='bold')

plot_pair1()
plot_pair2()
plot_pair3()
plot_pair4()
root.title("Pairs Trading Analysis")

root.mainloop()


