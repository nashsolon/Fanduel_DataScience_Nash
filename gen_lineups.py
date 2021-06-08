import numpy as np
from numpy import random
import pandas as pd 

def csv_df(path):
    # print(path)
    df = pd.read_csv(path)
    # print (df)
    return df


def drop_unwanted(df, unwanted):
    dropped_unwanted = df.drop(unwanted, axis = 1)
    return dropped_unwanted

def get_only_healthy(df):
    df = df.where(df['Injury Indicator'] == 'Healthy')
    
    only_healthy = df.dropna()
    # print(only_healthy)
    return only_healthy

def sorted_FPPG(df):
    sorted_FPPG_df = df.sort_values(by = ['FPPG'], ascending = False)
    sorted_FPPG_df = sorted_FPPG_df.reset_index(drop = True)
    return sorted_FPPG_df

def get_above_x(df, x):
    df = df.where(df['FPPG'] >= x)

    
    above_16_FPPG = df.dropna()
    # print(only_healthy)
    return above_16_FPPG

def sorted_position(df, position):
    only_position_nan = df.where(df['Position'] == position)
    only_position = only_position_nan.dropna()
    sorted_position = only_position.sort_values(by = ['FPPG'], ascending = False)
    sorted_position = sorted_position.reset_index(drop = True)

    return sorted_position

def add_pps(df):
    # added_pps = df
    pps = (df['FPPG']/df['Salary'])*100
    pps_list = pps.to_list()
    df.insert(5, 'PPS', pps_list)
    

    return df

def sorted_all_pps(df):
    df = df.sort_values(by = ['PPS'], ascending = False)
    sorted_pps_df = df.reset_index(drop = True)
    return sorted_pps_df

def add_position_index(df):
   
    # unique_pos = df['Position'].unique() STILL DOES IN ORDER :(
    unique_pos = ['PG', 'SG','SF','PF','C']
    
    # CREATE A COLUMN IN DF THAT HAS POSITIONS AS NUMERICAL VALUES
    zero_positions = pd.DataFrame(np.zeros(df.shape[0]))
    df.insert(2,'Position_Index', zero_positions)
    for i, position in enumerate(unique_pos):
        # print(i)
        # print(position)
        
        #np.where returns list of indices where condition is satisfied
        position_indeces = np.where(df['Position'] == position)

        for position_index in position_indeces[0]:
            df.loc[position_index, 'Position_Index'] = i
            # print(position_indeces)
        
    return df


def choose_top_stars_by_PPS(sorted_above_16_w_position_indices, x, y, position_limit):
    top_y_players = sorted_above_16_w_position_indices[:y]
    sorted_top_y = sorted_all_pps(top_y_players)

    limit = x

    proper_order = sorted_above_16_w_position_indices.columns.tolist()

    chosen_stars = pd.DataFrame()

    for player_index in sorted_top_y.index:
        player_info = sorted_top_y.iloc[player_index]
        # print(type(player_info))
        # print('Hi my name is ' + player_info['Nickname'] + ' and I play ' + player_info['Position'])
        if limit != 0 :
            position_index = int(player_info['Position_Index'])
            if position_limit[position_index] != 0:
                print('Hi my name is ' + player_info['Nickname'] + ' and I play ' + player_info['Position']
                    + '. I am a chosen star because I am in the top ' + str(y) + ' FPPG players and top ' + str(x) + ' PPS players.')
                limit = limit - 1
                position_limit[position_index] = position_limit[position_index] - 1
                chosen_stars = chosen_stars.append(player_info)
    
    chosen_stars_by_PPS = chosen_stars[proper_order]

    #WE NEED TO RETURN THE REMAINING PLAYERS AS WELL
    remaining_players = (sorted_above_16_w_position_indices[~sorted_above_16_w_position_indices.Nickname.isin(chosen_stars.Nickname)])

    return chosen_stars_by_PPS, position_limit, remaining_players

#Stars are the top 10 (y-value) players with the highest FPPG
def choose_top_stars_by_FPPG(sorted_above_16_w_position_indices, x, y, position_limit):
    top_y_players = sorted_above_16_w_position_indices[:y]
    

    limit = x

    proper_order = sorted_above_16_w_position_indices.columns.tolist()

    chosen_stars = pd.DataFrame()
    remaining_players = pd.DataFrame()

    for player_index in top_y_players.index:
        player_info = top_y_players.iloc[player_index]
        # print(type(player_info))
        # print('Hi my name is ' + player_info['Nickname'] + ' and I play ' + player_info['Position'])
        if limit != 0 :
            position_index = int(player_info['Position_Index'])
            if position_limit[position_index] != 0:
                print('Hi my name is ' + player_info['Nickname'] + ' and I play ' + player_info['Position']
                    + '. I am a chosen star because I am in the top ' + str(x) + ' FPPG players')
                limit = limit - 1
                position_limit[position_index] = position_limit[position_index] - 1
                chosen_stars = chosen_stars.append(player_info)

            

        # print(player_info)
        # print()

    #WE NEED TO RETURN THE REMAINING PLAYERS AS WELL
    remaining_players = (sorted_above_16_w_position_indices[~sorted_above_16_w_position_indices.Nickname.isin(chosen_stars.Nickname)])

    chosen_stars_by_FPPG = chosen_stars[proper_order]

    return chosen_stars_by_FPPG, position_limit, remaining_players


    

# When choosing random players, make sure we extract them from remaining players
def gen_top_stars_lineup(sorted_above_16_w_position_indices, positions_list, PPS_or_FPPG):

    position_limits = [2, 2, 2, 2, 1]

    full_lineup = pd.DataFrame()

    if PPS_or_FPPG == 'PPS':
        top_stars, position_limits, remaining_players = choose_top_stars_by_PPS(sorted_above_16_w_position_indices, 1, 10, position_limits)
        print()

    if PPS_or_FPPG == 'FPPG':
        top_stars, position_limits, remaining_players = choose_top_stars_by_FPPG(sorted_above_16_w_position_indices, 1, 10, position_limits)
        print()

    full_lineup = full_lineup.append(top_stars)
    
    print()
    
    

    # OLD WAY
    # sorted_pg_above_16 = sorted_position(sorted_above_16, 'PG')
    # sorted_sg_above_16 = sorted_position(sorted_above_16, 'SG')
    # sorted_sf_above_16 = sorted_position(sorted_above_16, 'SF')
    # sorted_pf_above_16 = sorted_position(sorted_above_16, 'PF')
    # sorted_c_above_16 = sorted_position(sorted_above_16, 'C')

    # sorted_df_list.append(sorted_pg_above_16)
    # sorted_df_list.append(sorted_sg_above_16)
    # sorted_df_list.append(sorted_sf_above_16)
    # sorted_df_list.append(sorted_pf_above_16)
    # sorted_df_list.append(sorted_c_above_16)

    remaining_players_above_20 = get_above_x(remaining_players, 20)

    # NEW WAY
    sorted_positions_by_FPPG_above_20 = []

    for position in positions_list:
        sorted_one_position_remaining = sorted_position(remaining_players_above_20, position)
        sorted_positions_by_FPPG_above_20.append(sorted_one_position_remaining)

    #Just for show
    sorted_PG = sorted_positions_by_FPPG_above_20[0]
    sorted_SG = sorted_positions_by_FPPG_above_20[1]
    sorted_SF = sorted_positions_by_FPPG_above_20[2]
    sorted_PF = sorted_positions_by_FPPG_above_20[3]
    sorted_C = sorted_positions_by_FPPG_above_20[4]
    # print()

    positions = ['PG', 'SG', 'SF', 'PF', 'C']
    position_indexer = 0
    
    for position_limit in position_limits:
        while position_limit > 0:
            # position_limit.index
            
            sorted_position_above_20 = sorted_positions_by_FPPG_above_20[position_indexer]
            size_of_position_list = sorted_position_above_20.shape[0]
            random_player_index = random.randint(size_of_position_list - 1)

            chosen_random_player_series = sorted_position_above_20.iloc[random_player_index]
            print("The random " + positions[position_indexer] + ' we chose is ' + chosen_random_player_series['Nickname'])
            
            full_lineup = full_lineup.append(chosen_random_player_series)

            position_limits[position_indexer] = position_limits[position_indexer] - 1
            position_limit = position_limit - 1
            
            if position_indexer == 5:
                position_indexer = 0
            print()
        position_indexer = position_indexer + 1

    full_lineup = full_lineup.reset_index(drop=True)
    return full_lineup


def calculate_tot_salary(df):
    # print()
    tot_salary = np.sum(df['Salary'])
    return (tot_salary)

def calculate_tot_FPPG(df):
    # print()
    tot_FPPG = np.sum(df['FPPG'])
    return (tot_FPPG)




csv_month = '06'
csv_day = '07'
csv_year = '2021'
path = '../Fanduel_csvs/FanDuel-NBA-' + csv_month + '-' + csv_day + '-' + csv_year+ '.csv'
raw_sports_data = csv_df(path)

unwanted_cols = ['Tier', 'Unnamed: 14', 'Unnamed: 15']
drop_sports_data = drop_unwanted(raw_sports_data, unwanted_cols)

# Fill NaN with healthy 
drop_sports_data['Injury Indicator'] = drop_sports_data['Injury Indicator'].fillna('Healthy')
drop_sports_data['Injury Details'] = drop_sports_data['Injury Details'].fillna('Healthy')

# print(drop_sports_data)

all_only_healthy = get_only_healthy(drop_sports_data)

sorted_all_FPPG = sorted_FPPG(all_only_healthy)

sorted_above_16 =  get_above_x(sorted_all_FPPG, 16)

above_16_w_pps = add_pps(sorted_above_16)

players_16_pps_position_indeces = add_position_index(above_16_w_pps)


# NEXT LINE PUTS IN ORDER OF HIGHEST FPPG POSITION. NO GOOD
# positions_list = sorted_above_16.Position.unique()

positions_list = ['PG', 'SG','SF','PF','C']
# position_limit = [2, 2, 2, 2, 1]

top_stars_lineup_FPPG = gen_top_stars_lineup(players_16_pps_position_indeces, positions_list, 'FPPG')

top_stars_lineup_PPS = gen_top_stars_lineup(players_16_pps_position_indeces, positions_list, 'PPS')

total_salary_FPPG = calculate_tot_salary(top_stars_lineup_FPPG)
print(top_stars_lineup_FPPG)
print('The total salary for this team is ' + str(total_salary_FPPG))
print()
total_salary_PPS =  calculate_tot_salary(top_stars_lineup_PPS)
print(top_stars_lineup_PPS)
print('The total salary for this team is ' + str(total_salary_PPS))
print()

# single_team_df = pd.DataFrame(columns = ['Team_Num' ,'Teams', 'Tot_Salary'])
FPPG_teams_df = pd.DataFrame(columns = ['Team_Num' ,'Teams', 'Positions', 'Tot_Salary', 'Tot_FPPG'])
PPS_teams_df = pd.DataFrame(columns = ['Team_Num', 'Teams', 'Positions', 'Tot_Salary', 'Tot_FPPG'])

team_counter = 0
for i in range(0, 50):
    team_list = []
    position_list = []
    single_team_df = pd.DataFrame(columns = ['Team_Num' ,'Teams', 'Tot_Salary'])
    top_stars_lineup_FPPG = gen_top_stars_lineup(players_16_pps_position_indeces, positions_list, 'FPPG')
    # total_salary_FPPG = calculate_tot_salary(top_stars_lineup_FPPG)
    for player_index in top_stars_lineup_FPPG.index:
        player_info = top_stars_lineup_FPPG.loc[player_index]
        player_name = player_info['Nickname']
        player_position = player_info['Position']

        position_list.append(player_position)
        team_list.append(player_name)
    
    print(i)
    

    # team_series = pd.Series(team_list)
    single_team_df['Teams'] = team_list

    single_team_df['Team_Num'] = team_counter
    team_counter = team_counter + 1

    single_team_df['Positions'] = position_list
    # team_counter = team_counter + 1
    
    total_salary_FPPG = calculate_tot_salary(top_stars_lineup_FPPG)
    single_team_df['Tot_Salary'] = total_salary_FPPG

    total_FPPG = calculate_tot_FPPG(top_stars_lineup_FPPG)
    single_team_df['Tot_FPPG'] = total_FPPG

    FPPG_teams_df = FPPG_teams_df.append(single_team_df)

    print()
    print('New change!')

    # del single_team_df


    

    



