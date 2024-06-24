import click
from .interface import *
from .structures import GameState
from .riskAI import riskAgent
from .simpleAI import attackGraphSimple
from .multiAI import attackGraphMulti
from .randAI import randAI
from .drawInterface import drawArborescence



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
    click.echo("3. Test the single stack minimum arborescence algorithm on a static position")
    click.echo("4. Test the multi stack msa on a static position")
    click.echo("5. Evaluate a static position using the heuristic")
    click.echo("6. Use the debugging features for a variable player game")
    click.echo("7. <Misc to be added>")
    click.echo("8. Exit")
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
        
    

def msaSimpleDebug(gameState : GameState):
    # Outputs board for debugging
    drawBoard(gameState)
    # Gets list of territories to capture
    territories = getTerritories(gameState.map)
    # Gets simple attack graph
    attackGraph, stack, sumTroops = attackGraphSimple(gameState, territories)
    # Outputs results
    drawArborescence(gameState, attackGraph, 100)
    print("Min sum troops found is", sumTroops)
    click.echo("Finished drawing simple arborescence")

def msaMultiDebug(gameState : GameState):
    # Operates as simple msa. Currenlty not working.
    click.echo("NOTE: This function is broken as incorrect graph algorithm has been used to generate pathing. This will require further research. ")
    drawBoard(gameState)
    territories = getTerritories(gameState.map)
    attackGraph, stacks, sumTroops = attackGraphMulti(gameState, territories)
    drawArborescence(gameState, attackGraph, 300)
    print("Min sum troops found is", sumTroops)
    print("Stacks used are", stacks)

    click.echo("Finished drawing multi arborescence")


def heuristicEval(gameState : GameState):
    eval = heuristicEval(gameState)
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
            msaSimpleDebug(gameState)
        case 4:
            msaMultiDebug(gameState)
        case 5:
            heuristicEval(gameState)
        case 6:
            debugVariableGame(gameState)
        case 7:
            pass
        case 8:
            print("Exiting...")
    
    


if __name__ == "__main__":
    main()
