from glob import glob
from settings import  BASE_DIR, FILLING_COLUMNS
from itertools import combinations
from correlation.algorithm import PearsonCorrelation
from pyg2plot import Plot

import joblib


class CorrelationEvaluatorExhibitor:
    def __init__(self):
        self.model_dir = BASE_DIR / "statics" / "correlation" / "models"
        self.columns = [i["title"] for i in FILLING_COLUMNS]

        self.exhibition_flag = True

    def __call__(self, *args, **kwargs):
        algorithm_title = PearsonCorrelation().__class__.__name__

        pair_list = list(combinations(
            iterable=self.columns,
            r=2
        ))

        final_score_list = []
        for pair in pair_list:
            column1 = pair[0]
            column2 = pair[1]

            try:
                model_file_path = glob(
                    pathname=str(self.model_dir / f"{algorithm_title}-{column1}-{column2}.pkl")
                )[0]
            except IndexError:
                model_file_path = glob(
                    pathname=str(self.model_dir / f"{algorithm_title}-{column2}-{column1}.pkl")
                )[0]

            model_dict = joblib.load(filename=model_file_path)

            score_dict = {
                "correlation_score": abs(model_dict["model"].correlation_number),  # 预测
                "title": model_dict["title"],  # 算法标题
                "x_column": model_dict["x_column"],  # 横坐标字段名称
                "y_column": model_dict["y_column"]  # 纵坐标字段名称
            }

            final_score_list.append(score_dict)

        if self.exhibition_flag:
            self.chordal_graph(data_list=final_score_list)

    @staticmethod
    def chordal_graph(data_list):
        chord = Plot("Chord")

        chord.set_options(
            options={
                "height": 400,
                "data": data_list,
                'sourceField': 'x_column',
                'targetField': 'y_column',
                'weightField': 'correlation_score',
                'theme': {
                    'colors10': [
                        '#FF6B3B', '#626681', '#FFC100', '#9FB40F',
                        '#76523B', '#DAD5B5', '#0E8E89', '#E19348',
                        '#F383A2', '#247FEA'
                    ]
                }
            }
        )

        saving_path = BASE_DIR / "statics" / "exhibition" / "correlation.html"
        chord.render(path=str(saving_path))
