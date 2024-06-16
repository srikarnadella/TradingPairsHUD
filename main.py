import tkinter as tk
from tkinter import ttk
from tkinter import Label, Text
from tkinter.font import Font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf  # Using yfinance for fetching historical stock data

# Global variable for figure size
figsize = (6, 5)  # Change this to adjust the size of all charts uniformly

# Function to fetch historical data and plot for pair 1: AMZN vs GOOGL
def plot_pair1():
    # Fetch historical data for AMZN and GOOGL
    stocks = ['AMZN', 'GOOGL']
    data = yf.download(stocks, start='2020-01-01', end='2023-01-01')['Adj Close']
    
    fig = Figure(figsize=figsize, dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    data.plot(ax=plot)
    plot.set_title('AMZN vs GOOGL')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')

    # Calculate historical trading ratio and current values
    historical_ratio = data['AMZN'] / data['GOOGL']
    current_values = data.iloc[-1]
    current_ratio = current_values['AMZN'] / current_values['GOOGL']
    
    # Display historical ratio, current values, and current ratio in a formatted text box
    text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
           f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
           f"{'AMZN:':<18} {current_values['AMZN']:.2f}\n" \
           f"{'GOOGL:':<18} {current_values['GOOGL']:.2f}"
    
    label = Label(frame1, text=text, justify='left', font=font, padx=10, pady=10)
    label.pack(side='left', anchor='nw')

    canvas = FigureCanvasTkAgg(fig, master=frame1)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to fetch historical data and plot for pair 2: V vs MA
def plot_pair2():
    # Fetch historical data for V and MA
    stocks = ['V', 'MA']
    data = yf.download(stocks, start='2020-01-01', end='2023-01-01')['Adj Close']
    
    fig = Figure(figsize=figsize, dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    data.plot(ax=plot)
    plot.set_title('V vs MA')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')

    # Calculate historical trading ratio and current values
    historical_ratio = data['V'] / data['MA']
    current_values = data.iloc[-1]
    current_ratio = current_values['V'] / current_values['MA']
    
    # Display historical ratio, current values, and current ratio in a formatted text box
    text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
           f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
           f"{'V:':<18} {current_values['V']:.2f}\n" \
           f"{'MA:':<18} {current_values['MA']:.2f}"
    
    label = Label(frame2, text=text, justify='left', font=font, padx=10, pady=10)
    label.pack(side='left', anchor='nw')

    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to fetch historical data and plot for pair 3: AAPL vs MSFT
def plot_pair3():
    # Fetch historical data for AAPL and MSFT
    stocks = ['AAPL', 'MSFT']
    data = yf.download(stocks, start='2020-01-01', end='2023-01-01')['Adj Close']
    
    fig = Figure(figsize=figsize, dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    data.plot(ax=plot)
    plot.set_title('AAPL vs MSFT')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')

    # Calculate historical trading ratio and current values
    historical_ratio = data['AAPL'] / data['MSFT']
    current_values = data.iloc[-1]
    current_ratio = current_values['AAPL'] / current_values['MSFT']
    
    # Display historical ratio, current values, and current ratio in a formatted text box
    text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
           f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
           f"{'AAPL:':<18} {current_values['AAPL']:.2f}\n" \
           f"{'MSFT:':<18} {current_values['MSFT']:.2f}"
    
    label = Label(frame3, text=text, justify='left', font=font, padx=10, pady=10)
    label.pack(side='left', anchor='nw')

    canvas = FigureCanvasTkAgg(fig, master=frame3)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to fetch historical data and plot for pair 4: XOM vs CVX
def plot_pair4():
    # Fetch historical data for XOM and CVX
    stocks = ['XOM', 'CVX']
    data = yf.download(stocks, start='2020-01-01', end='2023-01-01')['Adj Close']
    
    fig = Figure(figsize=figsize, dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    data.plot(ax=plot)
    plot.set_title('XOM vs CVX')
    plot.set_xlabel('Date')
    plot.set_ylabel('Price')

    # Calculate historical trading ratio and current values
    historical_ratio = data['XOM'] / data['CVX']
    current_values = data.iloc[-1]
    current_ratio = current_values['XOM'] / current_values['CVX']
    
    # Display historical ratio, current values, and current ratio in a formatted text box
    text = f"{'Historical Ratio:':<18} {historical_ratio.mean():.2f}\n" \
           f"{'Current Ratio:':<18} {current_ratio:.2f}\n\n" \
           f"{'XOM:':<18} {current_values['XOM']:.2f}\n" \
           f"{'CVX:':<18} {current_values['CVX']:.2f}"
    
    label = Label(frame4, text=text, justify='left', font=font, padx=10, pady=10)
    label.pack(side='left', anchor='nw')

    canvas = FigureCanvasTkAgg(fig, master=frame4)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create main application window
root = tk.Tk()
root.title("Pairs Trading App")

# Calculate total window size based on plot sizes and padding
plot_width, plot_height = 600, 500  # Width and height of each plot in pixels
padding = 20  # Padding between plots and window edges

# Calculate window size based on plot dimensions and padding
window_width = 2 * plot_width + 3 * padding
window_height = 2 * plot_height + 3 * padding

# Set the window size and position
root.geometry(f"{window_width}x{window_height}")

# Create frames for each pair
frame1 = ttk.Frame(root, padding=padding, relief="sunken", width=plot_width, height=plot_height)
frame1.grid(row=0, column=0, padx=padding, pady=padding)

frame2 = ttk.Frame(root, padding=padding, relief="sunken", width=plot_width, height=plot_height)
frame2.grid(row=0, column=1, padx=padding, pady=padding)

frame3 = ttk.Frame(root, padding=padding, relief="sunken", width=plot_width, height=plot_height)
frame3.grid(row=1, column=0, padx=padding, pady=padding)

frame4 = ttk.Frame(root, padding=padding, relief="sunken", width=plot_width, height=plot_height)
frame4.grid(row=1, column=1, padx=padding, pady=padding)

# Define a bold font
font = Font(weight='bold')

# Call plotting functions to fetch data and display plots in each frame
plot_pair1()
plot_pair2()
plot_pair3()
plot_pair4()

# Run the main event loop
root.mainloop()
