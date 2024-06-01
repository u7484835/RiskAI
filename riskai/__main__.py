import click
from interface import getSetupInfo, instructTurn, displayGameover
from riskAI import riskAgent

def playRound():
    pass


def playOpponentsTurn():
    
    # remember when inidividual player attacks to check each time for termination
    pass

def getUserTurn():
    action = riskAgent()
    instructTurn(action)
    pass

def funcPrompt() -> int:
    click.echo("Please select the mode with which you wish to use this agent:")
    click.echo("1. Play a game with the agent against other players")
    click.echo("2. Play with a variable amount of agents and other players")
    click.echo("3. Evaluate a static position using BFS")
    click.echo("4. Evaluate a static position using the heuristic")
    click.echo("5. Use the debugging features for a variable player game")
    click.echo("6. <Misc to be added>")
    click.echo("7. Exit")
    return click.prompt("... \n", type=click.IntRange(min=1, max=7))


def singleAgentGame():
    pass

def variableAgentGame():
    pass

def bfsEval():
    pass

def heuristicEval():
    pass

def debugVariableGame():
    pass







def selectFunctionality():
    match funcPrompt():
        case 1:
            singleAgentGame()
        case 2:
            variableAgentGame()
        case 3:
            bfsEval()
        case 4:
            heuristicEval()
        case 5:
            debugVariableGame()
        case 6:
            pass
        case 7:
            print("Exiting...")


@click.command()
def main(blizzards : bool, fog : bool):
    # Handles CLI interactions implemented by click package
    getSetupInfo()
    # Loop placeholder for main game loop which handles all actions. Will terminate
    # once the player is eliminated or wins the game.
    while True:
        playOpponentsTurn()
        getUserTurn()
    displayGameover()
    