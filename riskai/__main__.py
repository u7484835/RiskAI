import click
from .interface import *
from .structures import GameState
from .riskAI import riskAgent
from .randAI import randAI


def playRound():
    pass


def playOpponentsTurn():
    
    # remember when inidividual player attacks to check each time for termination
    pass

def getAgentTurn(gameState : GameState) -> bool:
    move = randAI(gameState)
    executeAgentTurn(move, gameState)

def funcPrompt() -> int:
    click.echo("Please select the mode with which you wish to use this agent")
    click.echo("1. Play a game with the agent against other players")
    click.echo("2. Play with a variable amount of agents and other players")
    click.echo("3. Evaluate a static position using BFS")
    click.echo("4. Evaluate a static position using the heuristic")
    click.echo("5. Use the debugging features for a variable player game")
    click.echo("6. <Misc to be added>")
    click.echo("7. Exit")
    return click.prompt("Choice", type=click.IntRange(min=1, max=7))


def singleAgentGame(gameState : GameState):
    # Game loops infinitely until a player achieves victory
    while True:
        # Loops over all alive players
        for i in gameState.playersAlive:
            # Agent players get AI moves
            if i == gameState.agentID:
                getAgentTurn()
                winFlag = executeAgentTurn()
                # Exit loop if player wins
                if winFlag:
                    displayGameover(i)
                    return
                
            # Opponent players give system update of what's happened
            else:
                winFlag = getTurn(i, gameState)
                # Exit loop if opponent wins
                if winFlag:
                    displayGameover(i)
                    return
                
        gameState.round += 1

def variableAgentGame(gameState : GameState):
    # recreating player list
    playerList = [player['colour'] for player in gameState.playerDict.values()]
    agentList = getAgentList(playerList)
    
    # Game loops infinitely until a player achieves victory
    while True:
        # Loops over all alive players
        for i in gameState.playersAlive:
            click.echo(f"It is {gameState.playerDict[i]['colour']}'s turn")
            # Agent players get AI moves
            if i in agentList:
                gameState.agentID = i
                getAgentTurn()
                winFlag = executeAgentTurn()
                # Exit loop if player wins
                if winFlag:
                    displayGameover(i)
                    return
                
            # Opponent players give system update of what's happened
            else:
                winFlag = getTurn(i, gameState)
                # Exit loop if opponent wins
                if winFlag:
                    displayGameover(i)
                    return
        
    

def bfsEval():
    pass

def heuristicEval():
    pass

def debugVariableGame():
    pass    


@click.command()
def main():
    # Initialises gamestate which holds all relevant info 
    # about game in progress
    gameState = setupGameState()
    
    # Chooses and executes desired game functionality
    match funcPrompt():
        case 1:
            singleAgentGame(gameState)
        case 2:
            variableAgentGame(gameState)
        case 3:
            bfsEval(gameState)
        case 4:
            heuristicEval(gameState)
        case 5:
            debugVariableGame(gameState)
        case 6:
            pass
        case 7:
            print("Exiting...")
    
    


if __name__ == "__main__":
    main()
