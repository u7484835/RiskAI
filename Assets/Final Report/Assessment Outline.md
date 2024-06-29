# ASC Final Report Outline
### By Campbell McTernan u7484835

  
For your convenience I have compiled a few notes about the project as we have not discussed the intent and details of this Assignment in person. 

### Project Summary

This research course will focus on the detailed exploration and analysis of the online board game Risk: Global Domination or similar variants. Risk is a multi-player, turn based, diplomacy driven game with an objective to capture all territories on the board. With up to 6 players, optimal gameplay must include careful communication and cooperation between players. The goal of this project is to design and implement an AI bot to play Risk with more profficiency than the current foremost AI standard, or otherwise perform an equivalent turing test to act passably as a human player. Students will examine both machine learning and symbolic AI methods to achieve this goal. Students will finish this course by producing a program which implements a significantly developed AI, examining its performance and presenting the findings in a short lecture.

  
### Project Outcomes
Upon successful completion, students will have the knowledge and skills to:
1. Identify algorithms, data structures and an operational interface best suited to Risk as a Non-deterministic diplomacy based game.
2. Implement this framework into a working bot with the capacity to respond dynamically and diplomatically to other players
3. Design and perform an empirical evaluation of the approach/es used, discuss improvements which could be made, and state the conclusions that the evaluation supports.Oral Presentation will discuss the implementation, progress and challenges of the project, with a particular focus on the work done to address the Risk game's specific gameplay. Student will present and teach the research group on this area.

### Assessment Details

" The final Report will consist of a 35% (total weighting) code artifact which implements advanced algorithms to play the Risk game in an interesting and significant way, perhaps focusing on communication and cooperation or statistically optimal play. The other 35% will consist of a technical report discussing the algorithms and approach/es used, with empirical evaluations of performance and future improvements."

### Submission Notes

As mentioned, this submission is a 50/50 between the codebase and report. Personally, I found the report quite difficult to write for 2 main reasons:
+ As the AI planned was to be handcrafted, and largely predicated on my deep understanding of the Risk game and high level strategy most implementation details were best suited to readers with significant knowledge on the game. Of course this is a niche game and thus to make my ideas even comprehensible I had to spend a significant amount of time covering the baseline. This felt directly contrary to the intention of a report which should assume working peer knowledge. 
+ As the project was far larger and more complicated than intended, I simply did not summarise all of my efforts appropriately in the document. For brievity I completely neglected to mention the risk-dice problem. This was that to implement the game, there should be robust predictions of the attacking dice. The exact dice code used in game has been released here: https://github.com/smgstudio/risk-dice . The code was built in Unity for C#, and I spent perhaps 10-15 hours attempting to compile and run it to no avail. Instead I found community resources which were numerical approximations and outputs of the code. I formatted these into a csv and used Numpy to facilliate fast access of "perfect dice" amounts needed etc. There were many such problems like this which I just did not cover. 

The main reason I left this outline is that I firmly believe that <u>reading the pages suggested in Reference [1] and [2] could have a +10% effect on my mark </u>, as information is so important in informing the rest of my implementation and strategy. It is unfortunate that I did not have the time to personally outline the game and papers (of course that would be more befitting an honours work) but it is still quite relevant to any reasonable understanding of the strategies I attempted to implement. 