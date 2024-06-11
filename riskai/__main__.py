import click
from .interface import *
from .structures import GameState
from .riskAI import riskAgent
from .randAI import randAI


def getAgentTurn(gameState : GameState, agentType : str) -> Move:
    match agentType:
        case "actionAI":
            return riskAgent(gameState)
        case "randAI":
            return randAI(gameState)
        case _:
            raise ValueError("Invalid agent type")
        

def funcPrompt() -> int:
    click.echo("Please select the mode with which you wish to use this agent")
    click.echo("1. Play a game with the strongest agent against other players")
    click.echo("2. Play a game with the random agent against other players")
    click.echo("3. Evaluate a static position using BFS")
    click.echo("4. Evaluate a static position using the heuristic")
    click.echo("5. Use the debugging features for a variable player game")
    click.echo("6. <Misc to be added>")
    click.echo("7. Exit")
    return click.prompt("Choice", type=click.IntRange(min=1, max=7))

def variableAgentGame(gameState : GameState, agentType : str):
    # recreating player list
    playerList = [player['colour'] for player in gameState.playerDict.values()]
    agentList = getAgentList(playerList)
    
    # Game loops infinitely until a player achieves victory
    while True:
        # Loops over all alive players
        for i in gameState.playersAlive:
            click.prompt(f"Press enter to to start {gameState.playerDict[i]['colour']}'s turn", default="", show_default=False, prompt_suffix='')

            # Agent players get AI moves
            if i in agentList:
                gameState.agentID = i
                move = getAgentTurn(gameState, agentType)
                winFlag = executeAgentTurn(move, gameState)
                # Exit loop if player wins
                if winFlag:
                    displayGameover(i, gameState)
                    return
                
            # Opponent players give system update of what's happened
            else:
                winFlag = getTurn(i, gameState)
                # Exit loop if opponent wins
                if winFlag:
                    displayGameover(i, gameState)
                    return
        gameState.round += 1
        
    

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
            variableAgentGame(gameState, "actionAI")
        case 2:
            variableAgentGame(gameState, "randAI")
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
