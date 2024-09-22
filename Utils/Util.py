import yaml
from pydantic import BaseModel



class Util(BaseModel):
    @staticmethod
    def read_yaml(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data