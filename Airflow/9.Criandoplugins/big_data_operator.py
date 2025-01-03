# Domine Apache Airflow. https://www.eia.ai/
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd

class BigDataOperator(BaseOperator):

    @apply_defaults
    def __init__(self,path_to_csv_file,path_to_save_file,separator=";",
                 file_type='parquet',*args,**kwargs ) -> None:
        super().__init__(*args,**kwargs)
        self.path_to_csv_file = path_to_csv_file
        self.path_to_save_file = path_to_save_file
        self.separator = separator
        self.file_type = file_type

    def execute(self,context):
        df = pd.read_csv(self.path_to_csv_file, sep=self.separator)
        if self.file_type == 'parquet':
            df.to_parquet(self.path_to_save_file)
        elif self.file_type == 'json':
            df.to_json(self.path_to_save_file)
        else:
            raise ValueError("O valor é inválido")
