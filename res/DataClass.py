import pandas as pd


class Data:

    @staticmethod
    def get_data(source):

        return pd.read_csv(source)
