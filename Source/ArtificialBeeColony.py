import random


class Honey(object):
    MAX_LENGTH = None
    nectar = list()
    trials = None
    conflicts = None
    fitness = None
    selection_probability = None
    
    def __init__(self, size):
        self.MAX_LENGTH = size
        self.nectar = [i for i in range(self.MAX_LENGTH)]
        self.conflicts = 0
        self.trials = 0
        self.fitness = 0.0
        self.selection_probability = 0.0

    def __lt__(self, other):
        return self.conflicts < other.get_conflicts()

    def __gt__(self, other):
        return self.conflicts > other.get_conflicts()

    def __eq__(self, other):
        return self.conflicts == other.get_conflicts()
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def compute_conflicts(self):
        board = [[None] * self.MAX_LENGTH] * self.MAX_LENGTH
        dx = [-1, 1, -1, 1]
        dy = [-1, 1, 1, -1]
        conflicts = 0
        board = self.clear_board(board)
        board = self.plot_queens(board)
        for i in range(self.MAX_LENGTH):
            x = i
            y = self.nectar[i]
            for j in range(4):
                tempx = x
                tempy = y
                done = False
                while not done:
                    tempx += dx[j]
                    tempy += dy[j]
                    if tempx < 0 or tempx >= self.MAX_LENGTH or tempy < 0 or tempy >= self.MAX_LENGTH:
                        done = True
                    elif board[tempx][tempy] == "Q":
                        conflicts += 1
        self.conflicts = conflicts
    
    def plot_queens(self, board):
        for i in range(self.MAX_LENGTH):
            board[i][self.nectar[i]] = "Q"
        return board
    
    def clear_board(self, board):
        for i in range(self.MAX_LENGTH):
            for j in range(self.MAX_LENGTH):
                board[i][j] = ""
        return board
    
    def get_conflicts(self):
        return self.conflicts
    
    def set_conflicts(self, new_conflicts):
        self.conflicts = new_conflicts
    
    def get_selection_probability(self):
        return self.selection_probability
    
    def set_selection_probability(self, new_selection_probability):
        self.selection_probability = new_selection_probability
    
    def get_fitness(self):
        return self.fitness
    
    def set_fitness(self, new_fitness):
        self.fitness = new_fitness
    
    def get_nectar(self, idx):
        return self.nectar[idx]
    
    def get_index(self, value):
        k = 0
        for k in range(self.MAX_LENGTH):
            if self.nectar[k] == value:
                break
        return k
    
    def set_nectar(self, idx, value):
        self.nectar[idx] = value
    
    def get_trials(self):
        return self.trials
    
    def set_trials(self, trials):
        self.trials = trials
    
    def get_max_length(self):
        return self.MAX_LENGTH


class ArtificialBeeColony(object):
    MAX_LENGTH = None
    NP = None
    FOOD_NUMBER = None
    LIMIT = None
    MAX_EPOCH = None
    MIN_SHUFFLE = None
    MAX_SHUFFLE = None
    rand = random
    food_sources = list()
    solutions = list()
    gBest = None
    epoch = None
    
    def __init__(self, n):
        self.MAX_LENGTH = n
        self.NP = 40
        self.FOOD_NUMBER = self.NP/2
        self.LIMIT = 50
        self.MAX_EPOCH = 1000
        self.MIN_SHUFFLE = 8
        self.MAX_SHUFFLE = 20
        self.gBest = None
        self.epoch = 0
        
    def algorithm(self):
        self.food_sources = list()
        self.solutions = list()
        self.rand = random
        done = False
        self.epoch = 0
        self.initialize()
        self.memorize_best_food_source()
        
        while not done:
            if self.epoch < self.MAX_EPOCH:
                if self.gBest.get_conflicts() == 0:
                    done = True
                self.send_employed_bees()
                self.get_fitness()
                self.calculate_probabilities()
                self.send_onlooker_bees()
                self.memorize_best_food_source()
                self.send_scout_bees()
                self.epoch += 1
                print("Epoch: " + str(self.epoch))
            else:
                done = True
        if self.epoch == self.MAX_EPOCH:
            print("No solution found")
            done = False
        print("done.")
        print("Completed " + str(self.epoch) + " epochs.")
        for h in self.food_sources:
            if h.get_conflicts() == 0:
                print("SOLUTION")
                self.solutions.append(h)
                self.print_solution(h)
                print("conflicts:" + str(h.get_conflicts()))
        return done
        
    def send_employed_bees(self):
        for i in range(self.FOOD_NUMBER):
            neighbor_bee_idx = self.get_exclusive_random_number(self.FOOD_NUMBER - 1, i)
            current_bee = self.food_sources[i]
            neighbor_bee = self.food_sources[neighbor_bee_idx]
            self.send_to_work(current_bee, neighbor_bee)
    
    def send_onlooker_bees(self):
        i = 0
        t = 0
        while t < self.FOOD_NUMBER:
            current_bee = self.food_sources[i]
            if self.rand.random() < current_bee.get_selection_probability():
                t += 1
                neighbor_bee_idx = self.get_exclusive_random_number(self.FOOD_NUMBER - 1, i)
                neighbor_bee = self.food_sources[neighbor_bee_idx]
                self.send_to_work(current_bee, neighbor_bee)
            i += 1
            if i == self.FOOD_NUMBER:
                i = 0
                
    def send_to_work(self, current_bee, neighbor_bee):
        prev_conflicts = current_bee.get_conflicts()
        parameter_to_change = self.get_random_number(0, self.MAX_LENGTH - 1)
        temp_value = current_bee.get_nectar(parameter_to_change)
        new_value = int(temp_value + (temp_value - neighbor_bee.get_nectar(parameter_to_change)) * (self.rand.random() - 0.5) * 2)
        if new_value < 0:
            new_value = 0
        if new_value > self.MAX_LENGTH - 1:
            new_value = self.MAX_LENGTH - 1
        temp_idx = current_bee.get_index(new_value)
        current_bee.set_nectar(parameter_to_change, new_value)
        current_bee.set_nectar(temp_idx, temp_value)
        current_bee.compute_conflicts()
        curr_conflicts = current_bee.get_conflicts()
        if prev_conflicts < curr_conflicts:
            current_bee.set_nectar(parameter_to_change, temp_value)
            current_bee.set_nectar(temp_idx, new_value)
            current_bee.compute_conflicts()
            current_bee.set_trials(current_bee.get_trials() + 1)
        else:
            current_bee.set_trials(0)
            
    def send_scout_bees(self):
        for i in range(self.FOOD_NUMBER):
            current_bee = self.food_sources[i]
            if current_bee.get_trials() >= self.LIMIT:
                shuffles = self.get_random_number(self.MIN_SHUFFLE, self.MAX_SHUFFLE)
                for j in range(shuffles):
                    self.randomly_arrange(i)
                current_bee.compute_conflicts()
                current_bee.set_trials(0)
        
    def get_fitness(self):
        food_source_str = ""
        if len(self.food_sources) > 0:
            food_source_str = "[" + str(self.food_sources[0].get_conflicts())
            for i in range(1, len(self.food_sources)):
                food_source_str += ", " + str(self.food_sources[i].get_conflicts())
            food_source_str += "]"
        worst_score = max(self.food_sources).get_conflicts()
        best_score = worst_score - min(self.food_sources).get_conflicts()
        food_source_str = "Best score: " + str(best_score) + " Worst score: " + str(worst_score) + " " + food_source_str
        print(food_source_str)
        for i in range(self.FOOD_NUMBER):
            if best_score == 0.0:
                return
            this_food = self.food_sources[i]
            this_food.set_fitness(((worst_score - this_food.get_conflicts()) * 100.0) / best_score)
    
    def calculate_probabilities(self):
        max_fit = self.food_sources[0].get_fitness()
        for i in range(1, self.FOOD_NUMBER):
            this_food = self.food_sources[i]
            if this_food.get_fitness() > max_fit:
                max_fit = this_food.get_fitness()
        for j in range(self.FOOD_NUMBER):
            this_food = self.food_sources[j]
            this_food.set_selection_probability((0.9*(this_food.get_fitness()/max_fit))+0.1)
    
    def initialize(self):
        for i in range(self.FOOD_NUMBER):
            new_honey = Honey(self.MAX_LENGTH)
            self.food_sources.append(new_honey)
            new_food_idx = self.food_sources.index(new_honey)
            shuffles = self.get_random_number(self.MIN_SHUFFLE, self.MAX_SHUFFLE)
            for j in range(shuffles):
                self.randomly_arrange(new_food_idx)
            self.food_sources[new_food_idx].compute_conflicts()
    
    def get_random_number(self, low, high):
        return self.rand.randint(low, high)
        
    def get_exclusive_random_number(self, high, excluded):
        exclusive_rand = 0
        while exclusive_rand == excluded:
            exclusive_rand = self.rand.randint(0, high)
        return exclusive_rand
    
    def randomly_arrange(self, idx):
        position_a = self.get_random_number(0, self.MAX_LENGTH - 1)
        position_b = self.get_exclusive_random_number(self.MAX_LENGTH - 1, position_a)
        this_honey = self.food_sources[idx]
        temp = this_honey.get_nectar(position_a)
        this_honey.set_nectar(position_a, this_honey.get_nectar(position_b))
        this_honey.set_nectar(position_b, temp)
    
    def memorize_best_food_source(self):
        self.gBest = min(self.food_sources)
    
    def print_solution(self, solution):
        board = [["" for y in range(self.MAX_LENGTH)] for x in range(self.MAX_LENGTH)]
        for x in range(self.MAX_LENGTH):
            board[x][solution.get_nectar(x)] = "Q"
        print("Board:")
        for y in range(self.MAX_LENGTH):
            for x in range(self.MAX_LENGTH):
                if board[x][y] == "Q":
                    print("Q ")
                else:
                    print(". ")
            print("")
        
    def get_solutions(self):
        return self.solutions
        
    def get_epoch(self):
        return self.epoch
    
    def set_max_epoch(self, new_max_epoch):
        self.MAX_EPOCH = new_max_epoch
    
    def get_pop_size(self):
        return len(self.food_sources)
    
    def get_start_size(self):
        return self.NP
    
    def get_food_num(self):
        return self.FOOD_NUMBER
    
    def get_limit(self):
        return self.LIMIT
    
    def set_limit(self, new_limit):
        self.LIMIT = new_limit
    
    def get_max_epoch(self):
        return self.MAX_EPOCH
    
    def get_shuffle_min(self):
        return self.MIN_SHUFFLE
    
    def get_shuffle_max(self):
        return self.MAX_SHUFFLE


class Writer(object):
    log_list = None

    def __init__(self):
        self.log_list = list()

    def add(self, line):
        self.log_list.append(line)
    
    def add_honey(self, honey):
        n = honey.get_max_length()
        board = [["" for j in range(n)] for i in range(n)]
        self.clear_board(board, n)
        for x in range(n):
            board[x][honey.get_nectar(x)] = "Q"
        self.print_board(board, n)

    @staticmethod
    def clear_board(board, n):
        for x in range(n):
            for y in range(n):
                board[x][y] = ""
    
    def print_board(self, board, n):
        for y in range(n):
            temp = ""
            for x in range(n):
                if board[x][y] == "Q":
                    temp += "Q "
                else:
                    temp += ". "
            self.log_list.append(temp)
    
    def write_file(self, filename):
        with open(filename, "w") as output:
            for line in self.log_list:
                output.write(line)


class TesterABC(object):
    log_writer = None
    abc = None
    MAX_RUN = None
    MAX_LENGTH = None
    runtimes = None
    
    def __init__(self):
        self.log_writer = Writer()
        self.MAX_RUN = 50
        self.runtimes = [None] * self.MAX_RUN
    
    def test(self, max_length, trial_limit, max_epoch):
        self.MAX_LENGTH = max_length
        self.abc = ArtificialBeeColony(self.MAX_LENGTH)
        self.abc.set_limit(trial_limit)
        self.abc.set_max_epoch(max_epoch)
        filepath = "ABC-N" + str(self.MAX_LENGTH) + "-" + str(trial_limit) + "-" + str(max_epoch) + ".txt"
        total_time = 0
        fail = 0
        success = 0
        i = 0
        while i < self.MAX_RUN:
            if self.abc.algorithm():
                self.runtimes[i] = total_time
                i += 1
                success += 1
                self.log_writer.add("Run: " + str(i))
                self.log_writer.add("Found at epoch: " + str(self.abc.get_epoch()))
                self.log_writer.add("Population size: " + str(self.abc.get_pop_size()))
                self.log_writer.add("")
                for honey in self.abc.get_solutions():
                    self.log_writer.add_honey(honey)
                    self.log_writer.add("")
            else:
                fail += 1
                print("Fail!")
            if fail >= 100:
                print("Cannot find solution with these params")
            total_time = 0
        print("Number of successes: " + str(success))
        print("Number of failures: " + str(fail))
        self.log_writer.add("Runtime summary")
        self.log_writer.add("")
        for x in self.runtimes:
            self.log_writer.add(str(x))
        self.log_writer.write_file(filepath)
    
    def log_parameters(self):
        self.log_writer.add("Artificial Bee Colony Algorithm")
        self.log_writer.add("Parameters")
        self.log_writer.add("MAX_LENGTH: " + str(self.MAX_LENGTH))
        self.log_writer.add("STARTING_POPULATION: " + str(self.abc.get_start_size()))
        self.log_writer.add("MAX_EPOCHS: " + str(self.abc.get_max_epoch()))
        self.log_writer.add("FOOD_NUMBER: " + str(self.abc.get_food_num()))
        self.log_writer.add("TRIAL_LIMIT: " + str(self.abc.get_limit()))
        self.log_writer.add("MINIMUM_SHUFFLES " + str(self.abc.get_shuffle_min()))
        self.log_writer.add("MAXIMUM_SHUFFLES " + str(self.abc.get_shuffle_max()))
        self.log_writer.add("")
    
    def print_runtimes(self):
        for x in self.runtimes:
            print("Run with time " + str(x) + " nanoseconds")
        
tester = TesterABC()
tester.test(4, 50, 1000)
