import pandas as pd


mayors = pd.read_csv('./city_ps_2000_2017.csv')
mayor_names = mayors['name'].unique()

# counter == 331
# len(mayors['name'].unique()) == 1637
counter = 0 

# term_length and term_year

for mayor in mayor_names:
    mayor_rows = mayors[mayors['name']==mayor]
    if 2007.0 not in list(mayor_rows['year']):
        continue
    counter += 1
    city_2007 = mayor_rows[mayor_rows['year'] == 2007.0].iloc[0]['cityID']
    city_rows = mayor_rows[mayor_rows['cityID'] == city_2007]
    num_years = city_rows.shape[0]
    term_len = range(num_years)
    for year, index in enumerate(city_rows.index):
        mayors.loc[index, 'term_year'] = year + 1
        mayors.loc[index, 'term_length'] = num_years

mayor_rows = mayors[mayors['term_year']==1.0]
mayor_names = mayor_rows['name'].unique()
print(mayor_rows.shape)

# rank, job, and location

background = pd.read_csv('./full_data.csv')
counter = 0
for mayor in mayor_names:
    mayor_row = mayor_rows[mayor_rows['name']==mayor]
    mayors_ind = mayor_row.index[0]
    background_rows = background[background['name'].str.contains(mayor)]
    job_rows = background_rows.loc[background_rows['job']=='市委书记']
    counter += 1
    found = False
    prior_ind = -1
    current_ind = -1
    next_ind = -1
    for i, ind in enumerate(job_rows.index):
        start_year = int(job_rows.loc[ind, 'start_date'].split('/')[0])
        end_year = int(job_rows.loc[ind, 'end_date'].split('/')[0])
        if start_year <= 2007 and end_year >= 2007:
            prior_ind = ind - 1
            current_ind = ind
            next_ind = ind + 1
            found = True
            break
    if found:
        rank_current = background_rows.loc[current_ind, 'rank']
        mayors.loc[mayors_ind, 'rank_current'] = rank_current
        if prior_ind in background_rows.index:
            rank_prior = background_rows.loc[prior_ind, 'rank']
            job_prior = background_rows.loc[prior_ind, 'job']
            location_prior = background_rows.loc[prior_ind, 'location']
            mayors.loc[mayors_ind, 'rank_prior'] = rank_prior
            mayors.loc[mayors_ind, 'job_prior'] = job_prior
            mayors.loc[mayors_ind, 'location_prior'] = location_prior
        if next_ind in background_rows.index:
            rank_next = background_rows.loc[next_ind, 'rank']
            job_next = background_rows.loc[next_ind, 'job']
            location_next = background_rows.loc[next_ind, 'location']
            mayors.loc[mayors_ind, 'rank_next'] = rank_next
            mayors.loc[mayors_ind, 'job_next'] = job_next
            mayors.loc[mayors_ind, 'location_next'] = location_next
    else:
        # Cannot find row where the 标志位 variable has value "市委书记"
        mayors.loc[mayors_ind, 'rank_current'] = "NOT FOUND"
        print('Cannot find information for', mayors.loc[mayors_ind, 'name'])
print(counter)
mayors.to_stata('./city_ps_2000_2017.dta', version=118)