# Artemis

Artemis is an algorithmic trading project designed to execute trades using the Alpaca API. It's divided into several modules, each serving a specific function in the trading process.

## Modules

### Trader
The 'Trader' module manages API calls to Alpaca, facilitating the execution of trades and handling interactions with the Alpaca API.

### Manager
The 'Manager' module oversees different strategy submodules that can be interchanged. Currently, it employs the Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD) crossover strategies. These strategies can be easily swapped in and out for testing and implementation.

### Researcher
The 'Researcher' module is responsible for gathering and processing data from Yahoo Finance. It acquires and preprocesses the necessary data for the trading strategies employed by the Manager.

### Backtesting
The 'Backtesting' module creates a simulation environment loaded with specific data from a given ticker. It tests the strategies in real-time and has the capability to process roughly 3000 data points for performance analysis and profit analytics in approximately 1.5 seconds.

## Usage

To use Artemis, follow these steps:
1. Ensure Alpaca API keys are set up and configured.
2. Explore the 'Trader' module to understand and execute trades.
3. Experiment with different strategies in the 'Manager' module.
4. Leverage the 'Researcher' module to gather and preprocess data.
5. Utilize the 'Backtesting' module to simulate and analyze strategy performance.

## Installation

To install Artemis and its dependencies, run 
>pip install requirements.txt
We recommend doing so in a virtual environment, though this is not necessary.

## Contributors

- [Jeffrey Drew](https://github.com/jeffreydrew)
- [Michael](https://github.com/vsaucebrownie)

## Support

For any questions or concerns, feel free to contact [liangjdrew@gmail.com].


## Contributing Conventions:
1. for importing local modules in other folders:

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from folder.subfolder.file import *

#Do not have driver code in the file, otherwise don't import *, only classes and functions you need

2. for sqlite3 database connections:

conn = sqlite3.connect('database.db')
c = conn.cursor()

3. Keep everything modular

4. Generally do not have any driver code inside def files; name driver files <foldername>_core.py

5. Use the following format for driver code:
if __name__ == "__main__":
    #driver code
