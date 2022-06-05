import os
import joblib
import shutil

from settings import FILLING_COLUMNS, BASE_DIR
from correlation.algorithm import PearsonCorrelation
from pandas import to_numeric
from itertools import combinations


class CorrelationTrainer:
    def __init__(self, data):
        self.data = data
        self.columns = [i["title"] for i in FILLING_COLUMNS]

    def __call__(self, *args, **kwargs):

        column_pair_combinations = list(combinations(
            iterable=self.columns,
            r=2
        ))

        model_dir = BASE_DIR / "statics" / "correlation" / "models"
        if model_dir.exists():
            shutil.rmtree(str(model_dir))

        model_dir.mkdir()

        for pair in column_pair_combinations:
            x_column = pair[0]
            y_column = pair[1]

            correlator = PearsonCorrelation()
            correlator.fit(
                x_series=self.data[x_column].apply(to_numeric),
                y_series=self.data[y_column].apply(to_numeric)
            )

            model_title = correlator.__class__.__name__

            saving_model_path = model_dir / f"{model_title}-{x_column}-{y_column}.pkl"

            if saving_model_path.exists():
                os.remove(saving_model_path)

            final_dict = {
                "model": correlator,
                "title": model_title,
                "x_column": x_column,
                "y_column": y_column
            }

            joblib.dump(
                value=final_dict,
                filename=saving_model_path
            )
