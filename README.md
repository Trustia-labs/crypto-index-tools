# Crypto Index Tools

Crypto Index Tools is a Python script that helps you build a customized cryptocurrency portfolio based on user preferences. It retrieves a list of cryptocurrency trading pairs from the Binance API, filters them based on the user's selected and excluded tags, and calculates the portfolio percentages based on the desired weighting distribution.

## Features

- Fetches trading pairs from Binance API
- Filters trading pairs based on user-selected and excluded tags
- Allows the user to deselect products they don't want to include
- Allows the user to select the number of top products to display
- Calculates the portfolio percentages based on the desired weighting distribution (equal or market cap based)
- Displays the selected products as a table with columns: symbol, baseAsset, quoteAsset, tags, and market cap

## Requirements

- Python 3.6+
- Packages: requests, binance-client, PyInquirer, pandas

To install the required packages, run:

```sh
pip install requests binance-client PyInquirer pandas
```

## Usage

1. Clone the repository or download the `crypto_index_tools.py` script.

2. Open your terminal or command prompt, navigate to the directory where the script is located, and run:

```sh
python crypto_index_tools.py
```

3. Follow the prompts to select tags to include, tags to exclude, and the number of top products to display.

4. The script will show you a list of filtered products. You can deselect any products you don't want to include in your portfolio.

5. Select the desired weighting distribution for your portfolio (equal or market cap based).

6. The script will display a table with the selected products, their market caps, and their portfolio percentages based on the chosen weighting distribution.

## Customization

You can modify the script to change the filters or calculations used to build the portfolio. Additionally, you can integrate other APIs or data sources to enrich the information displayed in the table or implement different weighting schemes for your portfolio.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
