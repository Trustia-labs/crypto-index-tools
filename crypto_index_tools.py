import requests
from binance.client import Client
from PyInquirer import prompt
import pandas as pd

def format_market_cap(market_cap):
    if market_cap >= 1e9:
        return f'{market_cap / 1e9:.2f}B'
    elif market_cap >= 1e6:
        return f'{market_cap / 1e6:.2f}M'
    elif market_cap >= 1e3:
        return f'{market_cap / 1e3:.2f}K'
    else:
        return f'{market_cap:.2f}'

def calculate_portfolio_percentages(products, weighting_distribution):
    if weighting_distribution == 'Equal':
        equal_weight = 1 / len(products)
        return [equal_weight] * len(products)
    else:  # Market cap based
        total_market_cap = sum(product['market_cap'] for product in products)
        return [product['market_cap'] / total_market_cap for product in products]


client = Client()

# Fetch products from Binance API
products = client.get_products()

# Extract tags from products
tags = set()
for product in products['data']:
    for tag in product['tags']:
        tags.add(tag)

# Prompt user to select multiple tags
tags = sorted(tags)
questions = [
    {
        'type': 'checkbox',
        'name': 'selected_tags',
        'message': 'Select tags to include',
        'choices': [{'name': tag} for tag in tags],
    },
    {
        'type': 'checkbox',
        'name': 'excluded_tags',
        'message': 'Select tags to exclude',
        'choices': [{'name': tag} for tag in tags],
    }
]

answers = prompt(questions)
selected_tags = answers['selected_tags']
excluded_tags = answers['excluded_tags']

# Filter products by the selected and excluded tags
filtered_products = [
    product for product in products['data']
    if any(tag in product['tags'] for tag in selected_tags)
    and not any(tag in product['tags'] for tag in excluded_tags)
    and 'USDT' in product['q']
]
# Show the user the list of filtered products and let them unselect the ones they don't want
questions = [
    {
        'type': 'checkbox',
        'name': 'selected_products',
        'message': 'Select the products you want to include',
        'choices': [{'name': f"{product['s']}", 'checked': True} for product in filtered_products],
    }
]

answers = prompt(questions)
selected_products_symbols = set(answers['selected_products'])
filtered_products = [product for product in filtered_products if product['s'] in selected_products_symbols]


# Calculate market cap for each product
for product in filtered_products:
    cs = float(product['cs']) if product['cs'] is not None else 0
    c = float(product['c']) if product['c'] is not None else 0
    product['market_cap'] = cs * c

# Prompt user to select the number of top products to display
questions = [
    {
        'type': 'input',
        'name': 'top_x',
        'message': 'Enter the number of top products to display:',
        'validate': lambda val: val.isdigit() and int(val) > 0 or 'Please enter a positive integer',
        'filter': lambda val: int(val)
    }
]

top_x = prompt(questions)['top_x']


# Add a question to ask the user about the desired weighting distribution
questions = [
    {
        'type': 'list',
        'name': 'weighting_distribution',
        'message': 'Choose the weighting distribution for your portfolio:',
        'choices': ['Equal', 'Market cap based'],
    }
]

answers = prompt(questions)
weighting_distribution = answers['weighting_distribution']


# Sort filtered products by market cap and select the top x
sorted_filtered_products = sorted(filtered_products, key=lambda x: x['market_cap'], reverse=True)[:top_x]
portfolio_percentages = calculate_portfolio_percentages(sorted_filtered_products, weighting_distribution)

# Display top x filtered products as a table
df = pd.DataFrame(sorted_filtered_products)
df['market_cap'] = df['market_cap'].apply(format_market_cap)
df = df[['s', 'b', 'q', 'tags', 'market_cap']]
df.columns = ['symbol', 'baseAsset', 'quoteAsset', 'tags', 'market_cap']


print(df)


#
