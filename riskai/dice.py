import pandas as pd

minAttLostDf = pd.read_csv('../DiceData/MinAttLost.csv', index_col=0)
avgAttLostDf = pd.read_csv('../DiceData/AvgAttLost.csv', index_col=0)
perfDiceDf = pd.read_csv('../DiceData/PerfectDice.csv')


def averageAttLost(attacking : int, defending : int) ->  int:
    return minAttLostDf.iloc[attacking, defending] 

def averageAttLost(attacking : int, defending : int) ->  float:
    return avgAttLostDf.iloc[attacking, defending] 
    
    
def perfectDice(defending : int) -> int:
    return perfDiceDf.loc[defending, 'Attackers']