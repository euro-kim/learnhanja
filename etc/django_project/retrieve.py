import os
import django
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import csv
from app_0.models import model_Person

# Retrieve all model_Person objects
QuerySet_Person = model_Person.objects.all()
dict_Person = list(QuerySet_Person.values())
# Convert list of dictionaries to a pandas DataFrame
df = pd.json_normalize(dict_Person)

# Expand lists in DataFrame into separate columns
hanjas_df = pd.DataFrame(df['hanjas'].tolist(), index=df.index).add_prefix('hanja_')
result_df = pd.DataFrame(df['result'].tolist(), index=df.index).add_prefix('result_')

# Drop original columns and concatenate expanded columns
df = df.drop(columns=['hanjas', 'result']).join(hanjas_df).join(result_df)

# Create a new Excel workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "Person Data"

# Write the DataFrame to the Excel file
for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        ws.cell(row=r_idx, column=c_idx, value=value)

# Save the workbook
wb.save("save.xlsx")
