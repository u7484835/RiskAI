import click
from interface import getSetupInfo, instructTurn, displayGameover
from riskAI import riskAgent


def playOpponentsTurn():
    pass

def getUserTurn():
    action = riskAgent()
    instructTurn(action)
    pass

def main(blizzards : bool, fog : bool):
    # Handles CLI interactions implemented by click package
    getSetupInfo()
    # Loop placeholder for main game loop which handles all actions. Will terminate
    # once the player is eliminated or wins the game.
    while True:
        playOpponentsTurn()
        getUserTurn()
    displayGameover()
    