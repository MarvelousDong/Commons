from importlib import import_module
from sklearn import __all__


def find_class_obj_in_sklearn(target_string):

    for script_string in __all__:
        try:
            script = import_module(name=f"sklearn.{script_string}")
        except ModuleNotFoundError:
            continue

        try:
            return getattr(script, target_string)
        except AttributeError:
            continue


def find_local_model(target_string):
    for local_string in ["complexity", "correlation", "regression"]:
        for sub_string in ["train", "evaluation_exhibition"]:
            try:
                script = import_module(name=f"{local_string}.{sub_string}")
            except ModuleNotFoundError:
                continue

            try:
                return getattr(script, target_string)
            except AttributeError:
                continue
