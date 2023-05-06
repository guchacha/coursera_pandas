from src.app.core.data_processing import data_processing_and_correlation


if __name__ == "__main__":
    print("The win/loss ratio's correlation with the population of the city:")
    data_processing_and_correlation(filename="nhl.csv", sport="NHL", area_list=['area1', 'area2', 'area3'])
    data_processing_and_correlation(filename="nba.csv", sport="NBA", area_list=['area1', 'area2'])
    data_processing_and_correlation(filename="mlb.csv", sport="MLB", area_list=['area1', 'area2'])
    data_processing_and_correlation(filename="nfl.csv", sport="NFL", area_list=['area1', 'area2'])
