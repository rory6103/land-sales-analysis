# class Data():
#     def __init__(self, fname):
#         self.df = pd.read_csv(fname, low_memory=False) if fname[-3:] == "csv" else pd.read_stata(fname)
#         self.variables = list(self.df.columns)

#     def get_cities(self):
#         cities = list(self.df['cityID'].unique())
#         return cities

#     def get_variables(self):
#         return self.variables

def main(args):
    processed_data = pd.read_stata(args.label)
    labeled_cities = list(processed_data['cityID'].unique())
    print("labeled cities:", labeled_cities)
    labeled_variables = list(processed_data.columns)
    print("labeled variables:", labeled_variables)
    unprocessed_data = pd.read_csv(args.data, low_memory=False)
    raw_regions = list(unprocessed_data['region'].unique())
    print("num raw regions:", len(raw_regions))
    raw_approvals = list(unprocessed_data['approval_unit'].unique())
    print("num raw approval units:", len(raw_approvals))
    raw_variables = list(unprocessed_data.columns)
    print("raw variables:", raw_variables)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Processor')
    parser.add_argument("--label", "-l", default=label_path, help="Load existing processed data")
    parser.add_argument("--data", "-d", default=data_path, help="Load unprocessed raw data")
    args = parser.parse_args()
    print(args)
    main(args)