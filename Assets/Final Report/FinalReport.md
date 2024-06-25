# Action Oriented AI for Risk: Global Domination

### By Campbell McTernan u7484835

## Abstract
This project aimed to implement "ActionAI": an Artificial Intelligence (AI) agent to play the online board game Risk: Global Domination (RGD). Risk is a multiplayer diplomacy game with an objective to capture all territories on a map.  Territories are captured from other players by attacking with dice rolls, and this non-determinism results in Risk having a state-space and game-tree complexity hugely exceeding games popular for AI such as Chess, Shogi, and Go [1]. Current academic work on Risk agents have primarily used techniques such as the Monte Carlo Tree Search and Machine Learning  [4, 5, 6, 7] with low success and subhuman performance attributed to this huge game complexity. 

To innovate on this strategy, this paper presents the novel approach of "Action Abstraction", in which agents search and calculate moves based on high-level handcrafted such as eliminating players or taking a bonus on the map. The agent was proposed to utilise an Iterative Deepening Search (IDS) under time constraints to find the optimal combination of actions and will instruct the user on which moves to execute. ActionAI was implemented in Python, and provided an extensive Command Line Interface (CLI) for textual representation of the game state with support for visual output of the board attack pathing. The goal of the project was for ActionAI to surpass all agents implemented in the existing game package. Overall, due to time constraints and the complexities of implementing a handcrafted agent, no working copy of ActionAI was created. Despite this, the project achieved moderate success in the creation of the first public interface for development of agents for RGD, with a strong library of functions developed to implement ActionAI in the future. 


## Introduction

Risk: Global Domination is a videogame developed by SMGStudio in 2015, which digitises and expands upon the classic board game created in the 1950's. The traditional game supports 2-6 players and takes place on a global map broken into 42 territories which are initially assigned to random players and are occupied by their troops. Taking turns, players receive troop income based on their amount of territories and "bonus" troops for owning continents. A player wins the game by capturing all territories on the board, which is achieved by attacking the territories with troops using a system based on dice rolls. Although SMGStudio's implementation of RGD has limited communication, gameplay is highly dependant on diplomacy and player relations. In recent years, the game has found huge online success with prize money tournaments featuring thousands of players. RGD typically allows users 60-120 seconds to complete a turn, and thus games often last 0.5-3 hours. Due to the slow nature of play, almost every game has one or most players leaving early, and for fairness Risk's AI agents command these players after departure. As this has significant effects on the outcomes of competitive games with cash stakes, the nature of the agents in RGD is very important.

## Background 
### Risk: Global Domination
For brevity, this report will assume working knowledge at an intermediate level of the rules, gameplay and strategy of Risk. For a practical academic introduction to the ruleset, it is highly recommended to read M. Wolf's explanation of Risk in his landmark paper given in Reference [1] pg 20-42. References [11] and [12] respectively give an overview of current strategy, and a former World Champion's  beginner's guide. Gillenwater's paper [2] pg 30-37 is also recommended as a concurrent literature review of progress in AI agent strategies explored in the game. It should be noted that RGD supports a wide variety of  additions and customisations to the original Risk game, including over 100 unique maps, variations to the dice mechanics, game mode goals, and information provided. For a manageable scope on the project, the ActionAI agent has been implemented with a ruleset closely following the traditional game: with the settings "Fixed Cards, No Fog, No Portals, No Capitals, No Blizzards, Automatic Troop Placement, and Balanced Blitz dice". This exactly the same as ruleset described in Wolf's paper except for Balanced Blitz dice which are a new addition to RGD and entirely changes conclusions and strategy about gameplay. This ruleset has been chosen it mirrors the majority of online games. 


### Risk Bots
As RGD is a recent online game with no api, nor support for any controls input other than a mouse-based GUI, there are no community implementations for artificial agents. Hence, the only non-human agents capable of playing RGD are the agents (named bots) implemented by the game studio. These bots have a "difficulty" indicative of playing strength from "Beginner" to "Expert" and have been revealed by SMGStudio to have 40 attributes [8] affecting their "persona" and playstyle. As can be seen in gameplay [9], even the strongest agents act greedily: it is my strong belief that the bots behave without search functions. Their behaviour can be described as follows:

+ **Aggression**: According to their persona, the aggression of the bots varies wildly, although all expert bots attack far more frequently than skilled players. Due to quirks in the RDG's attacking system, for every number of defending troops there is an amount of troops to attack with which guarantees success and minimises average troop loss. The bots do not use "perfect dice" amounts to achieve this, and often attempt battles with a 60% win chance which is very poor play. 
+ **Stack Placement**: All bots have the strong tendency to place troops and attack territories towards areas with high troops. This can clearly be seen in Reference [9], and manifests like an attraction to "stacks" (territories with high troops). In combination with the tendency to attack territories given a low win chance, the movement pattern of bots is to continually disperse in blotches towards opponent stacks and bonuses. 
+ **Bonuses and Diplomacy**:  Bots tend to move greedily towards capturing bonuses and intentionally break other player's bonuses in close proximity. When capturing territories, bots have no conception of diplomacy with other players. They are incapable of direct retaliation. They are also unaware of creating hostilities by capturing territories or bonuses. 

As the current bots appear to move greedily to achieve their hidden metrics (owning territories, bonuses, and placing stacks adjacent to other players) gameplay even using the most advanced AI can be quite static. As shown in Reference [9], skilled players often manipulate the bots to gain a competitive advantage over other players, but even an intermediate player would never feel threatened or excited by playing bots. This is acknowledged by the developers, as an in-game challenge is to defeat the most difficult bot which has double the troops as shown in Figure -(chalGame). With a suite of AI agents in which the bot of pinnacle playing strength is given 2-1 odds to make a challenging game, combined with the static, search-less, and undiplomatic nature of the agents leaves a significant for innovation.

## ActionAI 
### Research Analysis
With the exception of Johansson's Multi Agent system [15] which saw small success, almost all publications of research into Risk agents have used a Monte Carlo Tree Search (MCTS) [1, 2, 4, 5, 6, 7, 15] with minimal results. Worse yet, Wolf's agent (developed in 2006) is the only model which could exceed average human capacity at the game [1]. As this research has occurred in a revitalised competitive gaming scene, it is unlikely that Wolf's agent would be as strong as a modern player two decades later. 

With the popular rise of machine learning, several recent publications into Risk agents attempted several methods, including Zero Learning [6], Expert Iteration [7] and a Stochastic Beam Search [2]. These approaches largely ended in failure as the Zero Learning agent "did however not improve with further iterations of network training" [6], while the Beam Search "cannot create contingencies that allow for effective strategy across multiple turns" [2]. Furthermore, "on more complex phases like attacking" the Expert Iteration Agent had "no clear signs of learning" [7] . 

Overall, I believe results in the development of agents playing Risk is quite poor. As shown in Figure -(complexTab), the game tree complexity of Risk is so staggeringly large that MCTS agents struggle heavily to search any meaningful depth into future events. Furthermore, in a true 6-player game, the true outcomes for play become close to random. A particular problem with the machine learning attempts is that as gameplay is dependant on diplomacy, self-learning agents in enclosed learning systems merely find a diplomatic equilibrium rather than strong individual play. 

Risk's game tree complexity is largely the product of the dice mechanics of the traditional Risk game. With the introduction of Balanced Blitz dice to RGD (which allows for certain attacking results and heavily pruned variance), if the assumption of perfect dice choices is implemented many handcrafted MCTS systems may perform significantly better. I would estimate the game tree complexity would be reduced to values similar to Go. So far, all considerations of search and moves focus on the action of capturing a single territory, and the individual dice rolls associated with that attack. This is a naïve approach as each territory is considered for its isolated merit, whereas strong human players reason about all moves with sophisticated conceptual goals to far surpass machine performance. To improve the search space problem further, I propose that agents should search and evaluate a state space of Risk based on concrete plans or objectives. 

### Abstract Actions
My own experience of the Risk game has come from hundreds of hours of viewership of narrated World-Champion level play. I have also achieved the Master ranking on RGD (this puts me in the top <2% of players). When advanced human players strategize about the game 


In Risk, a player's turn is comprised of a Draft, Attack, and Fortify phase. An abstraction action is defined to be a sequence possible troop drafts, individual territory attacks and a fortification which achieve a broader conceptual purpose such as eliminating a player, 



As shown in Wolf and Brand's research, the highest performing agents by far had a 






## RiskAI
### Aims
The RiskAI project aimed to address the ineptitude of the current Artificial Intelligence agents implemented within the RGD game by providing a package which could:
+ Provide a stand-alone project to host and represent Risk games by interfacing with a Command Line Interface (CLI)
+ Allow for local representation and agent suggestions of online games from the RGD server, using human input to execute actions in-game and to notate online opponent's moves
+ Visually display game positions for any variety of maps and communicate abstract action concepts
+ Evaluate positions based on qualitative board metrics and diplomatic considerations
+ Provide a debugging interface with detailed outputs of internal data
+ Implement an agent which generates, searches and calculates abstract actions which follow intelligent hand-crafted move sequences
<p> To achieve excellence in Agent's results, the goals were to: </p>
+ Exceed the playing strength of all bots provided in the native game implementation, from difficulties "Beginner" to "Expert"
+ Implement non-deterministic actions to avoid being predictable to human players
+ Interact dynamically and diplomatically with players, forming trust and enacting vengeance

### Project Structure and Dependencies
Heirarchy, function design

Packages, Solutions

## Implementation 
### Data structures
For its core evaluations, this package uses the following atomic types specified in ChessAI.Structures.lean:

| Type | Data |
|--|--|






























| ***Player***| A player is white or black|
| ***PieceType***| Denotes all standard chess pieces|
| ***Rank*** | Indicates the horizontal row component of a square location from White's perspective|
|***File*** | Indicates the vertical column component of a square location from White's perspective|

  

These atomic types are primarily used in more complex structures for calculation:

| Type | Purpose|
|--|--|
| ***Piece*** | Denotes a piece with owner information|
| ***Square***| Represents a single chessboard tile which is either empty or occupied by a piece|
| ***Location*** | Uses rank and file components to specify a unique square on the board such as e4|
| ***PieceLoc***| Specifies a PieceType-Location pair with implicit player ownership|
|***PieceList***| An *array* of PieceLocs denoting all the pieces a player owns and their position for quick access |
| ***Promotion*** | The PieceType a pawn is promoted to in moves if valid |
| ***Move*** | Encodes the 'long notation' for a move including the PieceType, start and finish locations and potential promotions[9] |
| ***En Passant*** | The destination location of En Passant if possible |


Other important types include the various abstractions of the chessboard:
 
| Type | Abstraction| Use Case|
|--|--| -- |
| ***ArrayOfN*** | Atomic structure to implement 2D array| Implements an indexed family for fixed length Arrays, a counterpart to 'Vector'|
| ***EightByEight*** | Base type of an 8x8 array |Allows both Board and Heuristic value representation |
| ***Board*** |2D array of 8x8 squares to form literal board |To be looped on for heuristics and move generation|
| ***BoardState***|Includes *board* and game variables including the player's turn and piece lists | Main piece of data handled by the NegaMax algorithm for move generation and evaluation. Serves as the bridge between the backend and front end of the program. |

 

### Control flow

### Interface

### RandAI

### ActionAI 
ids, timeout, simple


## Design

### Style 
+ Overcommented as it is  meant to be a public work for community use
+ Internal documentation varies
+ 

### Code Quality
+ In some places very high. Design of gamestate, playerdict, maps is very good. Use of type aliases is good 
+ Action file is very poor. Action classes were created but not utilised correctly at all. Type enums made things quite confusing 

### Development Notes
As can be seen by comparing this final report to the initial design specification, major changes to the project were made during development. Important changes include: 
+ **Search algorithm** : I changed from believeing IDS would be suitable to bfs. The main predicited limitation of computation was the space of having graph gamesates. Furthermore, 
+ **Sequential Nodes vs Action Sequences**: Originally wanted to enact actions in normal path, one after the other. Because of pathing this does not work at all
+ **Attack pathing**: Way harder than it seemed

### Challenges 

**Territory Representation** 

**Package integration** 

+ Dice package: risk-dice compile
+ Attack trees, msa/tsp/mst
+ complexity

## Evaluation and Testing 

This section should be clearly prefaced with the simple fact that the engine strength is quite poor. In fact, significant bugs have been found in the move generation system, so the system does not even correctly implement the stated rules correctly. The main points to consider are as follows: 

**As a package:**


**As an implementation of the chess game**


**As a chess engine** 



## References
Sample Evaluation for Action Selection in Monte Carlo Tree Search

[1]  Wolf, M. (2005) An Intelligent Artificial Player for the Game of Risk.
[2]   Gillenwater, J. (2022) RISK Gameplay Analysis Using Stochastic Beam Search.
[3]  SMG Studio (2021) RGD Balanced Blitz Source code. Available at: [https://github.com/smgstudio/risk-dice/tree/master](https://github.com/smgstudio/risk-dice/tree/master) (Accessed: 17 April 2024).
[4]   Ferrari, R.G. and Assuncao, J.V.C. (2022) Towards playing Risk with a hybrid Monte Carlo based agent.
[5]   Bethdavid, S. (2020) Zero-Knowledge Agent Trained for the Game of Risk.
[6]   Blomqvist, E. (2020) Playing the Game of Risk with an AlphaZero Agent.
[7]   Heredia, L.G. and Cazenave, T. (2022) Expert Iteration for Risk.
[8] SMGStudio (2021). _Our RISK AI_. [online] SMG Studio. Available at: https://smgstudio.freshdesk.com/support/solutions/articles/11000077687-our-risk-ai.
[9] https://youtu.be/9vgiZwV6kR8?si=nAo3P-6Snzx7l8vF
[10] jack678899 (2022). _Balanced Blitz calculator and data_. [online] Google Sheets. Available at: https://docs.google.com/spreadsheets/d/1Htk4vaXqNWsKDU7oSoeqbENLp_MjDKSxKXyL1W7rTHk/edit?usp=sharing [Accessed 22 Jun. 2024].
[11] Legendary Tactics (2022). _RISK Strategy Guide - Top 10 Tips_. [online] YouTube. Available at: https://youtu.be/Ltf7NldY-Nc?si=qKgnRjStPI0gvsLa [Accessed 22 Apr. 2024].
[12] The Kill Pete Strategy (2022). _How to Play Risk! Tutorial for Beginners_. [online] YouTube. Available at: https://youtu.be/y-ESVSkkMus?si=QAbui0XRvhUoETei [Accessed 15 Mar. 2024].
[13] jack678899 (2022b). _Calculation Method Balanced Blitz Troop Losses_. [online] Google Docs. Available at: https://docs.google.com/document/d/1LL5Q6mZISZgMyPm1E4i9g-RlENYeFzzD9yL8YXEnpDo/edit?usp=sharing [Accessed 18 Jun. 2024].
[14] Risk: Global Domination Wiki (2022). _Everything You Need to Know about Zombies!_ [online] Available at: https://risk-global-domination.fandom.com/wiki/Everything_you_need_to_know_about_Zombies! [Accessed 29 Apr. 2024].
[15] Johansson, S.J. (2014). Using Multi-Agent System Technology in Risk Bots. Proceedings of the Second Artificial Intelligence and Interactive Digital Entertainment Conference. ResearchGate.
[16] Brand, D. and Kroon, S. (2014). Sample Evaluation for Action Selection in Monte Carlo Tree Search. doi:https://doi.org/10.1145/2664591.2664612.

## Appendix 
I would also highly recommend you view the function comments in the code artifact. 
![Minimal Hierarchy chart](assets/HeirArchyTableFull.pdf)