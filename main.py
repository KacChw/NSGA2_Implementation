from algorithm import *
from simulation import plot_all_trajectories, visualize_trajectory
from deap import algorithms
import numpy as np
from perpendicular_parking import visualize_perpendicular_parking
from alternate_parking import visualize_alternate_parking
from deap import algorithms


def main():
    # Tworzenie populacji i uruchamianie NSGA-II
    toolbox = base.Toolbox()
    toolbox.register("individual", init_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", crossover)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", evaluate)

    population = toolbox.population(n=100)
    algorithms.eaMuPlusLambda(population, toolbox, mu=100, lambda_=200, cxpb=0.7, mutpb=0.2, ngen=100)

    # Wybór scenariusza parkowania
    scenario = input(
        "Wybierz scenariusz: (1) Parkowanie równoległe, (2) Parkowanie prostopadłe, (3) Alternatywne miejsce parkingowe: ")

    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
    print(f"Znaleziono {len(pareto_front)} rozwiązań Pareto.")

    for i, ind in enumerate(pareto_front[:5]):
        print(f"Trajektoria {i + 1}: Time: {ind.fitness.values[0]}, Quality: {ind.fitness.values[1]}")
        if scenario == "1":
            visualize_trajectory(ind)
        elif scenario == "2":
            visualize_perpendicular_parking(ind)
        elif scenario == "3":
            visualize_alternate_parking(ind)


if __name__ == "__main__":
    main()

