import pandas as pd

def buy_estate(row):
    if (row.price < row.median_price) & (row.condition >= 3):
        buy_estate = 'yes'
    else:
        buy_estate = 'no'

    return buy_estate


def price_sale(row):
    if row.price_buy >= row.season_median:
        sale_price = row.price_buy * 1.1
    else:
        sale_price = row.price_buy * 1.3

    return sale_price


def percentual_sale(row):
    if row.price_buy >= row.season_median:
        percentual = '10%'

    else:
        percentual = '30%'

    return percentual

##### HIPOTESES DE NEGOCIO ####

def mean_feature(feature):  # Calculates the mean of a given feature
    return feature.mean()


def percentual_growth(row):  # Calculates the percentual difference in relation to the mean value
    if row.price > row.price_mean:
        percentual = ((row.price - row.price_mean) / row.price_mean) * 100

    else:
        percentual = ((row.price_mean - row.price) / row.price_mean) * 100

    return percentual


def bigger_smaller_than_avg(
        row):  # Calculates if a given estate has a bigger or smaller price in relation to the mean value
    if row.price > row.price_mean:
        bigger_smaller = 'bigger'
    else:
        bigger_smaller = 'smaller'

    return bigger_smaller


def create_price_mean_col(data):  # Merges column price_mean on the current dataset
    price_mean = data[['zipcode', 'price']].groupby('zipcode').mean().reset_index()
    df = pd.merge(data, price_mean, on='zipcode', how='inner')
    df.rename(columns={"price_x": "price", "price_y": "price_mean"}, inplace=True)

    return df


def waterfront_expensive_col(row,
                             percentage):  # Creates column to indicate if a given estate has a more expensive price (%) than the mean value
    if (row.price >= row.price_mean * ((percentage / 100) + 1)):
        expensive_index = f'more expensive than {percentage}% of the avg'
    else:
        expensive_index = f'less expensive than {percentage}% of the avg'

    return expensive_index


def yrbuilt_expensive_col(row,
                          percentage):  # Creates column to indicate if a given estate with year of construction < 1955 has a cheaper/expensive price than the mean value
    if (row.yr_built < 1955) & (row.price < row.price_mean * (percentage / 100)):
        cheaper_index = f'cheaper than {percentage}%  of avg'
    else:
        cheaper_index = f'{percentage}% more expensive than avg'
    return cheaper_index


def basement_size_col(row, percentage):
    if row.no_basement_sqft_lot > (row.with_basement_sqft_lot * ((percentage / 100) + 1)):
        no_basement_sqft = f'bigger than {percentage} of avg%'
    else:
        no_basement_sqft = f'smaller than {percentage} of avg%'
    return no_basement_sqft