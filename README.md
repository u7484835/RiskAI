# ActionAI: A handcrafted planning agent for Risk

The RiskAI project is intended to provide the internal representation, interface, and agents to play Risk: Global Domination (RGD) alongside the main package provided on Steam. It is a research project testing the viability of implementing abstract conceptual planning into a diplomacy-driven non-deterministic board game. Although simple agents such as a random moving agent are implemented, the premier agent ActionAI plans turns through a strong heuristic geared towards making its position impregnable to other players without searching over their move possibilities. During its turn, the agent searches and selects from a number of actions including eliminating a player, breaking a bonus, and taking a card, or combinations of these plans to calculate its moves. The agent has not yet been tested against the current RGD bots. 

## Installation

RiskAI is written in Python using Click, Poetry, NetworkX and the risk-dice package provided by SMG Studio. It should work on any platform supporting Python 3. To install RisKAI, first **ensure that you have at least a Python 3.11** installation available, then install [Poetry](https://python-poetry.org). The poetry install instructions vary depending on your preferences for a python setup this is likely to work on Linux, macOS or Windows (WSL):

    curl -sSL https://install.python-poetry.org | python3 -

Then you should clone this repository or download it to your computer:

    git clone https://gitlab.cecs.anu.edu.au/u7484835/riskai.git
    cd riskai

Then you can install the dependencies using Poetry:

    poetry install

## How to use

The main executable can be run using the command ```poetry run python run_riskAI.py```. This will execute a function which guides all functionality implemented for the RiskAI project. To run the rudimentary tests implemented, use the command ```poetry run python tests/<testName>.py```. An example would be ```poetry run python tests/graphTests.py```. Each test was intended for proof of concept tests during implementation rather than validity of the programs so they may not be very useful. 

## Questions? Contact me

If you'd like any further information or explanation about the repo, please contact me at u7488435@anu.edu.au. I'd be happy to help. 

## Credits 

The layout of this repository, the README, and package choices have been modelled off of Charles Martin's IMPSY project. Huge hat tip to him for the inspiraration for the underlying foundation of this project. You can find the project [here](https://github.com/cpmpercussion/imps.git)