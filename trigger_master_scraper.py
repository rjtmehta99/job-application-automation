import yaml
import importlib
from helpers.constants import COMPANY_MASTER_DATA

with open(COMPANY_MASTER_DATA, 'r') as file:
    data = yaml.safe_load(file)

# Get all python files and run scrape
python_files = [data[key]['python_file'] for key in data.keys()]

for py_file in python_files:
    imported_file = importlib.import_module(name=py_file)
    imported_file.scrape()
