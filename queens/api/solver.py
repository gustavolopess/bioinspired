from queens.api.chessboard import Chessboard, crossover
from queens.api.charts import line_chart
import random


class Population(list):
    def __init__(self, population_size):
        super(Population, self).__init__()
        self.population_size = population_size
        self.mean = 0

    def insort(self, ind: Chessboard):
        l, r = 0, self.__len__()
        while l < r:
            mid = int((l + r) / 2)
            if ind.fitness > self[mid].fitness:
                l = mid + 1
            else:
                r = mid
        self.insert(l, ind)
        self.evaluate_mean()

    def better2of5(self):
        _5selected = list([])
        for i in range(5):
            idx = random.randint(0, self.__len__() - 1)
            _5selected.append(self[idx])
        _5selected = sorted(_5selected, key=lambda ind: ind.fitness)
        _2better = _5selected[-2:]
        return crossover(_2better[0], _2better[1])

    def mutate(self):
        ind = random.randint(0, self.__len__() - 1)
        self[ind].mutate()
        self.evaluate_mean()

    def pop_front(self):
        del self[0]

    def evaluate_mean(self):
        self.mean = sum(ind.fitness for ind in self)/float(self.__len__())


def solve(n_queens, population_size, repr_optimization, rec_prob: float, mut_prob: float, max_fits: int, to_django=False):
    population = Population(population_size)

    for i in range(population_size):
        individual = Chessboard(n_queens=n_queens, repr_optimization=repr_optimization)
        population.insort(individual)

    iterations = 0
    gens_mean, gens_higher = [population.mean], [population[-1].fitness]
    while population[-1].fitness < 0 and iterations < max_fits:
        p = random.uniform(0, 1)
        if p <= rec_prob:
            c1, c2 = population.better2of5()
            if c1.fitness > c2.fitness:
                c1, c2 = c2, c1
            if c1.fitness >= population[0].fitness:
                population.pop_front()
                population.insort(c1)
            if c2.fitness >= population[0].fitness:
                population.pop_front()
                population.insort(c2)
        if p <= mut_prob:
            population.mutate()
        iterations += 1
        gens_mean.append(population.mean)
        gens_higher.append(population[-1].fitness)

    return {
        'candidate_solution': population[-1],
        'iterations': iterations,
        'mean_high_plot': line_chart(gens_mean, gens_higher, to_django=to_django)
    }



if __name__ == '__main__':
    solve(8, 1000, True, 0.9, 0.4, 10000)