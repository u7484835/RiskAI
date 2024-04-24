  

# Design Specification

### By Campbell McTernan u7484835

  
  

## Overview

This project aims to implement an Artificial Intelligence (AI) agent to play the online board game Risk: Global Domination. Risk is a multi-player, turn based, diplomacy driven game with an objective to capture all territories on a map. This is done by attacking territories with troops, which has non-deterministic outcomes. Risk has a state-space and game-tree complexity hugely exceeding games popular for AI such as Chess, Shogi, and Go [1], which has rendered renders lookahead strategies such as the Monte Carlo Tree Search (MCTS) or MiniMax far less effective. Thus, this project will use the novel approach of "Action Abstraction": forcing the agent to select and evaluate handcrafted high-level strategies such as eliminating players or taking a continent. This package will be implemented in Python and will provide a Command Line Interface (CLI) for interaction with the game. Overall, the aim of this project will be to surpass the inbuilt "Expert" bots provided, with a playing style which is enriching and balanced for high-level human play. 


## Risk: Global Domination

Overall, this design specification will assume intermediate knowledge in Risk and will not attempt to explain the game and strategies unless necessary. It would be highly advisable to read Michael Wolf's explanation of Risk _[1] pages 20-42. J. Gillenwater's literature review [2] (pages 30-37) is recent, comprehensive and concise and is also advisable to read. 

Risk: Global Domination (RGD) is the most popular and recent addition to Hasbro's Risk franchise. It is primarily played online with 4-6 players, with each player getting 60-180s per turn. RGD allows for huge variation on the original game including over 100 unique maps and mechanical variations to the dice, goals, maps and player communication. The crucial difference in RGD to every other Risk implementation studied is the introduction of "Balanced Blitz" dice. 

### True Random Dice

RGD denotes the traditional risk system of attacking territories as having "True Random" dice. In traditional Risk, when a territory is attacked the attacking player rolls up to 3 six-sided dice and the defender rolls up to 2 dice based on the troops used. The highest rolled attacking dice is then compared with the highest defending dice, with the highest rolling player declared as the victor. If the same number is rolled the defender is the victor. This eliminates one of the loser's troops. This process is repeated for the pair of second highest attacking and defending dice. Territories can be attacked as many times as desired until all defending troops are eliminated and the player gains control of the territory. With a sufficient advantage of attacking troops eg. 100 vs 1, the probability of winning the territory is stupendously high but not certain. This means that over games, the outcomes of battles can be highly unpredictable. 

### Balanced Blitz Dice

The standard configuration in RGD is "Balanced Blitz" dice, which entirely reconfigures the chances of winning an attack, and the possible losses an attack might deliver to both sides. In simple terms, this configuration reduces or eliminates all extreme outcomes of attacks, rounding all attacks with >= 95% winning chances to  100% and all  <= 5% winning chances to 0%. It also skews all troop outcomes toward the most likely result, so high probability attacks will lose less troops and low probability attacks will lose more troops. Other calculations are implemented to magnify this effect. Overall, this has huge implications, as a 4v1 and 17v9 roll will now certainly win a territory, while a 3v10 will certainly fail. This reduces the non-determinism in the game significantly with perfect play, and allows for a magnitude of new strategies for agents to implement. 

## Aims 



















## References

[1] Michael Wolf: An Intelligent Artificial Player for the Game of Risk

[2] Jacob Gillenwater: RISK Gameplay Analysis Using Stochastic Beam Search

[3] RGD Balanced Blitz Source code: https://github.com/smgstudio/risk-dice/tree/master 