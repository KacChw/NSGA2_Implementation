import random
import numpy as np
from deap import base, creator, tools
from car import Car
from parking import is_colliding_with_lines

creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)


def init_individual():
    individual = creator.Individual()
    for _ in range(150):  # Każdy osobnik to lista 150 ruchów
        move_direction = random.choice([0.6, -0.6])  # Ruch do przodu/tyłu
        steering_change = random.choice([-5, 0, 5])  # Skręt
        individual.append((move_direction, steering_change))
    return individual


# Funkcja oceny trajektorii
def evaluate(individual):
    car = Car(0, 0, 3.5, 1.75, 0, 2.4, 30,is_colliding_with_lines)
    initial_x, initial_y = car.x, car.y  # Pozycja początkowa samochodu
    steps = 0
    distance_travelled = 0
    total_steering_angle = 0
    prev_distance_to_center = float('inf')  # Poprzednia odległość od centrum miejsca parkingowego

    parking_center_x = -6.5  # Środek miejsca parkingowego
    parking_center_y = -3.75
    reverse_bonus = 0  # Inicjalizacja bonusu za cofanie
    penalty_collision = 10000  # Wysoka kara za kolizję z linią

    for move_direction, steering_change in individual:
        prev_x, prev_y = car.x, car.y  # Pozycja przed ruchem
        car.steer(steering_change)  # Najpierw ustaw skręt kół
        car.move(move_direction)  # Potem wykonaj rzeczywisty ruch
        steps += 1

        # Sprawdzamy, czy samochód koliduje z czarnymi liniami
        if is_colliding_with_lines(car):
            # Natychmiast kończymy symulację z maksymalną karą
            return penalty_collision, 0

        # Obliczamy dystans pokonany w tym kroku
        distance_travelled += np.sqrt((car.x - prev_x) ** 2 + (car.y - prev_y) ** 2)

        # Dodajemy karę, jeśli samochód zbytnio oddala się od parkingu
        if np.abs(car.x) > 20 or np.abs(car.y) > 20:
            return 1000, 0  # Bardzo wysoka kara za oddalenie

        # Obliczamy bieżącą odległość od środka miejsca parkingowego
        current_distance_to_center = np.sqrt((car.x - parking_center_x) ** 2 + (car.y - parking_center_y) ** 2)

        # Nagroda za przybliżanie się do miejsca parkingowego
        distance_improvement_bonus = 0
        if current_distance_to_center < prev_distance_to_center:
            distance_improvement_bonus = (prev_distance_to_center - current_distance_to_center) * 5  # Nagroda za zmniejszenie odległości

        # Zaktualizuj poprzednią odległość do celu
        prev_distance_to_center = current_distance_to_center

        # Bonus za jazdę tyłem (jeśli samochód cofa, a koła są skręcone o więcej niż 10 stopni)
        if move_direction == -0.6 and abs(car.steering_angle) > 10:
            reverse_bonus += 2  # Dodajemy premię za cofanie ze skręconymi kołami

        # Sprawdzenie warunków zaparkowania
        if car.is_parked():
            break

    # Cel 1: minimalizacja kroków
    time_cost = steps

    # Cel 2: maksymalizacja jakości parkowania
    if car.is_parked():
        # Kary za orientację nieoptymalną (nie równoległą)
        orientation_penalty = abs(car.orientation) % 360
        if orientation_penalty > 10:
            orientation_penalty = 10  # Maksymalna kara za orientację

        # Kara za nadmierną odległość od środka miejsca parkingowego
        distance_penalty = current_distance_to_center

        # Im mniejsza odległość do środka i lepsza orientacja, tym wyższa jakość
        quality = 1 / (1 + distance_penalty + distance_travelled - distance_improvement_bonus - reverse_bonus)
    else:
        quality = 0

    return time_cost, quality

def crossover(ind1, ind2):
    size = min(len(ind1), len(ind2))
    cx_point = random.randint(1, size - 1)
    ind1[cx_point:], ind2[cx_point:] = ind2[cx_point:], ind1[cx_point:]
    return ind1, ind2

def mutate(individual):
    index = random.randrange(len(individual))
    move_direction = random.choice([1, -1])
    steering_change = random.choice([-5, 0, 5])
    individual[index] = (move_direction, steering_change)
    return individual,