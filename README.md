# random-basketball-league-season-sim
Random simulation of a single season of a random basketball league

OOP project written in Python.

The whole league is generated randomly, names of both players and teams are selected random from files with city names, team names, first names and surnames, 
player are randomly assinged to teams and attributes of players are randomized based on ranged predifined for each position.

Based on randomly generated calendar, games are simulated. 
The logic behind game sim:
- in each quarter there are 20 ball possessions for each team
- decisions of players and their outcomes are randomly generated considering values of corresponding skill attributes

Based on results of games from the whole season team ranking is created and based on statistics of players the leaders in average stats and mvp are selected.

Simple GUI is provided to see those results.
