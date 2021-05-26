# class Data():
#     def __init__(self, fname):
#         self.df = pd.read_csv(fname, low_memory=False) if fname[-3:] == "csv" else pd.read_stata(fname)
#         self.variables = list(self.df.columns)

#     def get_cities(self):
#         cities = list(self.df['cityID'].unique())
#         return cities

#     def get_variables(self):
#         return self.variables
