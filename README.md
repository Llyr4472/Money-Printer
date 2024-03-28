[![Discord](https://img.shields.io/discord/1221415701353594940?color=7289DA&label=Discord&logo=discord&logoColor=white&style=flat-square)](https://discord.gg/MaCaJCN7)
[![GitHub stars](https://img.shields.io/github/stars/LLyr4472/nepse-trading-bot.svg?style=flat-square)](https://github.com/LLyr4472/nepse-trading-bot/stargazers)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python version](https://img.shields.io/badge/Python-3.11.1-blue.svg?style=flat-square)](https://www.python.org/downloads/)
[![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg?style=flat-square)](https://github.com/LLyr4472/nepse-trading-bot/issues)
[![GitHub issues](https://img.shields.io/github/issues/LLyr4472/nepse-trading-bot.svg?style=flat-square)](https://github.com/LLyr4472/nepse-trading-bot/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/LLyr4472/nepse-trading-bot.svg?style=flat-square)](https://github.com/LLyr4472/nepse-trading-bot/pulls)


## Nepse Trading Bot [Beta]

This project provides a foundational framework for developing a trading bot for the Nepse stock exchange in Nepal. It offers functionalities to fetch and process stock data, calculate technical indicators, generate buy/sell signals, and conduct backtesting and simulation of trading strategies.


### Features

* **Data Acquisition:**
    * Fetches stock data from the [API](https://the-value-crew.github.io/nepse-api) .
    * Provides functionalities to filter tradable stocks based on user-defined criteria.
    * Handles data retrieval for a specified date range.

* **Signal Generation:**
    * Calculates various technical indicators for tradable stocks
    * Combines the calculated technical indicators into a single buy/sell signal.
    * Allows customization of signal generation logic.
    * Signals are normalized between -1 and 1 for ease of interpretation.

* **Backtesting and Simulation:**
    * Enables users to backtest trading strategies against historical data.
    * Simulates trading activities to evaluate strategy performance.
    * Provides insights into potential profit/loss and risk metrics.

### Getting Started

1. **Installation:** Install the required libraries using pip:
    1. Download  or clone this repository onto your local machine.
        ```bash
        git clone https://www.github.com/llyr4472/nepse-trading-bot 
        ```
    2. Open terminal, navigate to project.
    3. Run following in terminal to install dependencies.
        ```bash
        pip install -r requirements.txt
        ```

2. **Configuration (Optional):**
    - Adjust filtering criteria in `stocks_json.py` to define tradable stocks.

3. **Data Preparation (Optional):**
    - Run `stocks_json.py` to generate the `stocks.json` file containing filtered company data.

4. **Customization (Optional):**
    - Explore and customize the logic in `signals.py` to adjust signal generation parameters.

5. **Running the Bot:**
    - Use `bot.py` to simulate trading and generate buy/sell signals.


### Code Structure

The project consists of the following core Python files:

* `Stocks.py`: Defines Stock() object and handles data acquisition.
* `signals.py`: Calculates technical indicators and generates buy/sell signals.
* `stocks_json.py`: Filters tradable stocks and creates the `stocks.json` file.
* `bot.py`: Simulates trading and generates signals based on predefined parameters.
* `backtest.py`: Conducts backtesting of trading strategies against historical data.

## To-Do

- **Improve Signal Generation:** Enhance the signal generation logic to increase accuracy and reliability.
- **Host the Bot:** Explore options for hosting the trading bot to enable continuous monitoring and automated trading.
- **Add more Indicators** : Implement additional technical analysis indicators to enhance signal quality.
- **Notifications**: Notify  users via discord channels when buying/selling  signals are generated.


### Contributing

Contributions to the Nepse Trading Bot project are welcome! If you have suggestions for improvements or new features, feel free to submit a pull request or open an issue on GitHub.

### Disclaimer

This project is for educational and experimental purposes only. It should not be considered financial advice, and using it for actual trading could result in financial losses. Always conduct your own research and consult with a qualified financial advisor before making any investment decisions.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Acknowledgments

Special thanks to the creators and maintainers of the libraries and resources used in this project, including Pandas, Requests, and Pandas TA.
