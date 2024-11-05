import numpy as np
import matplotlib.pyplot as plt


def is_colliding_with_lines(car):
    # Poziome linie: zmienna Y jest stała, X zmienia się w zakresie
    horizontal_lines = [
        (-15, -10, -2.5),  # Pozioma linia po lewej
        (-3, 15, -2.5),  # Pozioma linia po prawej
        (-10, -3, -5)  # Pozioma linia dolna
    ]

    # Pionowe linie: zmienna X jest stała, Y zmienia się w zakresie
    vertical_lines = [
        (-10, -5, -2.5),  # Pionowa linia po lewej
        (-3, -5, -2.5)  # Pionowa linia po prawej
    ]

    # Sprawdzenie kolizji z poziomymi liniami
    for line in horizontal_lines:
        if (line[0] <= car.x <= line[1]) and abs(car.y - line[2]) < 0.5:
            return True

    # Sprawdzenie kolizji z pionowymi liniami
    for line in vertical_lines:
        if (line[1] <= car.y <= line[2]) and abs(car.x - line[0]) < 0.5:
            return True

    return False


def draw_parking_lines(ax):
    # Poziome linie
    horizontal_lines = [
        (-15, -10, -2.5),  # Pozioma linia po lewej
        (-3, 15, -2.5),  # Pozioma linia po prawej
        (-10, -3, -5)  # Pozioma linia dolna
    ]

    # Pionowe linie
    vertical_lines = [
        (-10, -5, -2.5),  # Pionowa linia po lewej
        (-3, -5, -2.5)  # Pionowa linia po prawej
    ]

    # Rysowanie poziomych linii
    for line in horizontal_lines:
        ax.plot([line[0], line[1]], [line[2], line[2]], color='black', lw=3)

    # Rysowanie pionowych linii
    for line in vertical_lines:
        ax.plot([line[0], line[0]], [line[1], line[2]], color='black', lw=3)
