import pandas as pd

path_to_data_indian = "data/Indian_food/cuisines.csv"

path_to_kaggle = "data/Kaggle_recipes/Food Ingredients and Recipe Dataset with Image Name Mapping.csv"

data_frame = pd.read_csv(path_to_kaggle)

print(data_frame.columns)