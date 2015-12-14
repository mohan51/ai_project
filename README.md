![Bees.jpg](https://bitbucket.org/repo/q4XX5y/images/1858731202-Bees.jpg)

## Introduction ##

The Artificial Bee Colony algorithm is an algorithm based on the foraging behavior of real life honey bees. In the colony, there are three types of bees. Unlike in real life, there is only one employed bee per food source, and therefore there are an equal number of employed bees and food sources. Employed bees try to find a neighbor of relatively close to their food sources. The distance between the food source and its neighbors is a function of a distance to neighbor variable. Employed bees check the fitness of their respective food sources and report back to the hive. Onlooker bees evaluate the fitness of the employed bees relative to the other employed bees, follow the bees to the best food source, therefore reinforcing the fitness of that food source. Scout bees are spawned as food sources are abandoned to search for new food sources. The algorithm terminates after the bees have converged on a single source, or after a set number of epochs.

By modifying the function and parameter for distance to neighbor, its apparent that the algorithm converges more slowly towards a solution, but finds solutions more easily. These findings are important to the effectiveness of this algorithm.

### The general idea of the algorithm ###

Food sources and employed bees are matched

WHILE there is no definite solution and the algorithm hasn't looped MAX_EPOCH number of times

 - Each employed bee goes to a food source in her memory and determines a neighbour source, then evaluates its nectar amount and dances in the hive. This neighbor source is a function of the distance parameter.

 - Each onlooker watches the dance of employed bees and chooses one of their sources depending on the dances, and then goes to that source. After choosing a neighbour around that, she evaluates its nectar amount.

 - Abandoned food sources are determined and are replaced with the new food sources discovered by scouts.

- The best food source found so far is registered.

Return the best food sources

## A Visual Guide ##

I plotted the state of the bees in the artificial bee colony at several fixed epochs. The employed bees are spawned dependent on the distance parameter. The optimal food source is located at the origin (0, 0).

### Default Arrangement of Bees ###

Initial randomize configuration of "employed bees." 
![Initial.png](https://bitbucket.org/repo/q4XX5y/images/217938213-Initial.png)

After only a few cycles, the algorithm begins to converge on the global minimum (the origin in this example) after only 10 cycles
![Cycle10.png](https://bitbucket.org/repo/q4XX5y/images/1292224664-Cycle10.png)

After all employed bees converge on a solution, "scout bees" are spawned
![Cycle85.png](https://bitbucket.org/repo/q4XX5y/images/3725638092-Cycle85.png)

Final configuration -- Note that all bees from previous iterations have been stacked on the center (0,0) "food source"
![Cycle200.png](https://bitbucket.org/repo/q4XX5y/images/3228738010-Cycle200.png)

Performance of the Artificial Bee Colony without any parameter tweaking
![ArtificialBeeColony.png](https://bitbucket.org/repo/q4XX5y/images/1339486431-ArtificialBeeColony.png)

### Effects of Greater Distance on Convergence ###

Initial configuration of bees with a greater distance parameter set. Note how the bees are more spread apart.
![1.png](https://bitbucket.org/repo/q4XX5y/images/1650011785-1.png)

The bees begin to converge later because of the greater distance.
![10.png](https://bitbucket.org/repo/q4XX5y/images/2396434634-10.png)

When the employed bees abandon their food sources, the scout bees are spawned at greater distance from each other.
![85.png](https://bitbucket.org/repo/q4XX5y/images/681249855-85.png)

After 200 epochs, the algorithm is stopped. The newly spawned scout bees are still fairly scattered.
![200.png](https://bitbucket.org/repo/q4XX5y/images/1341039890-200.png)

The results of the run with greater distance. The initial run by the employed bees takes less time to converge, but the optimal solution is found later. The spawning of scout bees greatly affects the average performance of the algorithm.
![results.png](https://bitbucket.org/repo/q4XX5y/images/1211122148-results.png)

### Effects of Smaller Distance on Convergence ###

Initial configuration of bees. The bees are spawned more closely.
![1.png](https://bitbucket.org/repo/q4XX5y/images/3940758951-1.png)

The bees quickly swarm upon the food source.
![10.png](https://bitbucket.org/repo/q4XX5y/images/2923254128-10.png)

The scout bees are spawned at smaller distance from each other
![85.png](https://bitbucket.org/repo/q4XX5y/images/599805997-85.png)

The final configuration of bees converges on the solution quickly
![200.png](https://bitbucket.org/repo/q4XX5y/images/1983623346-200.png)

The results of smaller distance. An optimal solution is found quickly, but it takes longer for bees to converge on a solution. The scout bees move more slowly toward the optimal solution, but the average performance is never greatly affected.
![results.png](https://bitbucket.org/repo/q4XX5y/images/2380272736-results.png)

## Conclusion ##

Modifying the distance parameter of the bees algorithm has an exceptional effect on the performance of the algorithm. The greater the distance bees can move, the higher the variability in results, the quicker the convergence, and the higher effect on average performance.

### Thanks ###
Jordan Devenport
