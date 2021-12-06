import pandas as pd


def processdata(fileToProcess):
    # Loading and reading the CSV file.
    df = pd.read_csv(fileToProcess, delimiter =',')
    # Converting the CSV data to a list.
    df = df.to_dict(orient = 'records')
    return df