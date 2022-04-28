"""
Test File
"""
import asyncio
import math
import matplotlib.pyplot as plt

import time
from calculus.expression import Expression

# Dummies


class Port:
    A = 'A'
    B = 'B'
    C = 'C'


class Motor:
    def __init__(self, port, gears=None) -> None:
        self.port = port
        self.gears = gears

    def run_angle(self, speed, angle, wait=True):
        # print('{}: Running to angle {} at speed {}'.format(self.port, speed, angle))
        pass

    def run(self, speed):
        # print('{}: Running at speed {}'.format(self.port, speed))
        pass

    def hold(self):
        pass


def wait(ms):
    time.sleep(ms)


DRAW_ASPECT_RATIO = 10/6  # x:y

# Motors

motor_x = Motor(Port.A, gears=[20, 16])
motor_y = Motor(Port.B, gears=[16])
motor_z = Motor(Port.C)

# in mm

X_LENGTH = 127
X_LEFT_BOUND = -X_LENGTH/2
X_RIGHT_BOUND = X_LENGTH/2

Y_LENGTH = 91
Y_UPPER_BOUND = Y_LENGTH/2
Y_LOWER_BOUND = -Y_LENGTH/2

# in °/s

X_MAX_ANGLE_SPEED = 360
Y_MAX_ANGLE_SPEED = 720

# in °

ANGLE_TO_LIFT = 90

# Distance driven equals the amount of degrees multiplied by the angle ratio
# distance = angle * ANGLE_RATIO
# Angle needed for given distance is distance divided by angle ratio
# angle = distance / ANGLE_RATIO
# Same for speeds (replace distance with distance/time or angle with angle/time)

SIXTEEN_TEETH_GEAR_DIAMETER = 17.5  # mm
CIRCUMFERENCE = SIXTEEN_TEETH_GEAR_DIAMETER * math.pi
ANGLE_RATIO = CIRCUMFERENCE * (1/360)

PRECISION = 1000  # 100 intervals
# somehow the precision alters the speed, so maybe resulting in bugs
# if these bugs influences influence the real drawings
# fuck new algorithm is needed


def find_start(f):
    x = X_LEFT_BOUND
    while x < X_RIGHT_BOUND:
        x += X_LENGTH / PRECISION
        y = f.evaluate(x)
        if Y_LOWER_BOUND < y < Y_UPPER_BOUND:
            return x, y


class Plotter:
    def __init__(self, current_x=X_LEFT_BOUND, current_y=Y_UPPER_BOUND, lifted=False):
        self._current_x = current_x
        self._current_y = current_y

        self.lifted = lifted

    @property
    def current_x(self):
        return self._current_x

    @current_x.setter
    def current_x(self, value):
        # print('x', value)
        self._current_x = value

    @property
    def current_y(self):
        return self._current_y

    @current_y.setter
    def current_y(self, value):
        # print('y', value)
        self._current_y = value

    @property
    def coords(self):
        return self.current_x, self.current_y

    def lift(self, wait=True):
        if self.lifted:
            return

        motor_z.run_angle(360, ANGLE_TO_LIFT, wait=wait)
        self.lifted = True

    def lower(self, wait=True):
        if not self.lifted:
            return

        motor_z.run_angle(360, -ANGLE_TO_LIFT, wait=wait)
        self.lifted = False

    def move_to(self, coords, wait=True, x_wait=False):
        x, y = coords
        # same position, no movement needed
        if x == self.current_x and y == self.current_y:
            return

        if not (X_LEFT_BOUND <= x <= X_RIGHT_BOUND or Y_LOWER_BOUND <= y <= Y_UPPER_BOUND):
            raise ValueError('Values out of bounds')

        angle_x = (x - self.current_x) / ANGLE_RATIO
        angle_y = (y - self.current_y) / ANGLE_RATIO

        # make sure to lift before moving, but retain old lift status
        was_lifted = self.lifted
        if not self.lifted:
            self.lift()

        motor_x.run_angle(X_MAX_ANGLE_SPEED, angle_x, wait=x_wait)
        motor_y.run_angle(Y_MAX_ANGLE_SPEED, angle_y, wait=wait)

        if not was_lifted:
            self.lower()

        self.current_x = x
        self.current_y = y

    def draw(self, f):
        """Draws the expression

        Args:
            f (Expression): Expression to draw

        Yields:
            float: percentage of progress
        """
        # first derative
        fp = f.diff()

        x_points = []
        y_points = []

        self.lift()

        # calculate timings
        x_speed = (X_MAX_ANGLE_SPEED * ANGLE_RATIO)
        total_time = X_LENGTH / x_speed  # t = s / v
        average_time = total_time / PRECISION

        self.move_to(find_start(f))

        # draw loop
        while self.current_x < X_RIGHT_BOUND:
            x_angle_speed = X_MAX_ANGLE_SPEED
            motor_x.run(x_angle_speed)

            if not (Y_LOWER_BOUND < f.evaluate(self.current_x) < Y_UPPER_BOUND):
                y_speed = 0.0
                print('not in bounds')
            else:
                y_speed = fp.evaluate(self.current_x)
            y_angle_speed = y_speed / ANGLE_RATIO

            # speed factor is the ratio of y to y_max
            speed_factor = 1.0
            # if y-speed exceeds, slow down x-motor to retain ratio
            if abs(y_angle_speed) > Y_MAX_ANGLE_SPEED:
                speed_factor = abs(y_angle_speed / Y_MAX_ANGLE_SPEED)
                # respect orientation
                y_angle_speed = math.copysign(Y_MAX_ANGLE_SPEED, y_speed)
                x_angle_speed /= speed_factor

            motor_x.run(x_angle_speed)
            motor_y.run(y_angle_speed)

            # average time multiplied with speed factor
            # gives the actual time for the current speeds
            time_spent = average_time * speed_factor

            # needed for loop
            # s = v · t
            self.current_x += (x_angle_speed * ANGLE_RATIO) * time_spent
            self.current_y += (y_angle_speed * ANGLE_RATIO) * time_spent

            # scatter diagram
            x_points.append(self.current_x)
            y_points.append(self.current_y)

            percentage = (self.current_x + X_LENGTH / 2) / X_LENGTH
            yield percentage

            wait(time_spent)

        plt.scatter(x_points, y_points)
        plt.show()


async def main():
    p = Plotter()
    # tokens = ['(VAL:0.1)', '(VAR:x)', '(TIMES:*)', '(SIN:sin)', '(VAL:30.0)', '(TIMES:*)']
    tokens = ['(VAL:0.1)', '(VAR:x)', '(VAL:2.0)', '(POW:^)', '(TIMES:*)']
    expr = Expression(tokens)
    print(expr)
    for p in p.draw(expr):
        print(p)


if __name__ == '__main__':
    asyncio.run(main())
