  

# Design Specification

### By Campbell McTernan u7484835

  
  

## Overview

This project aims to implement an Artificial Intelligence (AI) agent to play the online board game Risk: Global Domination. Risk is a multiplayer diplomacy game with an objective to capture all territories on a map. Territories are captured from other players by attacking with dice rolls, and this non-determinism results in Risk having a state-space and game-tree complexity hugely exceeding games popular for AI such as Chess, Shogi, and Go [1]. Current academic work on Risk agents have primarily used techniques such as the Monte Carlo Tree Search (MCTS) and Machine Learning  [4, 5, 6, 7] with low success and subhuman performance attributed to this huge game complexity. Thus, this project will use the novel approach of "Action Abstraction": forcing the agent to select and evaluate handcrafted high-level strategies such as eliminating players or taking a continent. The agent will perform an Iterative Deepening Search (IDS) under time constraints to find the best combination of actions and will instruct the user on which moves to execute. This package will be implemented in Python and will provide a Command Line Interface (CLI) for interaction with the agent. Overall, the aim of this project will be to surpass all agents implemented for the game, and demonstrate a playing style which is enriching and balanced for high-level human play. 



## Risk: Global Domination

This design specification will assume intermediate knowledge in Risk and will not attempt to explain the game and strategies unless necessary. For a necessary introduction to the game, it is highly advisable to Michael Wolf's explanation of Risk in his thesis (pages 20-42) [1] and a concise recent literature review in J. Gillenwater's thesis (pages 30-37) [2]. Risk: Global Domination (RGD) is the most popular and recent addition to Hasbro's Risk franchise, and boasts a ruleset differing to the traditional game as described above. It is primarily played online with 4-6 players, with each player getting 60-180s per turn. RGD allows for huge variation on the original game including over 100 unique maps and mechanical variations to the dice, goals, maps and player communication. The crucial difference in RGD to every other Risk implementation studied is the introduction of "Balanced Blitz" dice. 

RGD denotes the traditional Risk system of attacking territories as having "True Random" dice. This ruleset is described aptly in section 1.3.3 of Gillenwater's thesis [2]. In this system, no territory attack will have certain victory, and any amount of troop loss is possible. This means that individual events in the game are very highly unpredictable. In contrast, standard configuration in RGD is "Balanced Blitz" dice which guarantees certainty for attacks with highly probable outcomes. In a nutshell, this configuration reduces or eliminates all extreme outcomes of attacks, rounding all attacks with >= 95% winning chances to  100% and all  <= 5% winning chances to 0% [3]. It also skews all troop loss outcomes toward the most likely result, so high probability attacks will lose less troops and low probability attacks will lose more troops. Other calculations are implemented to magnify this effect. Overall, this has huge implications as a 4v1 and 17v9 roll will certainly succeed and  a 3v11 attack will certainly fail. Although this does not affect the game's search-space or game-tree complexity, it significantly reduces non-determinism for agents with perfect play. 


## Aims 

This project aims to create a package running in the Command Line Interface (CLI) which can:

+ Provide an AI agent which can correctly play Risk games on a number of maps and settings

+ Interface with Risk: Global Dominations by instructing a user on all moves to execute

+ Evaluate a given game position, and calculate the sequence of moves an Action requires

+ Use an Iterative Deepening algorithm terminated by time limits to select combinations of Actions

+ Provide a debugging interface which with a visualises the agent's perceived gamestate


<p> For excellence in the agent's performance and competitive viability, this project aims to: </p>

  
+ Confidently beat all bots provided in the native game implementation, from difficulties "Beginner" to "Expert"

+ Implement non-deterministic actions to avoid being predictable to human players

+ Play with minimal positional blunders as analysed by a human expert

  


## Implementation

The bulk of the implementation has been scaffolded in the project code directory. Please see the files, functions and classes definitions and docstrings for more detailed specifications. This section will instead discuss the conceptual groundwork for the agent. 


### Action Abstraction

Action Abstraction is the key conceptual technique underpinning this agent. I will define an "action" to be a cohesive group of individual "moves" (such as attacking, drafting or fortifying to a single territory) with conceptual intent. This mimics the thought process of strong human players and provides a useful rubric to greatly simplify the calculation and evaluation of move sequences. The intent of this Action framework is to provide strict and discreet multi-move concepts which the agent can consider (such as killing a player), while still providing the capacity for the agent to play theoretically optimally given enough computational power and time. The draft list of actions the AI should consider is:






| Action | Description | Calculations |  
|--|--| -- | 
| *Kill a Player*|Agent eliminates a player| Finds the optimal pathing to capture all territories a player owns |
| *Take a bonus*| Agent captures all territories on a bonus to receive additional troops each turn| Finds the optimal pathing to capture all territories in the bonus| 
| *Break a bonus* | Agent captures one territory in an opponent's bonus, removing their additional troop reward| Finds pathing to capture the weakest border territory of bonus| 
|*Hit a stack* | A stack is terminology for a territory with a high concentration of troops. Agent uses attacking advantage to capture the territory, significantly whittling down the opponent's troops and crippling their ability to retaliate| Chooses key stack and finds pathing  |
| *Expand Bonus Borders*|A semi unique number representation of a board position for lightweight storage


### Data Structures

+ Utilise the Python NetworkX library to represent the agent's gamestate 

+ Implement the Python Click package for CLI use
(NetworkX, enums)

| Type | Data |

|--|--|

| ***Player***| A player is white or black|

| ***PieceType***| Denotes all standard chess pieces|

| ***Rank*** | Indicates the horizontal row component of a square location from White's perspective|

|***File*** | Indicates the vertical column component of a square location from White's perspective|

| ***HashBoard***|A semi unique number representation of a board position for lightweight storage

  

### Selection Algorithm


## Design Choices





## References

[1] Michael Wolf: An Intelligent Artificial Player for the Game of Risk

[2] Jacob Gillenwater: RISK Gameplay Analysis Using Stochastic Beam Search

[3] RGD Balanced Blitz Source code: https://github.com/smgstudio/risk-dice/tree/master 

[4] Rene G. Ferrari, Joaquim V. C. Assuncao: Towards playing Risk with a hybrid Monte Carlo based agent

[5] Simon Bethdavid: Zero-Knowledge Agent Trained for the Game of Risk

[6] Erik Blomqvist: Playing the Game of Risk with an AlphaZero Agent

[7] Lucas Gnecco Heredia, Tristan Cazenave: Expert Iteration for Risk