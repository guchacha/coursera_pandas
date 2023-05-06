import pandas as pd
import numpy as np
import scipy.stats as stats


def nhl_correlation():
    cities = pd.read_html("core/input_files/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
    cities.columns = ['Metropolitan area', 'Population', 'NFL', 'MLB', 'NBA', 'NHL']
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='\[.*\]', value='',
                                                                                        regex=True)
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='', value=np.nan,
                                                                                        regex=True)
    cities[['NFL', 'MLB', 'NBA', 'NHL']] = cities[['NFL', 'MLB', 'NBA', 'NHL']].replace(to_replace='—', value=np.nan,
                                                                                        regex=True)

    nhl_cities = cities[['Metropolitan area', 'Population', 'NHL']]
    nhl_cities = nhl_cities.dropna().reset_index(drop=True)

    nhl_cities[['area1', 'area2', 'area3']] = nhl_cities['NHL'].replace(r'([A-Z])', r' \1', regex=True).str.split(
        expand=True)

    nhl_df = pd.read_csv("core/input_files/nhl.csv")
    nhl_df = nhl_df.loc[nhl_df['year'] == 2018]
    nhl_df = nhl_df.drop([0, 9, 18, 26])
    nhl_df['team'] = nhl_df['team'].replace(to_replace='\*', value='', regex=True)
    nhl_df = nhl_df.reset_index(drop=True)
    nhl_df[['W', 'L']] = nhl_df[['W', 'L']].astype(int)
    nhl_df['WL Ratio'] = nhl_df['W'] / (nhl_df['W'] + nhl_df['L'])
    nhl_df = nhl_df[['team', 'WL Ratio']]

    nhl_df[['team0', 'team1', 'team2']] = nhl_df['team'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)

    nhl_cities = nhl_cities.merge(nhl_df[['WL Ratio', 'team1']], how='left', left_on='area1', right_on='team1')
    nhl_cities = nhl_cities.merge(nhl_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area1', right_on='team2')
    nhl_cities['WL Ratio_area1'] = nhl_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    nhl_cities = nhl_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    nhl_cities = nhl_cities.merge(nhl_df[['WL Ratio', 'team1']], how='left', left_on='area2', right_on='team1')
    nhl_cities = nhl_cities.merge(nhl_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area2', right_on='team2')
    nhl_cities['WL Ratio_area2'] = nhl_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    nhl_cities = nhl_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    nhl_cities = nhl_cities.merge(nhl_df[['WL Ratio', 'team1']], how='left', left_on='area3', right_on='team1', suffixes=('_a', '_b'))
    nhl_cities = nhl_cities.merge(nhl_df[['WL Ratio', 'team2']].dropna(), how='left', left_on='area3', right_on='team2')
    nhl_cities['WL Ratio_area3'] = nhl_cities[['WL Ratio_x', 'WL Ratio_y']].mean(axis=1)
    nhl_cities = nhl_cities.drop(['WL Ratio_x', 'team1', 'WL Ratio_y', 'team2'], axis=1)

    nhl_cities['avg WL Ratio'] = nhl_cities[['WL Ratio_area1', 'WL Ratio_area2', 'WL Ratio_area3']].mean(axis=1)
    nhl_cities = nhl_cities[['Population', 'avg WL Ratio']]

    population_by_region = nhl_cities['Population'].astype(int).tolist()
    win_loss_by_region = nhl_cities['avg WL Ratio'].tolist()
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
