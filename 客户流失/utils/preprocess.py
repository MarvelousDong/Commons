from scipy.stats import iqr
from pandas import to_numeric
from settings import FILLING_COLUMNS


class PreProcess:
    def __init__(self):
        pass

    @staticmethod
    def quartile_filter(series):
        iqr_value = iqr(series)
        low_outlier = series.quantile(0.25) - iqr_value * 1.5
        high_outlier = series.quantile(0.75) + iqr_value * 1.5

        return series[series <= high_outlier][series >= low_outlier]

    @staticmethod
    def float_filter(float_number):
        return float("%.2f" % float_number)

    def mean_filling(self, data):

        mean_filling_columns = [i for i in FILLING_COLUMNS if i["flag"] == "mean"]

        for mean_column_dict in mean_filling_columns:

            mean_column = mean_column_dict["title"]
            method = mean_column_dict["method"]

            effective_series = data[data[mean_column] != "NULL"][mean_column].apply(to_numeric)

            if "positive" in method:
                effective_series = effective_series[effective_series >= 0]

            if "quartile" in method:
                effective_series = self.quartile_filter(
                    series=effective_series
                )

            mean_value = effective_series.mean()

            if "int_float" in method:
                mean_value = float(int(mean_value))
                mean_value = self.float_filter(float_number=mean_value)
            elif "int" in method:
                mean_value = int(mean_value)
            else:
                mean_value = self.float_filter(float_number=mean_value)

            data[mean_column] = data[mean_column].replace({"NULL": str(mean_value)})

        return data
