import argparse
import pandas as pd

print(len("石家庄"))
print("市" in "石家庄")
print("市" in "石家庄市")

label_path = './Data_City_1994_2017.dta'
data_path = './land.csv'

desired_vars = ['forway', 'deal_price_millon', 'land_source', 'approval_unit', 'contract_date', 
                'company_industry', 'landlevel', 'region', 'area_ha', 'landuse']


processed_data = pd.read_stata(label_path)
labeled_cities = list(processed_data['cityID'].unique())
print("labeled cities:", len(labeled_cities), labeled_cities)
labeled_variables = list(processed_data.columns)
print("labeled variables:", len(labeled_variables), labeled_variables)
unprocessed_data = pd.read_csv(data_path, low_memory=False)
raw_regions = list(unprocessed_data['region'].unique())
print("num raw regions:", len(raw_regions))
raw_approvals = list(unprocessed_data['approval_unit'].unique())
print("num raw approval units:", len(raw_approvals))
raw_variables = list(unprocessed_data.columns)
print("raw variables:", len(raw_variables))

drop_variables = [var for var in raw_variables if var not in desired_vars]
unprocessed_data.drop(columns=drop_variables, inplace=True)
raw_variables = list(unprocessed_data.columns)
print("raw variables:", len(raw_variables), raw_variables)

unprocessed_data.to_csv('land_temp.csv')