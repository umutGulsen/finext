import requests
import os
from evds import evdsAPI
import pandas as pd


evds_api_key = os.environ.get('EVDS_API')


def read_evds_data(series_code):

    evds = evdsAPI(os.environ.get("EVDS_API"))
    data = evds.get_data([series_code], startdate="01-01-2020", enddate="01-10-3024")
    return data


def write_evds_data(df, filename):
    df.to_csv(filename, index=False, sep=";")


def main():
    pass


if __name__ == '__main__':
    main()
