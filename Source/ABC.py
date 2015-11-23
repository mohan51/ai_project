__author__ = 'Jordan'
import math
import random


class ArtificialBeeColony(object):
    np = 20
    food_number = int(np/2)
    limit = 100
    max_cycle = 2500

    d = 100
    lower_bound = -5.12
    upper_bound = 5.12

    epochs = 30

    foods = [[0] * d] * food_number
    f = [0] * food_number
    fitness = [0] * food_number
    trial = [0] * food_number
    prob = [0] * food_number
    solution = [0] * d

    obj_val_sol = None
    fitness_sol = None

    neighbor = None
    param_to_change = None
    global_min = None
    global_params = [None] * d
    global_mins = [None] * epochs

    r = None

    @staticmethod
    def calculate_fitness(fun):
        if fun >= 0:
            return 1/(fun + 1)
        else:
            return 1 + abs(fun)

    def generate_random_number(self):
        self.r = float(random.random() * 32767) / (float(32767) + float(1))

    def memorize_best_food_source(self):
        for i in range(self.food_number):
            if self.f[i] < self.global_min:
                self.global_min = self.f[i]
                for j in range(self.d):
                    self.global_params[j] = self.foods[i][j]

    def init(self, index):
        for j in range(self.d):
            self.generate_random_number()
            self.foods[index][j] = self.r * (self.upper_bound - self.lower_bound) + self.lower_bound
            self.solution[j] = self.foods[index][j]
        self.f[index] = self.calculate_function(self.solution)
        self.fitness[index] = self.calculate_fitness(self.f[index])
        self.trial[index] = 0

    def initial(self):
        for i in range(self.food_number):
            self.init(i)
        self.global_min = self.f[0]
        for i in range(self.d):
            self.global_params[i] = self.foods[0][i]

    def send_employed_bees(self):
        for i in range(self.food_number):
            self.generate_random_number()
            self.param_to_change = int(self.r * self.d)
            self.generate_random_number()
            self.neighbor = int(self.r * self.food_number)
            for j in range(self.d):
                self.solution[j] = self.foods[i][j]
            self.generate_random_number()
            self.solution[self.param_to_change] = self.foods[i][self.param_to_change] + (self.foods[i][self.param_to_change] - self.foods[self.neighbor][self.param_to_change]) * (self.r - 0.5) * 2
            if self.solution[self.param_to_change] < self.lower_bound:
                self.solution[self.param_to_change] = self.lower_bound
            if self.solution[self.param_to_change] > self.upper_bound:
                self.solution[self.param_to_change] = self.upper_bound
            self.obj_val_sol = self.calculate_function(self.solution)
            self.fitness_sol = self.calculate_fitness(self.obj_val_sol)
            if self.fitness_sol > self.fitness[i]:
                self.trial[i] = 0
                for j in range(self.d):
                    self.foods[i][j] = self.solution[j]
                    self.f[i] = self.obj_val_sol
                    self.fitness[i] = self.fitness_sol
            else:
                self.trial[i] += 1

    def calculate_probabilities(self):
        maxfit = self.fitness[0]
        for i in range(1, self.food_number):
            if self.fitness[i] > maxfit:
                maxfit = self.fitness[i]
        for i in range(self.food_number):
            self.prob[i] = (0.9 * (self.fitness[i]/maxfit)) + 0.1

    def send_onlooker_bees(self):
        i = 0
        t = 0
        while t < self.food_number:
            self.generate_random_number()
            if self.r < self.prob[i]:
                t += 1
                self.generate_random_number()
                self.param_to_change = int(self.r * self.d)
                self.generate_random_number()
                self.neighbor = int(self.r * self.food_number)
                while self.neighbor == i:
                    self.generate_random_number()
                    self.neighbor = int(self.r * self.food_number)
                for j in range(self.d):
                    self.solution[j] = self.foods[i][j]
                self.generate_random_number()
                self.solution[self.param_to_change] = self.foods[i][self.param_to_change] + (self.foods[i][self.param_to_change] - self.foods[self.neighbor][self.param_to_change]) * (self.r - 0.5) * 2
                if self.solution[self.param_to_change] < self.lower_bound:
                    self.solution[self.param_to_change] = self.lower_bound
                if self.solution[self.param_to_change] > self.upper_bound:
                    self.solution[self.param_to_change] = self.upper_bound
                self.obj_val_sol = self.calculate_function(self.solution)
                self.fitness_sol = self.calculate_fitness(self.obj_val_sol)
                if self.fitness_sol > self.fitness[i]:
                    self.trial[i] = 0
                    for j in range(self.d):
                        self.foods[i][j] = self.solution[j]
                    self.f[i] = self.obj_val_sol
                    self.fitness[i] = self.fitness_sol
                else:
                    self.trial[i] += 1
                i += 1
                if i == self.food_number:
                    i = 0

    def send_scout_bees(self):
        maxtrial_index = 0
        for i in range(1, self.food_number):
            if self.trial[i] > self.trial[maxtrial_index]:
                maxtrial_index = i
        if self.trial[maxtrial_index] >= self.limit:
            self.init(maxtrial_index)

    def calculate_function(self, sol):
        return self.sphere(sol)

    def sphere(self, sol):
        top = 0
        for j in range(self.d):
            top += sol[j]**2
        return top

abc = ArtificialBeeColony()
j = 0
mean = 0

for run in range(abc.epochs):
    abc.initial()
    abc.memorize_best_food_source()
    for iter in range(abc.max_cycle):
        abc.send_employed_bees()
        abc.calculate_probabilities()
        abc.send_onlooker_bees()
        abc.memorize_best_food_source()
        abc.send_scout_bees()
    for j in range(abc.d):
        print("GlobalParam[" + str(j + 1) + "]:" + str(abc.global_params[j]))
    print(str(run + 1) + ".run:" + str(abc.global_min))
    abc.global_mins[run] = abc.global_min
    mean += abc.global_min

mean /= abc.epochs
print("Means of " + str(abc.epochs) + " runs: " + str(mean))
