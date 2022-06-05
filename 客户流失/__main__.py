from warnings import filterwarnings
from settings import TOTAL_CONTROLLER
from utils.data import DataLoader
from utils.preprocess import PreProcess
from utils.find_all import find_local_model

import sys


class Entrance:
    def __init__(self):
        self.dataloader = DataLoader()
        self.preprocessor = PreProcess()
        self.this_model = sys.modules[__name__]

    @staticmethod
    def reformat_controller_dict():
        final_dict = {}
        for key, value in TOTAL_CONTROLLER.items():
            for sub_key, sub_bool in value.items():

                if "_" in sub_key:
                    target_list = [i.title() for i in sub_key.split("_")]
                    class_title = key.title() + "".join(target_list)
                else:
                    class_title = key.title() + sub_key.title()

                final_dict[class_title] = sub_bool

        return final_dict

    def __call__(self, *args, **kwargs):
        filterwarnings(action="ignore")

        # origin_data = self.dataloader.read_sql_data()
        origin_data = self.dataloader.read_txt_data()
        preprocess_data = self.preprocessor.mean_filling(data=origin_data)

        controller_reformat_dict = self.reformat_controller_dict()

        for class_title, switch in controller_reformat_dict.items():

            if switch:
                try:
                    find_local_model(target_string=class_title)(data=preprocess_data)()
                except TypeError:
                    find_local_model(target_string=class_title)()()


if __name__ == '__main__':
    entrance = Entrance()
    entrance()
