from pandas import DataFrame


class PearsonCorrelation:
    def __init__(self):
        self.correlation_number = 0

    @staticmethod
    def func_ab(a, b):
        return a * b

    def fit(self, x_series, y_series):
        x_series = x_series - x_series.mean()
        y_series = y_series - y_series.mean()

        new_df = DataFrame(list(zip(x_series, y_series)), columns=["x", "y"])

        target_xy = new_df.apply(
            func=lambda column: self.func_ab(
                a=column["x"],
                b=column["y"]
            ),
            axis=1
        )

        target_xx = new_df.apply(
            lambda column: self.func_ab(
                a=column["x"],
                b=column["x"]
            ),
            axis=1
        )

        target_yy = new_df.apply(
            lambda column: self.func_ab(
                a=column["y"],
                b=column["y"]
            ),
            axis=1
        )

        self.correlation_number = target_xy.sum() / (target_xx.sum() ** 0.5 * target_yy.sum() ** 0.5)

    def __str__(self):
        return "PearsonCorrelation"
