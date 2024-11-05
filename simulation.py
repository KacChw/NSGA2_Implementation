import matplotlib.pyplot as plt
from car import Car
from parking import draw_parking_lines, is_colliding_with_lines

def visualize_trajectory(individual):
    car = Car(0, 0, 3.5, 1.75, 0, 2.4, 30, is_colliding_with_lines)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim([-15, 15])
    ax.set_ylim([-15, 15])
    ax.set_aspect('equal')
    ax.grid(True)
    draw_parking_lines(ax)
    for move_direction, steering_change in individual:
        if car.is_parked():
            print("Samochód zaparkował!")
            break
        car.steer(steering_change)
        car.move(move_direction)
        car.draw(ax)
        draw_parking_lines(ax)  # Rysuj linie przy każdej aktualizacji
        plt.pause(0.1)
    plt.show()

def plot_all_trajectories(trajectories):
    fig, ax = plt.subplots(figsize=(12, 8))
    for traj in trajectories:
        ax.plot(traj['x'], traj['y'], linewidth=0.5)
    ax.set_xlim([-15, 15])
    ax.set_ylim([-15, 15])
    ax.set_aspect('equal')
    ax.grid(True)
    plt.show()