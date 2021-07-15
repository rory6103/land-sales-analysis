from collections import defaultdict
import pandas as pd

### Requires Data_City_1994_2017.dta, land.csv, and city.csv in the same folder
### Generates land_city.csv in the same folder

LABEL_PATH = './Data_City_1994_2017.dta'
DATA_PATH = '../land.csv'
CITYID_PATH = './city.csv'
SAVE_PATH = 'land_city.csv'
DESIRED_VARS = ['forway', 'deal_price_millon', 'land_source', 'approval_unit', 'contract_date', 
                'company_industry', 'landlevel', 'region', 'area_ha', 'landuse']
LAND_SOURCE_MAP = {'现有建设用地':'existing', '新增建设用地(来自存量库)':'stock', '新增建设用地':'new'}
FORWAY_MAP = defaultdict(lambda:'other', key='other')
FORWAY_MAP.update({'挂牌出让':'auction', '拍卖出让':'auction', '招标出让':'auction', '招拍挂出让':'auction', '划拨':'transfer', '协议出让':'agreement', '租赁':'lease'})

def extract_city(str):
    """ Remove the suffix '市','盟','地区', or '自治州' (if any) 
        If no suffix found, return the original name
    """
    if str[-1] == '市' or str[-1] == '盟':
        return str[:-1]
    elif str[-2:] == '地区':
        return str[:-2]
    elif str[-3:] == '自治州':
        return str[:-3]
    else:
        print(str)
        return str

def get_city_keys():
    """ Construct a dictionary that maps the city names without suffix 
        to the city labels
    """
    processed_data = pd.read_stata(LABEL_PATH)
    labeled_cities = list(processed_data['cityID'].unique())
    city_keys = {}
    for city in labeled_cities:
        # If the label is separated by a '/', map both cities
        # before and after the '/', to the same label
        if '/' in city:
            cities = city.split('/')
            for temp_city in cities:
                city_keys[extract_city(temp_city)] = city
        else:
            city_keys[extract_city(city)] = city
    return city_keys

def get_types_and_cities(data):
    """ Takes in a dataset and determine if each row is a city-level transaction
        Returns a list of city names new_regions and a list of binary values city_types
    """
    new_regions = []
    city_types = []
    city_keys = get_city_keys()
    # Iterate through all the values from the approval_unit column
    for unit in data['approval_unit']:
        temp = ""
        # Iterate through the city labels withou suffix to match the city name
        for city in list(city_keys.keys()):
            if city in str(unit):
                # If a label is matched, append the label 
                # and exit current iteration in the inner loop
                if '市' in unit or '盟' in unit or '地区' in unit or '自治州' in unit:
                    temp = city_keys[city]
                    break
        # If no label is found to match the city name, mark it as not city-level
        if temp == "":
            new_regions.append("NA")
            city_types.append(0)
        else:
            new_regions.append(temp)
            city_types.append(1)
    return (new_regions, city_types)

if __name__ == "__main__":
    # load the land.csv file
    unprocessed_data = pd.read_csv(DATA_PATH, low_memory=False)
    # Get the column names from the file
    raw_variables = list(unprocessed_data.columns)
    # Keep desired variables and dropped the unwanted columns
    drop_variables = [var for var in raw_variables if var not in DESIRED_VARS]
    unprocessed_data.drop(columns=drop_variables, inplace=True)
    # Rename columns
    unprocessed_data.rename(columns={'contract_date':'year'}, inplace=True)
    unprocessed_data.rename(columns={'deal_price_millon':'deal_price_million'}, inplace=True)
    # Convert forway values
    unprocessed_data['forway'] = unprocessed_data['forway'].apply(lambda x: FORWAY_MAP[x])
    # Translate land_source values
    unprocessed_data['land_source'] = unprocessed_data['land_source'].apply(lambda x: LAND_SOURCE_MAP[x])
    # Determine if a transaction is city-level and the associated city based on "approval_unit"
    new_regions, city_types = get_types_and_cities(unprocessed_data)
    # Insert the extracted city names into a new column "cityID"
    unprocessed_data.insert(2, "cityID", new_regions)
    # Find indices for rows that are determined to be not city-level transactions
    drop_ind = [i for (i, t) in enumerate(city_types) if t == 0]
    # Drop rows that are not city-level transactions
    unprocessed_data.drop(index=drop_ind, inplace=True)
    # Retrieve the IDs associated with each city
    city_id_df = pd.read_csv(CITYID_PATH, low_memory=False)
    city_labels = list(city_id_df['city.name'])
    city_ids = list(city_id_df['city.id'])
    # Construct a dictionary that maps the names of the cities to their IDs
    city_ids = dict(zip(city_labels, city_ids))
    # Extract the last two digits from the values in the 'year' column
    years = list(unprocessed_data['year'])
    years = [s[2:4] for s in years]
    # Construct and insert the 'city_year' column by concatenating the cityIDs and years
    city_years = [str(city_ids[c])+years[i] for (i, c) in enumerate(list(unprocessed_data['cityID']))]
    unprocessed_data.insert(4, 'city_year', city_years)
    # Sort the data by the 'city_year' column
    unprocessed_data.sort_values('city_year', inplace=True)
    # Save the processed data to local folder
    unprocessed_data.to_csv(SAVE_PATH, index=False)