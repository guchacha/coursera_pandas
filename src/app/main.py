from src.app.core.nhl import nhl_correlation
from src.app.core.nba import nba_correlation
from src.app.core.mlb import mlb_correlation
from src.app.core.nfl import nfl_correlation


if __name__ == "__main__":
    print("The win/loss ratio's correlation with the population of the city:")
    print("for NHL teams:", nhl_correlation())
    print("for NBA teams:", nba_correlation())
    print("for MLB teams:", mlb_correlation())
    print("for NFL teams:", nfl_correlation())
