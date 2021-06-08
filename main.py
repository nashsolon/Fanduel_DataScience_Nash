import numpy as np
import pandas as pd 


# new_array = np.zeros(7)
# print(new_array)

def csv_df(path):
    print(path)
    df = pd.read_csv(path)
    # print (df)
    return df


def drop_unwanted(df, unwanted):
    df = df.drop(unwanted, axis = 1)
    return df


def points_per_salary(df):
    print('hello')
    pps = (df['FPPG']/df['Salary'])*100
    pps_list = pps.to_list()
    
    names = df['Nickname']
    names_list = names.to_list()

    position = df['Position']
    position_list = position.to_list()

    FPPG = df['FPPG']
    FPPG_list = FPPG.to_list()

    salary = df['Salary']
    salary_list = salary.to_list()

    injury = df['Injury Indicator']
    injury_list = injury.to_list()

    injury_details = df['Injury Details']
    injury_details_list = injury_details.to_list()

    pps = pps.to_frame()
    pps['Name'] = names_list
    pps['Position'] = position_list
    pps['Points_Per_Sal'] = pps_list
    pps['FPPG'] = FPPG_list
    pps['Salary'] = salary_list
    pps['Injury Indicator'] = injury_list
    pps['Injury Details'] = injury_details_list
    pps = pps.drop(0, axis = 1)
    # print(names)
    # print(pps)
     
    return pps


def sorted_position(df, position):
    only_position_nan = df.where(df['Position'] == position)
    only_position = only_position_nan.dropna()
    sorted_position = only_position.sort_values(by = ['Points_Per_Sal'], ascending = False)
    sorted_position = sorted_position.reset_index(drop = True)
   
    return sorted_position

def sorted_all_pps(df):
    df = df.sort_values(by = ['Points_Per_Sal'], ascending = False)
    return df



# def generate_random(df):
#     print('hi')

csv_month = '06'
csv_day = '02'
csv_year = '2021'
path = '../Fanduel_csvs/FanDuel-NBA-' + csv_month + '-' + csv_day + '-' + csv_year+ '.csv'
raw_sports_data = csv_df(path)

unwanted_cols = ['Tier', 'Unnamed: 14', 'Unnamed: 15']
drop_sports_data = drop_unwanted(raw_sports_data, unwanted_cols)

# Fill NaN with healthy 
drop_sports_data['Injury Indicator'] = drop_sports_data['Injury Indicator'].fillna('Healthy')
drop_sports_data['Injury Details'] = drop_sports_data['Injury Details'].fillna('Healthy')


##PPS Stuff
pps = points_per_salary(drop_sports_data)

sorted_pg = sorted_position(pps, 'PG')
sorted_sg = sorted_position(pps, 'SG')
sorted_sf = sorted_position(pps, 'SF')
sorted_pf = sorted_position(pps, 'PF')
sorted_c = sorted_position(pps, 'C')

sorted_all = sorted_all_pps(pps)

##Generate random lineup stuff



my_player_list = ['Lamelo Ball', 'Russel Westbrook', 
                    'Marcus Smart', 'Malik Monk','Rui Hachimura', 'Oshae Brissett', 'Jayson Tatum'
                    , 'Doug McDermott', 'Tristan Thompson' ]

# Lamelo - 17.2
# Russ - 55.3
# Smart - 20.4
# Monk - 16.2
# Rui - 22.2
# Oshae - 32
# Tatum - 72.6
# McDermott - 25.6
# Tristan Thompson - 30.4

