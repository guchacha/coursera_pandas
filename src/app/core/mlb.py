import pandas as pd
import numpy as np
import scipy.stats as stats


def mlb_correlation():
    cities = pd.read_html("core/input_files/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
    cities.columns = ['Metropolitan area', 'Population', 'NFL', 'MLB', 'NBA', 'NHL']
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='\[.*\]', value='',
                                                                                        regex=True)
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='', value=np.nan,
                                                                                        regex=True)
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='—', value=np.nan,
                                                                                        regex=True)

    mlb_cities = cities[['Metropolitan area', 'Population', 'MLB']]
    mlb_cities['MLB'] = mlb_cities['MLB'].replace(to_replace='Sox', value='', regex=True)  # SettingWithCopyWarning:
# A value is trying to be set on a copy of a slice from a DataFrame. Try using .loc[row_indexer,col_indexer] = value instead
    mlb_cities = mlb_cities.dropna().reset_index(drop=True)

    mlb_cities[['area1', 'area2']] = mlb_cities['MLB'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)

    mlb_df = pd.read_csv("core/input_files/mlb.csv")
    mlb_df = mlb_df.loc[mlb_df['year'] == 2018]
    mlb_df['WL Ratio'] = mlb_df['W'] / (mlb_df['W'] + mlb_df['L'])
    mlb_df = mlb_df[['team', 'WL Ratio']]

    mlb_df[['team0', 'team1', 'team2']] = mlb_df['team'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)

    mlb_cities = mlb_cities.merge(mlb_df[['WL Ratio', 'team1']], how='left', left_on='area1', right_on='team1')
    mlb_cities = mlb_cities.merge(mlb_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area1', right_on='team2')
    mlb_cities['WL Ratio_area1'] = mlb_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    mlb_cities = mlb_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    mlb_cities = mlb_cities.merge(mlb_df[['WL Ratio', 'team1']], how='left', left_on='area2', right_on='team1')
    mlb_cities = mlb_cities.merge(mlb_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area2', right_on='team2')
    mlb_cities['WL Ratio_area2'] = mlb_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    mlb_cities = mlb_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    mlb_cities['avg WL Ratio'] = mlb_cities[['WL Ratio_area1', 'WL Ratio_area2']].mean(axis=1)
    mlb_cities = mlb_cities[['Population', 'avg WL Ratio']]

    population_by_region = mlb_cities['Population'].astype(int).tolist()
    win_loss_by_region = mlb_cities['avg WL Ratio'].tolist()
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]