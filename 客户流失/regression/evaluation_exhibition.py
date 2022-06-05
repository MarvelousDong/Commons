from settings import BASE_DIR
from pandas import DataFrame, to_numeric
from pyg2plot import Plot

import joblib


class RegressionEvaluatorExhibitor:
    def __init__(self, data):
        self.model_dir = BASE_DIR / "statics" / "regression" / "models"
        self.exhibition_dir = BASE_DIR / "statics" / "exhibition"

        self.point_count = 500
        self.data = data

    def make_base_data(self, column_dict, model_type="supervised"):
        title_x, title_y = column_dict.values()

        if model_type == "supervised":
            max_x = self.data[title_x].apply(to_numeric).max()
            min_x = self.data[title_x].apply(to_numeric).min()

            block = (max_x - min_x) / self.point_count
            target_list = [min_x + block * i for i in range(self.point_count)]
            target_list = [float("%.2f" % i) for i in target_list]

            final_df = DataFrame(
                data=target_list,
                columns=[title_x]
            )

        else:
            column_df = self.data[[title_x, title_y]].apply(to_numeric)
            final_df = column_df.sample(n=self.point_count)

        return final_df

    def __call__(self, *args, **kwargs):

        for file_path in self.model_dir.iterdir():

            model_dict = joblib.load(str(file_path))

            model = model_dict["model"]
            algorithm_title = model_dict["title"]
            title_x = model_dict["title_x"]
            title_y = model_dict["title_y"]
            model_type = model_dict["model_type"]

            base_data = self.make_base_data(
                column_dict={
                    "title_x": title_x,
                    "title_y": title_y
                },
                model_type=model_type
            )

            if model_type == "supervised":
                predict_list = list(model.predict(base_data))
                predict_list = [float("%.2f" % i) for i in predict_list]

                predict_y_df = DataFrame(
                    data=predict_list,
                    columns=[title_y]
                )

                self.draw(
                    algorithm_title=algorithm_title,
                    base_x_df=base_data,
                    predict_y_df=predict_y_df,
                )
            else:

                predict_df = model.fit_predict(
                    data=base_data,
                    predict_flag=True
                ).applymap(lambda x: '%.2f' % x)

                self.draw(
                    algorithm_title=algorithm_title,
                    predict_df=predict_df
                )

    def draw(self, algorithm_title, base_x_df=None, predict_y_df=None, predict_df=None):

        bar = Plot('Line')

        if predict_df is None:
            title_x = list(base_x_df.keys())[0]
            title_y = list(predict_y_df.keys())[0]

            assert len(base_x_df) == len(predict_y_df)

            x_index = base_x_df.index
            y_index = predict_y_df.index

            data = [
                {
                    title_x: base_x_df[title_x][x_index[i]],
                    title_y: predict_y_df[title_y][y_index[i]]
                }
                for i in range(len(x_index))
            ]

        else:
            title_x, title_y = predict_df.keys()

            index_list = predict_df.index

            data = [
                {
                    title_x: predict_df[title_x][index_list[i]],
                    title_y: predict_df[title_y][index_list[i]]
                }
                for i in range(len(predict_df))
            ]

        data = sorted(data, key=lambda x: x[title_x])

        option_dict = {
            "appendPadding": 32,
            "data": data,
            "xField": title_x,
            "yField": title_y,
        }

        bar.set_options(options=option_dict)

        saving_path = self.exhibition_dir / f"{algorithm_title}-{title_x}-{title_y}.html"
        bar.render(path=str(saving_path))
