import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np
import os

def fit_trendline(year_timestamps, data):
    """Fits a trendline to the given data using linear regression.

    Args:
        year_timestamps (list): A list of year timestamps.
        data (list): A list of data points.

    Returns:
        tuple: A tuple containing the slope and R-squared value of the trendline.
    """
    if len(year_timestamps) != len(data):
        raise ValueError("タイムスタンプとデータの長さが一致していません。")
    result = linregress(year_timestamps, data)
    slope = round(result.slope, 3)
    r_squared = round(result.rvalue**2, 3)
    intercept = round(result.intercept,3)
    return slope, r_squared, intercept


def process_sdg_data(input_excel_file, columns_to_drop):
    """Process SDG data from an input Excel file downloaded from the SDG website.

    Args:
        input_excel_file (str): The path to the input Excel file.
        columns_to_drop (list): A list of column names to drop from the DataFrame.

    Returns:
        pandas DataFrame: The processed DataFrame with dropped columns and transposed index.
    """

    if not os.path.exists(input_excel_file):
        raise FileNotFoundError(f"ファイルが見つかりません: {input_excel_file}")

    df = pd.read_excel(input_excel_file)
    df = df.drop(columns_to_drop, axis=1)
    df = df.set_index("GeoAreaName").transpose()
    return df

def extract_country_data(df, country_name):
    if country_name not in df.columns:
        raise KeyError(f"指定された国名 '{country_name}' はデータに存在しません。")
    if df[country_name].isnull().all():
        raise ValueError(f"{country_name} のデータがすべて欠損しています。")
    
    timestamps = [int(i) for i in df.index.tolist()]
    country_data = df[country_name].tolist()
    return timestamps, country_data

def country_trendline(country_name):
    """Calculate the slope and R-squared value of the trendline for a given country.

    Args:
        country_name (str): The name of the country as represented in the SDG database.

    Returns:
        tuple: A tuple containing the slope and R-squared value of the trendline.
    """
    df = process_sdg_data(
        "SG_GEN_PARL.xlsx",
        [
            "Goal",
            "Target",
            "Indicator",
            "SeriesCode",
            "SeriesDescription",
            "GeoAreaCode",
            "Reporting Type",
            "Sex",
            "Units",
        ],
    )
    
    timestamps, country_data = extract_country_data(df, country_name)
    slope, r_squared, intercept  = fit_trendline(timestamps, country_data)
    return slope, r_squared, intercept

def generate_image(country_name):
    df = process_sdg_data(
        "SG_GEN_PARL.xlsx",
            [
            "Goal",
            "Target",
            "Indicator",
            "SeriesCode",
            "SeriesDescription",
            "GeoAreaCode",
            "Reporting Type",
            "Sex",
            "Units",
            ],
    )

    import matplotlib
    matplotlib.use('Agg')
    plt.clf()

    ## First Graph
    timestamps, country_data = extract_country_data(df, country_name)
    plt.plot(timestamps, country_data, color='blue', label='Data')  

    ## Second Graph
    slope, r_squared, intercept  = fit_trendline(timestamps, country_data)
    x = np.linspace(timestamps[0], timestamps[-1], 100) 
    y = slope * x + intercept
    plt.plot(x, y, label=f'y = {slope}x + {intercept}', color='red')  

    plt.xlabel('year')
    plt.ylabel('percent')
    plt.grid(True)
    plt.title(country_name + ': Data Plot with Linear Regression')
    plt.savefig(country_name+".png", dpi=300, bbox_inches='tight')
    #plt.show()
    return country_name+".png"

#generate_image("India")


