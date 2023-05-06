from src.app.core.nhl import nhl_correlation


if __name__ == "__main__":
    print("The win/loss ratio's correlation with the population of the city:")
    print("for NHL teams:", nhl_correlation())
