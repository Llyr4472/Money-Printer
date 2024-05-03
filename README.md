[![GitHub stars](https://img.shields.io/github/stars/LLyr4472/money-printer.svg?style=flat-square)](https://github.com/LLyr4472/money-printer/stargazers)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python version](https://img.shields.io/badge/Python-3.11.1-blue.svg?style=flat-square)](https://www.python.org/downloads/)
[![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg?style=flat-square)](https://github.com/LLyr4472/money-printer/issues)


## Money-Printer [Beta]

How it works (or is supposed to work):
* Get nepse data
* Generate money making signals
* Make money


### Getting Started

1. **Installation:** Install the required libraries using pip:
    1. Download  or clone this repository onto your local machine.
        ```bash
        git clone https://www.github.com/llyr4472/money-printer 
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

* `src\Stocks.py`: Defines Stock() object and handles data acquisition.
* `src\signals.py`: Calculates technical indicators and generates buy/sell signals.
* `src\stocks_data.py`: Filters tradable stocks and creates the `data\stocks.json` file.
* `src\bot.py`: Simulates trading and generates signals based on predefined parameters.
* `src\backtest.py`: Conducts backtesting of trading strategies against historical data.
* `src\stocks_data.py`: Add new feature to data "trade".


## To-Do

- **Improve Signal Generation:** Current signals reliability 0% .
- **Host the Bot:** Put it up and running somewhere
- **Add more Indicators** : More signals if i somehow am able to integrate it with current signal logic.
- **Notifications**: Tweets or discord bot.
- **AI**: Maybe someday, if possible, train a bot using RL or sth. 

### Disclaimer

This project is for educational and experimental purposes only. It should not be considered financial advice, and using it for actual trading could result in financial losses. Always conduct your own research and consult with a qualified financial advisor before making any investment decisions.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contact

For questions or inquiries about the Money-Printer project, please contact [Discord](https://discord.gg/MaCaJCN7).

### Acknowledgments

Special thanks to the creators and maintainers of the libraries and resources used in this project, including Pandas, Requests, and Pandas TA.
