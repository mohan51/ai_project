# Neighborhood Distance and the Artificial Bee Colony (ABC) Optimization Algorithm #

![Bees.jpg](https://bitbucket.org/repo/q4XX5y/images/1858731202-Bees.jpg)

### Brief Description ###

In the ABC model, the colony consists of three groups of bees: **employed bees**, **onlookers**, and **scouts**. It is assumed that there is only one artificial employed bee for each food source. In other words, the number of employed bees in the colony is equal to the number of food sources around the hive. Employed bees go to their food source and come back to hive and dance on this area. The employed bee whose food source has been abandoned becomes a scout and starts to search for finding a new food source. Onlookers watch the dances of employed bees and choose food sources depending on dances.

### The general idea of the algorithm ###

Initial food sources are produced for all employed bees

REPEAT

 - Each employed bee goes to a food source in her memory and determines a neighbour source, then evaluates its nectar amount and dances in the hive

 - Each onlooker watches the dance of employed bees and chooses one of their sources depending on the dances, and then goes to that source. After choosing a neighbour around that, she evaluates its nectar amount.

 - Abandoned food sources are determined and are replaced with the new food sources discovered by scouts.

- The best food source found so far is registered.

UNTIL (requirements are met)

### A Visual Guide ###

Initial randomize configuration of "employed bees." 
![Initial.png](https://bitbucket.org/repo/q4XX5y/images/217938213-Initial.png)

Begins to converge on the global minimum (the origin in this example) after only 10 cycles
![Cycle10.png](https://bitbucket.org/repo/q4XX5y/images/1292224664-Cycle10.png)

After all employed bees converge on a solution, "scout bees" are spawned
![Cycle85.png](https://bitbucket.org/repo/q4XX5y/images/3725638092-Cycle85.png)

Final configuration
![Cycle200.png](https://bitbucket.org/repo/q4XX5y/images/3228738010-Cycle200.png)

Performance of the Artificial Bee Colony
![ArtificialBeeColony.png](https://bitbucket.org/repo/q4XX5y/images/1339486431-ArtificialBeeColony.png)

### Thanks ###
Jordan Devenport
