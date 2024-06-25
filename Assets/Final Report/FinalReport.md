


  

# Action Oriented AI for Risk: Global Domination

### By Campbell McTernan u7484835

## Abstract
This project aimed to implement "ActionAI": an Artificial Intelligence (AI) agent to play the online board game Risk: Global Domination (RGD). Risk is a multiplayer diplomacy game with an objective to capture all territories on a map.  Territories are captured from other players by attacking with dice rolls, and this non-determinism results in Risk having a state-space and game-tree complexity hugely exceeding games popular for AI such as Chess, Shogi, and Go [1]. Current academic work on Risk agents have primarily used techniques such as the Monte Carlo Tree Search and Machine Learning  [4, 5, 6, 7] with low success and subhuman performance attributed to this huge game complexity. 

To innovate on this strategy, this paper presents the novel approach of "Action Abstraction", in which agents search and calculate moves based on high-level handcrafted such as eliminating players or taking a bonus on the map. The agent was proposed to utilise an Iterative Deepening Search (IDS) under time constraints to find the optimal combination of actions and will instruct the user on which moves to execute. ActionAI was implemented in Python, and provided an extensive Command Line Interface (CLI) for textual representation of the game state with support for visual output of the board attack pathing. The goal of the project was for ActionAI to surpass all agents implemented in the existing game package. Overall, due to time constraints and the complexities of implementing a handcrafted agent, no working copy of ActionAI was created. Despite this, the project achieved moderate success in the creation of the first public interface for development of agents for RGD, with a strong library of functions developed to implement ActionAI in the future. 


## Introduction

Risk: Global Domination is a videogame developed by SMGStudio in 2015, which digitises and expands upon the classic board game created in the 1950's. The traditional game supports 2-6 players and takes place on a global map broken into 42 territories which are initially assigned to random players and are occupied by their troops. Taking turns, players receive troop income based on their amount of territories and "bonus" troops for owning continents. A player wins the game by capturing all territories on the board, which is achieved by attacking the territories with troops using a system based on dice rolls. Although SMGStudio's implementation of RGD has limited communication, gameplay is highly dependant on diplomacy and player relations. In recent years, the game has found huge online success with prize money tournaments featuring thousands of players. RGD typically allows users 60-120 seconds to complete a turn, and thus games often last 0.5-3 hours. Due to the slow nature of play, almost every game has one or most players leaving early, and for fairness Risk's AI agents command these players after departure. As this has significant effects on the outcomes of competitive games with cash stakes, the nature of the agents in RGD is very important.

<p  align="center">  <img src="https://i.ibb.co/hYD4LwG/stock.jpg" alt="enter image description here" width="650" /> </p>
<p> Figure 1. Risk: Global Domination by SMGStudio </p>


## Background 
### Risk: Global Domination
For brevity, this report will assume working knowledge at an intermediate level of the rules, gameplay and strategy of Risk. For a practical academic introduction to the ruleset, it is highly recommended to read M. Wolf's explanation of Risk in his landmark paper given in Reference [1] pg 20-42. References [11] and [12] respectively give an overview of current strategy, and a former World Champion's beginner's guide. Gillenwater's paper [2] pg 30-37 is also recommended as a concurrent literature review of progress in AI agent strategies explored in the game. It should be noted that RGD supports a wide variety of  additions and customisations to the original Risk game, including over 100 unique maps, variations to the dice mechanics, game mode goals, and information provided. For a manageable scope on the project, the ActionAI agent has been implemented with a ruleset closely following the traditional game: with the settings "Fixed Cards, No Fog, No Portals, No Capitals, No Blizzards, Automatic Troop Placement, and Balanced Blitz dice". This exactly the same as ruleset described in Wolf's paper except for Balanced Blitz dice which are a new addition to RGD and entirely changes conclusions and strategy about gameplay. This ruleset has been chosen it mirrors the majority of online games. 


<p  align="center">  <img src="https://i.ibb.co/dM5QspQ/Bonus-Amouts.png" alt="enter image description here" width="650" /> </p>
<p> Figure 2. Bonus values on the Classic map </p>


### Risk Bots
As RGD is a recent online game with no api, nor support for any controls input other than a mouse-based GUI, there are no community implementations for artificial agents. Hence, the only non-human agents capable of playing RGD are the agents (named bots) implemented by the game studio. These bots have a "difficulty" indicative of playing strength from "Beginner" to "Expert" and have been revealed by SMGStudio to have 40 attributes [8] affecting their "persona" and playstyle. As can be seen in gameplay [9], even the strongest agents act greedily: it is my strong belief that the bots behave without search functions. Their behaviour can be described as follows:

+ **Aggression**: According to their persona, the aggression of the bots varies wildly, although all expert bots attack far more frequently than skilled players. Due to quirks in the RDG's attacking system, for every number of defending troops there is an amount of troops to attack with which guarantees success and minimises average troop loss. The bots do not use "perfect dice" amounts to achieve this, and often attempt battles with a 60% win chance which is very poor play. 
+ **Stack Placement**: All bots have the strong tendency to place troops and attack territories towards areas with high troops. This can clearly be seen in Reference [9], and manifests like an attraction to "stacks" (territories with high troops). In combination with the tendency to attack territories given a low win chance, the movement pattern of bots is to continually disperse in blotches towards opponent stacks and bonuses. 
+ **Bonuses and Diplomacy**:  Bots tend to move greedily towards capturing bonuses and intentionally break other player's bonuses in close proximity. When capturing territories, bots have no conception of diplomacy with other players. They are incapable of direct retaliation. They are also unaware of creating hostilities by capturing territories or bonuses. 

As the current bots appear to move greedily to achieve their hidden metrics (owning territories, bonuses, and placing stacks adjacent to other players) gameplay even using the most advanced AI can be quite static. As shown in Reference [9], skilled players often manipulate the bots to gain a competitive advantage over other players, but even an intermediate player would never feel threatened or excited by playing bots. This is acknowledged by the developers, as an in-game challenge is to defeat the most difficult bot which has double the troops as shown in Figure 3. With a suite of AI agents in which the bot of pinnacle playing strength is given 2-1 odds to make a challenging game, combined with the static, search-less, and undiplomatic nature of the agents leaves a significant for innovation.

<p  align="center">  <img src="https://i.ibb.co/7rQH2T5/challenge-Game.png" alt="enter image description here" width="650" /> </p>
<p> Figure 3. One vs All Challenge against RGD bot </p>


## ActionAI 
### Research Analysis
With the exception of Johansson's Multi Agent system [15] which saw small success, almost all publications of research into Risk agents have used a Monte Carlo Tree Search (MCTS) [1, 2, 4, 5, 6, 7, 15] with minimal results. Worse yet, Wolf's agent (developed in 2006) is the only model which could exceed average human capacity at the game [1]. As this research has occurred in a revitalised competitive gaming scene, it is unlikely that Wolf's agent would be as strong as a modern player two decades later. 

With the popular rise of machine learning, several recent publications into Risk agents attempted several methods, including Zero Learning [6], Expert Iteration [7] and a Stochastic Beam Search [2]. These approaches largely ended in failure as the Zero Learning agent "did however not improve with further iterations of network training" [6], while the Beam Search "cannot create contingencies that allow for effective strategy across multiple turns" [2]. Furthermore, "on more complex phases like attacking" the Expert Iteration Agent had "no clear signs of learning" [7] . 




<p  align="center"> <img src="https://i.ibb.co/84hXTMm/table.png" alt="enter image description here" width="650" /> </p>
<p> Figure 4. Wolf's comparison of game complexity [1] </p>



Overall, I believe results in the development of agents playing Risk is quite poor. As shown in Figure 4, the game tree complexity of Risk is so staggeringly large that MCTS agents struggle heavily to search any meaningful depth into future events. Furthermore, in a true 6-player game, the true outcomes for play become close to random. A particular problem with the machine learning attempts is that as gameplay is dependant on diplomacy, self-learning agents in enclosed learning systems merely find a diplomatic equilibrium rather than strong individual play. 

Risk's game tree complexity is largely the product of the dice mechanics of the traditional Risk game. With the introduction of Balanced Blitz dice to RGD (which allows for certain attacking results and heavily pruned variance), if the assumption of perfect dice choices is implemented many handcrafted MCTS systems may perform significantly better. I would estimate the game tree complexity would be reduced to values similar to Go. So far, all considerations of search and moves focus on the action of capturing a single territory, and the individual dice rolls associated with that attack. This is a naïve approach as each territory is considered for its isolated merit, whereas strong human players reason about all moves with sophisticated conceptual goals to far surpass machine performance. To improve the search space problem further, I propose that agents should search and evaluate a state space of Risk based on concrete plans or objectives. 

### Strategy 

As a Risk hobbyist, I chose this project because I believe I have a unique position as an advanced-intermediate player and developer. Primarily, I have enjoyed Risk by watching hundreds of hours of narrated World-Champion level gameplay. In competition I have also achieved the Master ranking which puts me in the top <2% of players. When strategizing about the game, advanced human players tend to discard a very significant amount of information when making decisions. For example, when considering the moves of an opponent, I need to consider whether they could break the defensive border built around my territories: my opponent capturing neutral or uncontested territories is largely irrelevant. Furthermore, a defining feature of human play which is far stronger than AI play is the concept of "stacking". As shown in Figure 6, the pink player is stacking their troops at the chokepoint to the Australia bonus as their internal territories do not need defence. As pink has a significant amount of troops on a single territory, if they desire to capture all territories in a bonus, or eliminate a player, they can make sequential attacks with the same stack, using the troop advantage for very favourable odds. It also provides significant defensive capabilities. To achieve any chance at eliminating the player, the opponent must also have a stack of similar size for a favourable attack. 


When viewed on a high level, the Draft, Attack, and Fortify phases of a turn have very unique characteristics affecting gameplay. In a turn an unlimited amount of attacks may be made, which have the side effect of moving troops across territories. As only a single fortification can be made, control of troop distribution between territories is quite limited. This mechanic dominates gameplay considerations, as attacking must be used as the primary method to control troop flow. Attacking a sequence of territories to capture one or many desired locations in an intelligent way is called "pathing": for an example of this advanced gameplay see a game by the former world champion in Reference [17]. When abstracted, a turn is an opportunity to acquire valuable territories (perhaps to complete a bonus or deny an opponent from taking one) with a draft to prepare a the stack, attacks to utilise the stack along a favourable path, and a fortification to recall troops or expand defensible borders. These strategies is a key factor separating the current capabilities of RGD bots, as they have no concept of weak points, defending territories, or actively eliminating players. 


### Abstract Actions
An abstraction action is defined to be a sequence possible troop drafts, individual territory attacks and a fortification which achieve a broader conceptual purpose which can be achieved in a single turn, or short number of turns. This is very similar to Wolf's "Plans" strategy, which saw huge success in his agent [1]. Replacing the previous methods of using a MCTS to search the the game tree comprising of every draft, attack, and fortify, as well as every dice outcome, ActionAI is proposed to search on the space of these useful action sequences. For simplicity, this project focused on developing an agent which searched only on its actions, intending for a sufficient heuristic to statically ensure the agent has a sufficient defence rather than calculating possibilities of incoming attacks. A comprehensive list of possible conceptual actions to take is as follows:

| Action | Purpose|
|--|--|-- |
| ***Eliminate a Player*** | Remove a player from the game by capturing all territories|
| ***Take a Bonus***| Capture all territories in a bonus to increase troop income|
| ***Break a Bonus*** | Capture a territory in a bonus owned by the opponent to deny their troop income|
| ***Expand Bonus Borders***|Chooses and captures more defensible chokepoints for territory borders, or moves towards capturing another bonus.|
|***Chip a Player***| Attack a player using favourable odds to decrease their troops|
| ***Defend Bonus Borders*** | Evaluates bonus borders of high risk of being attacked and increases troops to dissuade aggression. |
| ***Migrate Position*** | Move the majority of troops to a more favourable location on the map |
| **Take a Card** | Attacks a single territory with low troops to ensure a card is taken.|
| ***Take Territories*** | Take adjacent territories in an uninformed way. This is a catch-all action which when calculated at sufficient depth should encompass all possible move sequences. |
| ***No Attack*** | Conserve troops by avoiding battle |

### Action Sequencing
The action abstraction system reduces the state space complexity to trivially small proportions but creates huge complexity for planning, calculation, and assessment of actions. Correctly searching and sequencing actions is tremendously important, as in a two player game it is vital to break all of an opponent's bonuses if possible. This is shown in RGD's custom challenge in Figure 2, for which players must take advantage of the inactive expert bot to generate more troops and win the game.  A naïve approach to searching the space of actions is to calculate an action, generate the resulting game state and then search that game state for favourable nodes. As stacks must traverse the map to capture territories, this approach will often lead to displaced troops which cannot execute multiple actions. This approach also does not account for calculating the Draft and Fortify moves, which occur once.

Creating a robust algorithm to calculate action sequencing was by far the most difficult and complex part of this project, and a separate publication could easily be made discussing the solution details. As the key function of actions is to capture territories, and territories can be captures in any sequence, <u>general</u> functions calculating the specific moves to execute each phase can be found. An action sequence is then considered to be equivalent to a set of territories to capture, with optional bonus stipulations like troop migration deciding the fortify or draft output. Thus, action sequencing is implemented by creating a union of all objectives, and ActionAI agents have the capability to simultaneously pursue multiple goals in a turn. To search through action sequences, an Iterative Deepening Search (IDS) was chosen to cater to time constraints. The "depth" of the search corresponds to the amount of actions attempted in unison, with the optimal output moves and evaluation returned at cut-off. 


<p  align="center">  <img src="https://i.ibb.co/yyknsZr/Pathing1.png" alt="enter image description here" width="650" /> </p>
<p>  Figure 5. Example of Abstraction Action: Take Asia Bonus </p>

<p  align="center">  <img src="https://i.ibb.co/x5MgdT7/bonus2.png" alt="enter image description here" width="650" /> </p>
<p> Figure 6. Example of Abstraction Action: Take Europe Bonus  </p>


## Project Implementation 
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

<p  align="center">  <img src="https://i.ibb.co/KqjbBDV/Game-Output1.png" alt="enter image description here" width="650" /> </p>
<p> Figure 7. Display output for the game state </p>


### Dependencies and Data structures

The RiskAI project utilises the following dependencies:

| Package| Justification|
|--|--|
| ***NetworkX***| Risk maps consist of interconnected territories best represented by graphs. As handcrafted calculations require significant computations, performance is desired.|
| ***Click***| The project interface requires extensive CLI usage. |
| ***Poetry*** | As the package is intended for ongoing community development, installing and running the package should be ergonomic. |
|***MatPlotLib*** | The board state and attack pathing are necessary to display intuitively. |


For its core evaluations, this package uses the following types and objects specified in *structures.py*:

|Name | Type | Purpose|
|--|--|--|
| ***CardType***| Enum| Represents different card types gained after capturing a territory|
| ***Card***| Class | Object representing a card held by the agent.|
| ***Trade*** | Alias | Represents the move to specific 3 cards to trade in. |
|***Draft*** | Alias | Represents a list of locations and amounts to place troops. |
|***Attack*** | Alias | Represents a list of territory capture instructions. |
|***Fortify*** | Alias | Represents the internal transfer of troops. |
|***Move*** | Alias | Encodes the instructions to a player to execute a full turn.|
|***Territories*** | Alias | Holds a set of territory locations on the map.|
|***GameState*** | Class | Contains all game information for search, display and interfacing. |

The GameState encapsulates all information about a given game, and contains the fields:
|Name | Type | Purpose|
|--|--|--|
| ***Map***| Map| Class containing the graph of territories, bonus information, and values for display|
| ***AgentID***| int | Denotes the current agent playing. Can be modified during runtime to act as different players each turn|
| ***Round*** | int | Amount of turns the first player taken |
|***PlayerDict*** | Dictionary| Stores all details about each player in the game, including troop metrics and style inferences.|
|***PlayersAlive*** | list[int] | Iterator for players who still own territories |
|***RelationShipMatrix*** | list[list[int]]| Represents the trust/aggression player ID x feels toward player ID y at entry (x, y). Note: this functionality was not implemented|
|***Cards*** | list[card]| A list of cards held by the agent player, as only agent cards are seen. |

<p  align="center"> <img src="https://i.ibb.co/CHSsxzk/folders2.png" alt="enter image description here" width="450" /> </p>

<p  align="center">  <img src="https://i.ibb.co/YdT3QCz/4y4y.png" alt="enter image description here" width="570" /> </p>

<p> Figure 8. Above: Folder Directory for RiskAI project, Below: Hierarchy Chart for  main functions in project</p>



### Control flow
The project is executed from the *run_riskAI.py* file, which executes the *main* function in *\_\_main\_\_.py*. With simple CLI interaction, *main* gets the choice of program functionality which is defined in *\_\_main\_\_.py*.  To facilitate a game *variableAgentGame* is called, which utilises a instruct - response cycle until the game completes. To generate move instructions *getAgentTurn* is called, and textual commands are given to operate the Steam client Risk game through *executeAgentTurn*. As attacking during turns is non-deterministic, *executeAgentTurn* actively updates the GameState based on troop loss info, and monitors whether a player has been eliminated and the game is won.  On non-agent turns, *getTurn* recieves information passively about the state of the game, updating the GameState.

Depending on the functionality chosen, *getAgentTurn* calls the simple random acting agent in *randAI. py* or the ActionAI agent using *riskAgent*.  This initiates the *ids* searching function to dynamically select the most optimal move from *calculateActionSeq*, which is called on increasingly complex sequences of abstract actions. Finally, the general attack, draft, and fortification functions *attackSimple* and *generalFortify* are called to generate the moves, and the output is evaluated by *heuristic* in *heuristic. py*




## Attack Pathing
This project has been submitted without a working ActionAI agent. This is because the over a third of the total project was spent attempting to design a system achieving the goal as shown in Figures 5 and 6: to efficiently capture a set of territories. The considerations for making attacks are as follows:
+ **Troop Efficiency**: Attack paths found must attempt to capture all desired territories with the lowest troop expenditure. This is achieved by minimising travelling to neutral territories. 
+ **Stack Viability**: Predicting whether a stack could reliably execute a sequence of attacks requires accurate predictions of territory attack outcomes. 
+ **Pathing Efficiency**:  Due to attacking mechanics, it is optimal when retaining large stacks to make attacks in continuous paths rather than branching at a juncture. 
+ **Multiple Stacks**: As shown in Figure -(Slidepath), the agent should be able to use multiple stacks to capture the territories, creating paths which do not overlap
+ **Desirable Endpoints**: Stacks should be left at desirable locations by their last attack, defending chokepoints or with accessibility to make more attacks


<p  align="center">  <img src="https://i.ibb.co/thwjgPq/arb6.png" alt="enter image description here" width="650" /> </p>
<p> Figure 9. drawBoard display of attack pathing from blue stack to Alaska and North Africa </p>

<p  align="center">  <img src="https://i.ibb.co/v1rmJ6B/arb1.png" alt="enter image description here" width="650" /> </p>
<p>  Figure 10. drawArborescence  Attack pathing from different blue stack to Alaska and North Africa</p>


The complexity of this problem well exceeds the bounds of my knowledge in every way. As the map was represented as a graph, significant time was spent attempting to classify and modify this need into typical graph problems:

|Problem| Utility| Problem|
|--|--|--|
| ***Travelling Salesman Problem***| Provides a continuous path traversing nodes. | Attack path may require branching. |
| ***Minimum Spanning Tree***| Creates a tree of territories to traverse which is convenient to extract a path from. | Generated tree edges must bias against visiting neutral nodes and visit only in the worst case. This requires directional edges.|
| ***Minimum Spanning Arborescence*** | Generates essentially a "directional tree" with a root which can be set to the desired stack. Defines best paths to any node. | Does not support multiple roots. |
|***Minimum Branching*** |  Should create arborescence outcome for graphs with multiple separate components. | Unresolved errors during testing.|

After much work, the Minimum Spanning Arborescence (MSA) function was chosen to implement pathing, with the limitation that the agent could only execute actions attacking from one stack each turn. Attack paths (sequences of attack moves to capture a set of territories) were calculated using the following procedure in the *attackGraphSimple* function:

1. A directed graph is constructed from the current GameState, including all legal attacks connecting territories and the stack node
2. The edges are weighted using a custom weighting heuristic, ensuring travelling to neutral nodes is far more costly than to desired nodes, and travelling to nodes with high troops and low connectivity is also undesirable. 
3. A MSA calculation creates the arborescence connecting the stack through neutral territories of "least resistance" towards desired territories.
4. The arborescence still contains all neutral territories. All territories unneeded to reach a desired territory is discarded. 

## Project Termination
After successful development of the action pathing solutions for the general attack and draft functions, the project deadline arrived. This has halted development before a working ActionAI agent was created.  At the deadline, the *ids* function was being reworked and tested. 

### Capability at Termination
Although the ActionAI agent was not successfully implemented, the package successfully performs a number of operations. The RiskAI project can:
+ Correctly represent full Risk games of human players using the command line interface
+ Represent local games and interface with the Steam game with a human intermediary 
+ Allow a simple random acting agent to successfully generate and instruct moves
+ Draw board states and attack paths, and save these images during runtime
+ Use a heuristic to evaluate positions

### Project Success
Overall, this project can be deemed a partial success. As remarked in the Research analysis, Risk has relatively weak agents and research is lacking. Furthermore, for Risk: Global Domination no AI agents are publicly available due to difficulties interfacing with the game. This project has seen the successful creation of *a* interface which can be used as a foundation for further community development around of SMGStudio's game. An unforeseen aspect of writing game AI is that an entire internal representation of the game must be coded before agents can be created, which is hugely time consuming. Although the Attack Path problem was complex, as is yet to have a perfect solution, significant steps have been made towards a working agent, and I believe a successful agent could be created given time. It should be noted that I did not achieve my goals of having a non-trivial working agent, let alone beating the existing Risk bots. Despite this, the creation of my largest and most complex package to date allowed for deep and varied learning into Python, graphs, dependency managers, CLI usage, and project development. 


## References
[1]  Wolf, M. (2005) An Intelligent Artificial Player for the Game of Risk.
[2]   Gillenwater, J. (2022) RISK Gameplay Analysis Using Stochastic Beam Search.
[3]  SMG Studio (2021) RGD Balanced Blitz Source code. Available at: [https://github.com/smgstudio/risk-dice/tree/master](https://github.com/smgstudio/risk-dice/tree/master) (Accessed: 17 April 2024).
[4]   Ferrari, R.G. and Assuncao, J.V.C. (2022) Towards playing Risk with a hybrid Monte Carlo based agent.
[5]   Bethdavid, S. (2020) Zero-Knowledge Agent Trained for the Game of Risk.
[6]   Blomqvist, E. (2020) Playing the Game of Risk with an AlphaZero Agent.
[7]   Heredia, L.G. and Cazenave, T. (2022) Expert Iteration for Risk.
[8] SMGStudio (2021). _Our RISK AI_. [online] SMG Studio. Available at: https://smgstudio.freshdesk.com/support/solutions/articles/11000077687-our-risk-ai.
[9] https://youtu.be/9vgiZwV6kR8?si=nAo3P-6Snzx7l8vF
[10] jack6 (2022). _Balanced Blitz calculator and data_. [online] Google Sheets. Available at: https://docs.google.com/spreadsheets/d/1Htk4vaXqNWsKDU7oSoeqbENLp_MjDKSxKXyL1W7rTHk/edit?usp=sharing [Accessed 22 Jun. 2024].
[11] Legendary Tactics (2022). _RISK Strategy Guide - Top 10 Tips_. [online] YouTube. Available at: https://youtu.be/Ltf7NldY-Nc?si=qKgnRjStPI0gvsLa [Accessed 22 Apr. 2024].
[12] The Kill Pete Strategy (2022). _How to Play Risk! Tutorial for Beginners_. [online] YouTube. Available at: https://youtu.be/y-ESVSkkMus?si=QAbui0XRvhUoETei [Accessed 15 Mar. 2024].
[13] jack6 (2022b). _Calculation Method Balanced Blitz Troop Losses_. [online] Google Docs. Available at: https://docs.google.com/document/d/1LL5Q6mZISZgMyPm1E4i9g-RlENYeFzzD9yL8YXEnpDo/edit?usp=sharing [Accessed 18 Jun. 2024].
[14] Risk: Global Domination Wiki (2022). _Everything You Need to Know about Zombies!_ [online] Available at: https://risk-global-domination.fandom.com/wiki/Everything_you_need_to_know_about_Zombies! [Accessed 29 Apr. 2024].
[15] Johansson, S.J. (2014). Using Multi-Agent System Technology in Risk Bots. Proceedings of the Second Artificial Intelligence and Interactive Digital Entertainment Conference. ResearchGate.
[16] Brand, D. and Kroon, S. (2014). Sample Evaluation for Action Selection in Monte Carlo Tree Search. doi:https://doi.org/10.1145/2664591.2664612.
[17] Kylted (2024). _Round 1 of the Risk World Cup!_ [online] YouTube. Available at: https://www.youtube.com/watch?v=dBIwOcMGtKQ [Accessed 5 May 2024].