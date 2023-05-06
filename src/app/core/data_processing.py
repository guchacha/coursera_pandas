import pandas as pd
import numpy as np
import scipy.stats as stats


def data_processing_and_correlation(filename: str, sport: str, area_list: list) -> float:
    """
    Function calculates the win/loss ratio's correlation with the population of the city.
    :param filename: csv input file name
    :param sport: sport index (NHL, NBA, MLB, NFL)
    :param area_list: additional columns for splitting teams names for city
    :return: Pearson correlation coefficient value
    """

    # wikipedia data cleaning
    cities = pd.read_html("core/input_files/wikipedia_data.html")[1]
    cities = cities.loc[~cities['Metropolitan area'].str.contains("Totals")]
    cities = cities.rename(columns={'Metropolitan area': 'Metropolitan_area', 'Population (2016 est.)[8]': 'Population'})
    cities = cities[['Metropolitan_area', 'Population', 'NFL', 'MLB', 'NBA', 'NHL']]
    for k, v in {'\[.*\]': '', '': np.nan, '—': np.nan, 'Sox': ''}.items():
        cities = cities.replace(to_replace=k, value=v, regex=True)
    cities = cities[['Metropolitan_area', 'Population', f'{sport}']]
    cities = cities.dropna().reset_index(drop=True)

    # csv file data cleaning
    df = pd.read_csv(f"core/input_files/{filename}")
    df = df.loc[df['year'] == 2018]
    for c in ["Division", "AFC", "NFC"]:
        df = df.loc[~df['team'].str.contains(c)]
    for r in ["\*", "\(\d*\)", "\+"]:
        df['team'] = df['team'].replace(to_replace=r, value='', regex=True)
    df = df.reset_index(drop=True)

    # win/lose ratio calculation
    df[['W', 'L']] = df[['W', 'L']].astype(int)
    df['WL_Ratio'] = df['W'] / (df['W'] + df['L'])
    df = df[['team', 'WL_Ratio']]

    # dataframes preparation for merge
    df[['team0', 'team1', 'team2']] = df['team'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)
    cities[area_list] = cities[f'{sport}'].replace(r'([A-Z])', r' \1', regex=True).str.split(expand=True)

    # dataframes merge
    for a in area_list:
        cities = cities.merge(df[['WL_Ratio', 'team1']], how='left', left_on=a, right_on='team1')
        cities = cities.merge(df[['WL_Ratio', 'team2']].dropna(), how='left', left_on=a, right_on='team2')
        cities[f'WL_Ratio_{a}'] = cities[['WL_Ratio_x', 'WL_Ratio_y']].mean(axis=1)
        cities = cities.drop(['WL_Ratio_x', 'team1', 'WL_Ratio_y', 'team2'], axis=1)

    # avg_WL_Ratio calculation
    area_list = [f'WL_Ratio_{a}' for a in area_list]
    cities['avg_WL_Ratio'] = cities[area_list].mean(axis=1)
    cities = cities[['Population', 'avg_WL_Ratio']]

    # correlation calculation using stats library
    population_by_region = cities['Population'].astype(int).tolist()
    win_loss_by_region = cities['avg_WL_Ratio'].tolist()
    correlation = stats.pearsonr(population_by_region, win_loss_by_region)[0]
    print(f"for {sport} teams:", round(correlation, 5))
    return correlation
