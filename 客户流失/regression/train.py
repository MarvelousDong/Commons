from pandas import to_numeric
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.linear_model import ARDRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor

from regression.algorithm import KalmanFilterGenerate
from settings import REGRESSION_COLUMNS, BASE_DIR

import os
import joblib


class RegressionTrainer:
    def __init__(self, data):
        self.data = data
        self.random_state = 5

    def get_model_list(self):
        model_list = [
            {
                "model": DecisionTreeRegressor(random_state=self.random_state),
                "type": "supervised"
            },  # 决策树回归
            {
                "model": ARDRegression(),
                "type": "supervised"
            },  # 随机梯度下降
            {
                "model": RandomForestRegressor(random_state=self.random_state),
                "type": "supervised"
            },  # 随机森林回归
            {
                "model": AdaBoostRegressor(random_state=self.random_state),
                "type": "supervised"
            },  # adaboost（森林模型）
            {
                "model": make_pipeline(
                    PolynomialFeatures(2),
                    LinearRegression()
                ),
                "title": f"PolyNormalRegressor_rank2",
                "type": "supervised"
            },  # 二次多项式回归
            {
                "model": KalmanFilterGenerate(dim=2),
                "type": "unsupervised"
            },  # 卡尔曼滤波（维度可扩展）拟合
        ]

        return model_list

    def __call__(self, *args, **kwargs):
        for regression_pair in REGRESSION_COLUMNS:
            target_data = self.data[list(regression_pair.values())].apply(to_numeric)
            train_data, test_data = train_test_split(target_data, test_size=0.1)

            for model_dict in self.get_model_list():

                model_type = model_dict["type"]
                algorithm_model = model_dict["model"]

                if model_type == "supervised":
                    data_x = train_data[[regression_pair["title_x"]]]
                    data_y = train_data[[regression_pair["title_y"]]]
                    algorithm_model.fit(X=data_x, y=data_y)

                else:
                    algorithm_model.fit_predict(data=train_data)

                model_dir = BASE_DIR / "statics" / "regression" / "models"

                title_x = regression_pair["title_x"]
                title_y = regression_pair["title_y"]
                title_algorithm = model_dict["title"] if "title" in model_dict else algorithm_model.__class__.__name__

                saving_path = model_dir / f"{title_algorithm}-{title_x}-{title_y}.pkl"

                if saving_path.exists():
                    os.remove(saving_path)

                final_dict = {
                    "model": algorithm_model,
                    "title": title_algorithm,
                    "title_x": title_x,
                    "title_y": title_y,
                    "model_type": model_type
                }

                joblib.dump(
                    value=final_dict,
                    filename=saving_path
                )
