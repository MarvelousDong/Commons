from numpy import eye, argwhere, array
from pandas import DataFrame, to_numeric
from pykalman import KalmanFilter


class KalmanFilterGenerate:
    def __init__(self, dim=3):
        self.dim = dim

        self.model = KalmanFilter(
            transition_matrices=self.make_transition_matrix(),
            observation_matrices=self.make_observation_matrix(),
            transition_covariance=self.make_transition_covariance()
        )

        self.filtered_state_means0 = array([0.0 for _ in range(self.dim * 2)])
        self.filtered_state_covariances0 = eye(self.dim * 2)

    def make_transition_matrix(self):
        final_matrix = eye(N=self.dim * 2)

        for row in final_matrix:
            one_index = argwhere(row == 1)[0][0]
            target_index = one_index + self.dim

            try:
                row[target_index] += 1
            except IndexError:
                pass

        return final_matrix

    def make_observation_matrix(self):
        return eye(N=self.dim * 2)[:self.dim]

    def make_transition_covariance(self):
        return 0.03 * eye(N=self.dim * 2)

    def fit_predict(self, data, predict_flag=False):
        final_list = []

        data_index_list = data.index

        for i in data_index_list:
            current_measurement = array(data.loc[i].apply(to_numeric))

            filtered_state_means, filtered_state_covariances = self.model.filter_update(
                filtered_state_mean=self.filtered_state_means0,
                filtered_state_covariance=self.filtered_state_covariances0,
                observation=current_measurement
            )

            if predict_flag:
                target_list = list(filtered_state_means)[:self.dim]
                final_list.append(target_list)

        if predict_flag:
            data_keys_list = data.keys()

            return DataFrame(
                data=final_list,
                columns=data_keys_list
            )
