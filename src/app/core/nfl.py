import pandas as pd
import numpy as np
import scipy.stats as stats


def nfl_correlation():
    cities = pd.read_html("core/input_files/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
    cities.columns = ['Metropolitan area', 'Population', 'NFL', 'MLB', 'NBA', 'NHL']
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='\[.*\]', value='',
                                                                                        regex=True)
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='', value=np.nan,
                                                                                        regex=True)
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='—', value=np.nan,
                                                                                        regex=True)

    nfl_cities = cities[['Metropolitan area', 'Population', 'NFL']]
    nfl_cities = nfl_cities.dropna().reset_index(drop=True)

    nfl_cities[['area1', 'area2']] = nfl_cities['NFL'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)

    nfl_df = pd.read_csv("core/input_files/nfl.csv")
    nfl_df = nfl_df.loc[nfl_df['year'] == 2018]
    nfl_df = nfl_df.drop([0, 5, 10, 15, 20, 25, 30, 35])
    nfl_df['team'] = nfl_df['team'].replace(to_replace='\*', value='', regex=True)
    nfl_df['team'] = nfl_df['team'].replace(to_replace='\+', value='', regex=True)
    nfl_df = nfl_df.reset_index(drop=True)
    nfl_df[['W', 'L']] = nfl_df[['W', 'L']].astype(int)
    nfl_df['WL Ratio'] = nfl_df['W'] / (nfl_df['W'] + nfl_df['L'])
    nfl_df = nfl_df[['team', 'WL Ratio']]

    nfl_df[['team0', 'team1', 'team2']] = nfl_df['team'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)

    nfl_cities = nfl_cities.merge(nfl_df[['WL Ratio', 'team1']], how='left', left_on='area1', right_on='team1')
    nfl_cities = nfl_cities.merge(nfl_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area1', right_on='team2')
    nfl_cities['WL Ratio_area1'] = nfl_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    nfl_cities = nfl_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    nfl_cities = nfl_cities.merge(nfl_df[['WL Ratio', 'team1']], how='left', left_on='area2', right_on='team1')
    nfl_cities = nfl_cities.merge(nfl_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area2', right_on='team2')
    nfl_cities['WL Ratio_area2'] = nfl_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    nfl_cities = nfl_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    nfl_cities['avg WL Ratio'] = nfl_cities[['WL Ratio_area1', 'WL Ratio_area2']].mean(axis=1)
    nfl_cities = nfl_cities[['Population', 'avg WL Ratio']]

    population_by_region = nfl_cities['Population'].astype(int).tolist()
    win_loss_by_region = nfl_cities['avg WL Ratio'].tolist()
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
