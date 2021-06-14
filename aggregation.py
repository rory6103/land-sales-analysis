import numpy as np
import pandas as pd

CITYID_PATH = './city.csv'
LAND_CITY = './land_city.csv'
SAVE_PATH = 'land_city.csv'

def aggregate(dataframe, col='total', types=[]):
    city_year_unique = list(dataframe.index.unique())
    if types == []:
        if col=='total':
            types = ['total']
        else:
            types = list(dataframe[col].unique())
    arr = np.zeros((len(city_year_unique), 3*len(types)))
    if col=='total':
        for i, cyear in enumerate(city_year_unique):
            # Extracting multiple rows with same index using loc
            df_temp = dataframe.loc[cyear]
            # TODO: change to len(df_temp)
            arr[i][0] = len(dataframe['cityID'][cyear])
            prices = np.array(df_temp['deal_price_million'])
            arr[i][1] = np.sum(prices)
            areas = np.array(df_temp['area_ha'])
            arr[i][2] = np.sum(areas)
    else:
        for i, cyear in enumerate(city_year_unique):
            # Extracting multiple rows with same index using loc
            df_temp = dataframe.loc[cyear]
            for j, type in enumerate(types):
                # print(type, cyear)
                if len(df_temp.shape) == 1:
                    arr[i][j*3] = 1
                    arr[i][j*3+1] = df_temp['deal_price_million']
                    arr[i][j*3+2] = df_temp['area_ha']
                elif len(df_temp.shape) == 2:
                    type_df = df_temp[df_temp[col]==type]
                    arr[i][j*3] = len(type_df)
                    prices = np.array(type_df['deal_price_million'])
                    arr[i][j*3+1] = np.sum(prices)
                    areas = np.array(type_df['area_ha'])
                    arr[i][j*3+2] = np.sum(areas)
                else:
                    print("Unexpected")
    columns = []
    for type in types:
        columns.append(type+"_n")
        columns.append(type+"_p")
        columns.append(type+"_a")
    res = pd.DataFrame(arr, index=city_year_unique, columns=columns)
    return res        

df = pd.read_csv(LAND_CITY, index_col='city_year', low_memory=False)
df.fillna(0 ,inplace=True)
cols = list(df.columns)

# Retrieve the IDs associated with each city
city_id_df = pd.read_csv(CITYID_PATH, low_memory=False)
city_labels = list(city_id_df['city.name'])
city_ids = list(city_id_df['city.id'])
# Construct a dictionary that maps the IDs of the cities to their names
city_ids = dict(zip(city_ids, city_labels))
total_temp = aggregate(df)
cities = [city_ids[city_year//100] for city_year in total_temp.index]
total_temp.insert(0, "cityID", cities)
forway_temp = aggregate(df, col='forway')
land_source_temp = aggregate(df, col='land_source')
frames = [total_temp, forway_temp, land_source_temp]
result = pd.concat(frames, axis=1, join="inner")
result.to_csv(SAVE_PATH)