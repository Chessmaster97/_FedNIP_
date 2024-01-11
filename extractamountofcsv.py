import pandas as pd

def extract_amount_from_csv():
    # Read the CSV file
    df = pd.read_csv('./partition-reports/clientsplittrain___.csv')

    # Extract the Amount column as a list
    amounts = df['Amount'].tolist()

    return amounts