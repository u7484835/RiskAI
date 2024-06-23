import pandas as pd
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the DiceData folder
dice_data_dir = os.path.join(current_dir, '..', 'DiceData')

# Read the CSV files using the constructed paths
minAttLostDf = pd.read_csv(os.path.join(dice_data_dir, 'MinAttLost.csv'), index_col=0)
avgAttLostDf = pd.read_csv(os.path.join(dice_data_dir, 'AvgAttLost.csv'), index_col=0)
perfDiceDf = pd.read_csv(os.path.join(dice_data_dir, 'PerfectDice.csv'))


def averageAttLost(attacking : int, defending : int) ->  int:
    return minAttLostDf.iloc[attacking, defending] 

def averageAttLost(attacking : int, defending : int) ->  float:
    return avgAttLostDf.iloc[attacking, defending] 
    
    
def perfectDice(defending : int) -> int:
    return perfDiceDf.loc[defending, 'Attackers']