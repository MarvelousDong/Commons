import pathlib

BASE_DIR = pathlib.Path(__file__).parent

MYSQL_CONFIG = {
    "user": "***",
    "password": "***",
    "host": "***",
    "port": 3306,
    "db": "***",
}


FILLING_COLUMNS = [
    {
        "title": "decisionhabit_user",
        "flag": "mean",
        "method": ["quartile", "int_float"]
    },
    {
        "title": "ordercanceledprecent",
        "flag": "mean",
        "method": ["float"]
    },
    {
        "title": "commentnums",
        "flag": "mean",
        "method": ["int"]
    },
    {
        "title": "visitnum_oneyear",
        "flag": "mean",
        "method": ["int"]
    },
    {
        "title": "lastpvgap",
        "flag": "mean",
        "method": ["int"]
    },
    {
        "title": "starprefer",
        "flag": "mean",
        "method": ["float"]
    },
    {
        "title": "landhalfhours",
        "flag": "mean",
        "method": ["int_float", "quartile"]
    },
    {
        "title": "lowestprice_pre2",
        "flag": "mean",
        "method": ["int_float"]
    },
    {
        "title": "cityorders",
        "flag": "mean",
        "method": ["float", "quartile"]
    },
    {
        "title": "cityuvs",
        "flag": "mean",
        "method": ["float", "quartile"]
    }
]

REGRESSION_COLUMNS = [
    {
        "title_x": "starprefer",
        "title_y": "lowestprice_pre2",
    },
    {
        "title_x": "cityorders",
        "title_y": "cityuvs",
    }
]

POLICY_VERIFICATION = [
    {
        "title": "RandomForestRegressor",
        "title_x": "cityorders",
        "title_y": "cityuvs",
        "policy": {
            "random_state": [1, 2, 3, 4, 5],
            "n_estimators": [64, 81, 100]
        }
    },
    {
        "title": "DecisionTreeRegressor",
        "title_x": "cityorders",
        "title_y": "cityuvs",
        "policy": {
            "splitter": ["best", "random"],
            "min_samples_split": [0.5, 2, 3],
            "random_state": [1, 2, 3, 4],
        }
    }
]

TOTAL_CONTROLLER = {
    "regression": {
        "trainer": False,
        "evaluator_exhibitor": False
    },
    "correlation": {
        "trainer": False,
        "evaluator_exhibitor": False
    },
    "complexity": {
        "trainer": True,
        "evaluator_exhibitor": True
    }
}
