[![GitHub stars](https://img.shields.io/github/stars/LLyr4472/nepse-wizard.svg?style=flat-square)](https://github.com/LLyr4472/nepse-wizard/stargazers)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python version](https://img.shields.io/badge/Python-3.11.1-blue.svg?style=flat-square)](https://www.python.org/downloads/)
[![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg?style=flat-square)](https://github.com/LLyr4472/nepse-wizard/issues)


## Nepse Wizard [Beta]

How it works (or is supposed to work):
* Get nepse data
* Generate magical signals
* Backtest & simulate the strategy


### Getting Started

1. **Installation:** Install the required libraries using pip:
    1. Download  or clone this repository onto your local machine.
        
        git clone https://www.github.com/llyr4472/nepse-wizard 
        
    2. Open the terminal, and navigate to the project.
    3. Run the following in the terminal to install dependencies.
        
        pip install -r requirements.txt
        

2. **Configuration (Optional):**
    - Adjust filtering criteria in `stocks_data.py` to define tradable stocks.

3. **Data Preparation (Optional):**
    - Run `stocks_data.py` to generate the `stocks.json` file containing filtered company data.

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
* `src\csv_writer.py`: Gets data from api and writes them into csv.


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

For questions or inquiries about the Nepse Wizard project, please contact [Discord](https://discord.gg/Xn4erZuZ).

### Acknowledgments

Special thanks to the creators and maintainers of the libraries used in this project, including Pandas, Requests, and Pandas TA.