from pandas import DataFrame


class RademacherComplexity:
    def __init__(self):
        self.epsilon_list = [0.1, 0.5, 0.8, 1, 1.2, 1.5, 2]
        self.complexity = 0

    def fit(self, y_origin_data, y_predict_data):
        y_origin_key = y_origin_data.keys()[0]
        y_predict_keys = y_predict_data.keys()

        total_list = []

        for epsilon in self.epsilon_list:
            compute_list = []
            new_df = DataFrame()

            for y_predict_key in y_predict_keys:
                new_df[f"{epsilon}"] = abs(y_origin_data[y_origin_key] - y_predict_data[y_predict_key]) > epsilon
                compute_list.append(len(new_df[new_df[f"{epsilon}"]]) / len(new_df[f"{epsilon}"]))

            total_list.append(max(compute_list))

        self.complexity = sum(total_list) / len(total_list)
