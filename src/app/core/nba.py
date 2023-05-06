import pandas as pd
import numpy as np
import scipy.stats as stats


def nba_correlation():
    cities = pd.read_html("core/input_files/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
    cities.columns = ['Metropolitan area', 'Population', 'NFL', 'MLB', 'NBA', 'NHL']
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='\[.*\]', value='',
                                                                                        regex=True)
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='', value=np.nan,
                                                                                        regex=True)
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='—', value=np.nan,
                                                                                        regex=True)

    nba_cities = cities[['Metropolitan area', 'Population', 'NBA']]
    nba_cities = nba_cities.dropna().reset_index(drop=True)

    nba_cities[['area1', 'area2']] = nba_cities['NBA'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)

    nba_df = pd.read_csv("core/input_files/nba.csv")
    nba_df = nba_df.loc[nba_df['year'] == 2018]
    nba_df['team'] = nba_df['team'].replace(to_replace='\*', value='', regex=True)
    nba_df['team'] = nba_df['team'].replace(to_replace='\(\d*\)', value='', regex=True)
    nba_df[['W', 'L']] = nba_df[['W', 'L']].astype(int)
    nba_df['WL Ratio'] = nba_df['W'] / (nba_df['W'] + nba_df['L'])
    nba_df = nba_df[['team', 'WL Ratio']]

    nba_df[['team0', 'team1', 'team2']] = nba_df['team'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)

    nba_cities = nba_cities.merge(nba_df[['WL Ratio', 'team1']], how='left', left_on='area1', right_on='team1')
    nba_cities = nba_cities.merge(nba_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area1', right_on='team2')
    nba_cities['WL Ratio_area1'] = nba_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    nba_cities = nba_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    nba_cities = nba_cities.merge(nba_df[['WL Ratio', 'team1']], how='left', left_on='area2', right_on='team1')
    nba_cities = nba_cities.merge(nba_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area2', right_on='team2')
    nba_cities['WL Ratio_area2'] = nba_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    nba_cities = nba_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    nba_cities['avg WL Ratio'] = nba_cities[['WL Ratio_area1', 'WL Ratio_area2']].mean(axis=1)
    nba_cities = nba_cities[['Population', 'avg WL Ratio']]

    population_by_region = nba_cities['Population'].astype(int).tolist()
    win_loss_by_region = nba_cities['avg WL Ratio'].tolist()
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
