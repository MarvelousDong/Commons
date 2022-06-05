from settings import BASE_DIR, POLICY_VERIFICATION
from complexity.algorithm import RademacherComplexity
from glob import glob
from pandas import to_numeric, DataFrame, concat
from pyg2plot import Plot

import joblib


class ComplexityEvaluatorExhibitor:
    def __init__(self, data):
        self.data = data.sample(n=5000)

        self.model_dir = BASE_DIR / "statics" / "complexity" / "models"
        self.exhibition_dir = BASE_DIR / "statics" / "exhibition"

    def __call__(self, *args, **kwargs):

        final_list = []
        for policy_dict in POLICY_VERIFICATION:
            title_algorithm = policy_dict["title"]
            title_x = policy_dict["title_x"]
            title_y = policy_dict["title_y"]

            target_string = f"{title_algorithm}-{title_x}-{title_y}" + "*"

            model_filename_list = glob(str(self.model_dir / target_string))

            final_df = DataFrame()
            for file_path in model_filename_list:
                model_dict = joblib.load(filename=file_path)

                model = model_dict["model"]
                policy_string = model_dict["policy_string"]

                data_x = self.data[[title_x]].apply(to_numeric)

                predict_data_y = list(model.predict(data_x))
                predict_y_df = DataFrame(
                    data=predict_data_y,
                    columns=[policy_string]
                )

                final_df = concat([final_df, predict_y_df], axis=1)

            data_y = self.data[[title_y]].apply(to_numeric)

            complex_model = RademacherComplexity()
            complex_model.fit(
                y_origin_data=data_y,
                y_predict_data=final_df
            )

            final_list.append({
                "title_algorithm": title_algorithm,
                "complexity": float("%.4f" % complex_model.complexity) * 1000
            })

        self.draw(final_list=final_list)

    def draw(self, final_list):

        excel_file_path = self.exhibition_dir / "complexity.xlsx"
        html_file_path = self.exhibition_dir / "complexity.html"

        column = Plot("Column")

        column.set_options({
            "height": 450,
            "width": 300,
            "data": final_list,
            "xField": "title_algorithm",
            "yField": "complexity",
        })

        df = DataFrame(data=final_list)
        df.to_excel(
            excel_writer=str(excel_file_path),
            index=False
        )

        column.render(path=str(html_file_path))
