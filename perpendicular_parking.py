import matplotlib.pyplot as plt
from car import Car
from parking import is_colliding_with_lines, draw_parking_lines


def visualize_perpendicular_parking(individual):
    # Tworzymy samochód, przekazując funkcję `is_colliding_with_lines` jako `collision_check`
    car = Car(0, 0, 3.5, 1.75, 0, 2.4, 30, is_colliding_with_lines)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim([-15, 15])
    ax.set_ylim([-15, 15])
    ax.set_aspect('equal')
    ax.grid(True)

    # Ustawienia miejsca parkingowego na osi Y, prostopadle do początkowej pozycji auta
    parking_x, parking_y = 0, -10  # Przykładowe współrzędne miejsca parkingowego
    draw_parking_lines(ax)

    for move_direction, steering_change in individual:
        if car.is_parked():
            print("Samochód zaparkował prostopadle!")
            break
        car.steer(steering_change)
        car.move(move_direction)
        car.draw(ax)
        draw_parking_lines(ax)  # Rysuj linie przy każdej aktualizacji
        plt.pause(0.1)
    plt.show()
