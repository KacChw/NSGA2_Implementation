import numpy as np
import matplotlib.pyplot as plt

class Car:
    def __init__(self, x, y, width, height, orientation, wheelbase, max_steering_angle, collision_check):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation
        self.velocity = 1
        self.wheelbase = wheelbase
        self.steering_angle = 0
        self.max_steering_angle = max_steering_angle
        self.trajectory_x = [self.x]
        self.trajectory_y = [self.y]
        self.steps = 0
        self.collision_check = collision_check  # Funkcja sprawdzająca kolizję

    def move(self, direction):
        # Zapisz bieżącą pozycję, aby móc ją przywrócić w razie kolizji
        previous_x, previous_y, previous_orientation = self.x, self.y, self.orientation

        # Przekształć orientację i kąt skrętu na radiany
        orientation_rad = np.radians(self.orientation)
        steering_rad = np.radians(self.steering_angle)

        # Oblicz promień skrętu, jeśli kąt skrętu jest różny od zera
        if self.steering_angle != 0:
            turning_radius = self.wheelbase / np.tan(steering_rad)
            delta_orientation = (self.velocity / turning_radius) * direction
        else:
            delta_orientation = 0

        # Zaktualizuj orientację i pozycję
        self.orientation += np.degrees(delta_orientation)
        self.orientation %= 360
        self.x += self.velocity * np.cos(np.radians(self.orientation)) * direction
        self.y += self.velocity * np.sin(np.radians(self.orientation)) * direction

        # Sprawdź kolizję; jeśli wykryto kolizję, przywróć poprzednią pozycję
        if self.collision_check(self):
            self.x, self.y, self.orientation = previous_x, previous_y, previous_orientation
        else:
            # Zapisz nową trajektorię, jeśli nie wykryto kolizji
            center_x = self.x + self.wheelbase / 2 * np.cos(np.radians(self.orientation))
            center_y = self.y + self.wheelbase / 2 * np.sin(np.radians(self.orientation))
            self.trajectory_x.append(center_x)
            self.trajectory_y.append(center_y)

    def steer(self, angle):
        self.steering_angle += angle
        self.steering_angle = max(-self.max_steering_angle, min(self.max_steering_angle, self.steering_angle))


    def draw(self, ax):
        ax.clear()
        ax.set_xlim([-15, 15])
        ax.set_ylim([-15, 15])
        ax.set_aspect('equal')
        ax.grid(True)

        # Miejsce parkingowe jako prostokąt
        parking_x, parking_y, parking_width, parking_height = -10, -5, 7, 2.5
        parking_rect = plt.Rectangle((parking_x, parking_y), parking_width, parking_height, edgecolor="grey", fill=False, linestyle='dashed', lw=2)
        ax.add_patch(parking_rect)

        # Rysowanie samochodu
        center_x = self.x + self.wheelbase / 2 * np.cos(np.radians(self.orientation))
        center_y = self.y + self.wheelbase / 2 * np.sin(np.radians(self.orientation))
        angle_rad = np.radians(self.orientation)
        rect = plt.Rectangle((-self.width / 2, -self.height / 2), self.width, self.height, edgecolor="blue", fill=False, lw=2)
        transform = plt.matplotlib.transforms.Affine2D().rotate(angle_rad).translate(center_x, center_y)
        rect.set_transform(transform + ax.transData)
        ax.add_patch(rect)

        # Rysowanie kół jako linie
        self._draw_wheels(ax, angle_rad, center_x, center_y)

        # Rysowanie trajektorii
        ax.plot(self.trajectory_x, self.trajectory_y, 'g--', lw=2)

    def _draw_wheels(self, ax, angle_rad, center_x, center_y):
        # Rysowanie tylnych i przednich kół jako linie
        wheel_length = 0.5

        # Tylna oś
        rear_left_x = self.x - (self.height / 2) * np.sin(angle_rad)
        rear_left_y = self.y + (self.height / 2) * np.cos(angle_rad)
        rear_right_x = self.x + (self.height / 2) * np.sin(angle_rad)
        rear_right_y = self.y - (self.height / 2) * np.cos(angle_rad)

        # Przednia oś z uwzględnieniem kąta skrętu
        front_axle_x = self.x + self.wheelbase * np.cos(angle_rad)
        front_axle_y = self.y + self.wheelbase * np.sin(angle_rad)
        steering_rad = np.radians(self.steering_angle)
        front_left_x = front_axle_x - (self.height / 2) * np.sin(angle_rad + steering_rad)
        front_left_y = front_axle_y + (self.height / 2) * np.cos(angle_rad + steering_rad)
        front_right_x = front_axle_x + (self.height / 2) * np.sin(angle_rad + steering_rad)
        front_right_y = front_axle_y - (self.height / 2) * np.cos(angle_rad + steering_rad)

        # Rysowanie linii reprezentujących koła
        ax.plot([rear_left_x - wheel_length * np.cos(angle_rad), rear_left_x + wheel_length * np.cos(angle_rad)],
                [rear_left_y - wheel_length * np.sin(angle_rad), rear_left_y + wheel_length * np.sin(angle_rad)], 'k-', lw=3)
        ax.plot([rear_right_x - wheel_length * np.cos(angle_rad), rear_right_x + wheel_length * np.cos(angle_rad)],
                [rear_right_y - wheel_length * np.sin(angle_rad), rear_right_y + wheel_length * np.sin(angle_rad)], 'k-', lw=3)
        ax.plot([front_left_x - wheel_length * np.cos(angle_rad + steering_rad), front_left_x + wheel_length * np.cos(angle_rad + steering_rad)],
                [front_left_y - wheel_length * np.sin(angle_rad + steering_rad), front_left_y + wheel_length * np.sin(angle_rad + steering_rad)], 'r-', lw=3)
        ax.plot([front_right_x - wheel_length * np.cos(angle_rad + steering_rad), front_right_x + wheel_length * np.cos(angle_rad + steering_rad)],
                [front_right_y - wheel_length * np.sin(angle_rad + steering_rad), front_right_y + wheel_length * np.sin(angle_rad + steering_rad)], 'r-', lw=3)

    def is_parked(self):
        # Funkcja do sprawdzenia, czy samochód znajduje się w miejscu parkingowym
        parking_x, parking_y, parking_width, parking_height = -10, -5, 7, 2.5
        corners = [
            (self.x - (self.width / 2) * np.cos(np.radians(self.orientation)) - (self.height / 2) * np.sin(np.radians(self.orientation)),
             self.y - (self.width / 2) * np.sin(np.radians(self.orientation)) + (self.height / 2) * np.cos(np.radians(self.orientation))),
            (self.x + (self.width / 2) * np.cos(np.radians(self.orientation)) - (self.height / 2) * np.sin(np.radians(self.orientation)),
             self.y + (self.width / 2) * np.sin(np.radians(self.orientation)) + (self.height / 2) * np.cos(np.radians(self.orientation))),
            (self.x - (self.width / 2) * np.cos(np.radians(self.orientation)) + (self.height / 2) * np.sin(np.radians(self.orientation)),
             self.y - (self.width / 2) * np.sin(np.radians(self.orientation)) - (self.height / 2) * np.cos(np.radians(self.orientation))),
            (self.x + (self.width / 2) * np.cos(np.radians(self.orientation)) + (self.height / 2) * np.sin(np.radians(self.orientation)),
             self.y + (self.width / 2) * np.sin(np.radians(self.orientation)) - (self.height / 2) * np.cos(np.radians(self.orientation)))
        ]
        for corner in corners:
            if not (parking_x <= corner[0] <= parking_x + parking_width and parking_y <= corner[1] <= parking_y + parking_height):
                return False
        return True