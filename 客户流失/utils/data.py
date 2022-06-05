from settings import BASE_DIR, MYSQL_CONFIG
from pandas import DataFrame, read_sql_query
from sqlalchemy import create_engine


class DataLoader:
    def __init__(self):
        self.txt_data_path = BASE_DIR / "statics" / "userlostprob.txt"
        self.conn = create_engine(
            url=self.format_mysql_conn_string(
                format_dict=MYSQL_CONFIG
            )
        )

    @staticmethod
    def format_mysql_conn_string(format_dict):
        user = format_dict["user"]
        password = format_dict["password"]
        host = format_dict["host"]
        port = format_dict["port"]
        db = format_dict["db"]

        return f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'

    def read_txt_data(self):

        data_list = []
        with open(str(self.txt_data_path), "r", encoding="utf8") as f:
            columns = f.readline().strip().split()

            while 1:
                data_line = f.readline().strip().split()

                if data_line:
                    data_list.append(data_line)
                else:
                    break

        df = DataFrame(
            data=data_list,
            columns=columns
        )

        print("数据读取完毕！")

        return df

    def data_to_sql(self, data_df):

        data_df.to_sql(
            name="customer_discontent",
            con=self.conn,
            index=False
        )

    def read_sql_data(self, column=None):

        if column:
            sql = f"""
                select {column}
                from customer_discontent
            """

        else:
            sql = f"""
                select *
                from customer_discontent
            """

        return read_sql_query(
            sql=sql,
            con=self.conn
        )
