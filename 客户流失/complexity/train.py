from complexity.algorithm import RademacherComplexity
from settings import BASE_DIR, POLICY_VERIFICATION
from itertools import product
from utils.find_all import find_class_obj_in_sklearn
from pandas import to_numeric
from hashlib import md5

import joblib
import os


class ComplexityTrainer:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_model_list():
        model_list = [
            {"model": RademacherComplexity()}
        ]

        return model_list

    @staticmethod
    def reformat_policy_dict(policy_dict):
        keys_list = list(policy_dict.keys())

        product_list = product(
            *policy_dict.values()
        )

        final_list = [
            {keys_list[i]: each[i] for i in range(len(each))}
            for each in product_list
        ]

        return final_list

    @staticmethod
    def md5_encode(target_dict):
        md5_obj = md5()
        md5_obj.update(str(target_dict).encode())
        return md5_obj.hexdigest()

    def __call__(self, *args, **kwargs):
        for policy_dict in POLICY_VERIFICATION:

            title_algorithm = policy_dict["title"]
            title_x = policy_dict["title_x"]
            title_y = policy_dict["title_y"]
            policy_origin = policy_dict["policy"]

            policy_list = self.reformat_policy_dict(policy_dict=policy_origin)
            algorithm_class = find_class_obj_in_sklearn(target_string=title_algorithm)

            x_data = self.data[[title_x]].apply(to_numeric)
            y_data = self.data[[title_y]].apply(to_numeric)

            for each in policy_list:
                model = algorithm_class(**each)
                model.fit(X=x_data, y=y_data)

                md5_string = self.md5_encode(target_dict=each)

                model_dir = BASE_DIR / "statics" / "complexity" / "models"
                saving_path = model_dir / f"{title_algorithm}-{title_x}-{title_y}-{md5_string}.pkl"

                if saving_path.exists():
                    os.remove(saving_path)

                final_dict = {
                    "model": model,
                    "title": title_algorithm,
                    "title_x": title_x,
                    "title_y": title_y,
                    "policy_string": md5_string,
                    "policy": each
                }

                joblib.dump(
                    value=final_dict,
                    filename=saving_path
                )
