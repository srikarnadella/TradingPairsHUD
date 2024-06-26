# Pairs Trading HUD
This application uses Python and tkinter to display pairs trading analysis for selected stock pairs using historical data fetched from Yahoo Finance (`yfinance`). It plots the price trends and Relative Strength Index (RSI) for each pair, along with providing trading advice based on current and historical ratios.
Files Key:
* main.py rough bare bones version
* AdditonalTA.py version seen with 4 charts plotted
* userInputedCharts.py version that takes two user inputs and outputs the chart

## Purpose

The purpose of this application is to visualize and analyze pairs trading opportunities between selected stocks. It helps traders identify potential trading signals based on historical price ratios and technical indicators like RSI.

## Components

### Python Script (`PairsTradingApp.py`)

The main script utilizes the following components:

- **tkinter**: Used for creating the graphical user interface (GUI).
- **matplotlib**: Used for plotting the price charts and RSI graphs.
- **pandas**: Used for data manipulation and analysis, particularly for handling historical stock data.
- **yfinance**: Used for fetching historical stock data from Yahoo Finance.
- **datetime**: Used for date calculations and handling.

### Features

- **Pairs Analyzed:**
  - AMZN vs GOOGL
  - V vs MA
  - AAPL vs MSFT
  - XOM vs CVX

- **Displayed Information:**
  - Price history and RSI over time.
  - Current and historical price ratios.
  - Trading advice based on the current ratio compared to historical data.
 
## Output of code
This is what the HUD looks like. It has 4 trading pairs, their historical ratio (variable can be changed in the file currently sent to 1 year), their values, their current ratios, and their RSI.

### AdditionalTA.py HUD image
![Alt Text](HUDImage.jpg)
### userInputedCharts.py HUD Image
![Alt Text](uesrInputedHud.jpg)
