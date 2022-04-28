#!/usr/bin/env pybricks-micropython
"""
Main File that gets executed by the Lego Robot
"""
import json
import math

from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Direction, Port
from pybricks.tools import wait as wait_time

import uasyncio
from calculus.expression import Expression

# in mm
X_LENGTH = 128
X_LEFT_BOUND = -X_LENGTH/2
X_RIGHT_BOUND = X_LENGTH/2

Y_LENGTH = 55
Y_UPPER_BOUND = Y_LENGTH/2
Y_LOWER_BOUND = -Y_LENGTH/2

# in °/s
X_MAX_ANGLE_SPEED = 180
Y_MAX_ANGLE_SPEED = 180

# in °
ANGLE_TO_LIFT = 90


def calculate_angle_ratio(diameter):
    """Calculates the angle ratio for a given diameter, used
    for translating turn angle of a gear to distance on a gear rack.
    distance = degrees * angle ratio
    angle = distance / angle ratio
    Same for speeds.

    :param diameter: Median diameter of the gear
    :type diameter: float
    :return: Angle Ratio used for calculations
    :rtype: float
    """
    return diameter * math.pi * (1/360)


SIXTEEN_TEETH_GEAR_DIAMETER = 17.5  # mm
SIXTEEN_TEETH_ANGLE_RATIO = calculate_angle_ratio(SIXTEEN_TEETH_GEAR_DIAMETER)

TWENTYFOUR_TEETH_GEAR_DIAMETER = 22.0
TWENTYFOUR_TEETH_GEAR_ANGLE_RATIO = calculate_angle_ratio(
    TWENTYFOUR_TEETH_GEAR_DIAMETER)

angle_ratio = {
    'x': SIXTEEN_TEETH_ANGLE_RATIO,
    'y': TWENTYFOUR_TEETH_GEAR_ANGLE_RATIO
}


# somehow the precision alters the speed, so maybe resulting in bugs
# if these bugs influences influence the real drawings, fuck a
# new algorithm is needed
PRECISION = 100  # intervals


def find_start(expr):
    """Finds the drawing starting point of a given expression
    by iterating over the x length, respecting precision.

    :param expr: Expression to iterate over
    :type expr: Expression
    :return: tuple of (x, y) coordinates or None if no starting point
    is found
    :rtype: tuple[int, int] | None
    """
    x = X_LEFT_BOUND
    while x < X_RIGHT_BOUND:
        y = expr.evaluate(x)
        if Y_LOWER_BOUND < y < Y_UPPER_BOUND:
            return x, y
        x += X_LENGTH / PRECISION
    return None


class Plotter:
    """Class responsible for registering a drawing canvas."""

    def __init__(self, motor_x, motor_y, motor_z, lifted=False):
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.motor_z = motor_z

        self.current_x = X_LEFT_BOUND
        self.current_y = Y_UPPER_BOUND

        self.lifted = lifted

        # testing range
        # self.move_to((X_RIGHT_BOUND, self.current_y))
        # print('right top complete')
        # wait_time(1000)
        # self.move_to((self.current_x, Y_LOWER_BOUND))
        # print('right bottom complete')
        # wait_time(1000)
        # self.move_to((X_LEFT_BOUND, self.current_y))
        # print('left buttom complete')
        # wait_time(1000)
        # self.move_to((self.current_x, Y_UPPER_BOUND))
        # print('left top complete')
        # wait_time(1000)

    def lift(self, wait=True):
        """Lifts the pen if a z-motor is connected

        :param wait: Wait for the maneuver to complete before continuing
        with the rest of the program, defaults to True
        :type wait: bool, optional
        """
        if not self.motor_z:
            return
        if self.lifted:
            return

        self.motor_z.run_angle(360, ANGLE_TO_LIFT, wait=wait)
        self.lifted = True

    def lower(self, wait=True):
        """Lowers the pen if a z-motor is connected

        :param wait: Wait for the maneuver to complete before continuing
        with the rest of the program, defaults to True
        :type wait: bool, optional
        """
        if not self.motor_z:
            return
        if not self.lifted:
            return

        self.motor_z.run_angle(360, -ANGLE_TO_LIFT, wait=wait)
        self.lifted = False

    def move_to(self, coords, wait=True, parallel=False):
        """Moves to given Coords and updates current values. Retains lifted status.

        :param coords: Coords
        :type coords: tuple[int, int]
        :param wait: _description_, defaults to True
        :type wait: bool, optional
        :param parallel: Wait for the maneuver to complete before continuing
        with the rest of the program, defaults to True
        :type parallel: bool, optional
        :raises ValueError: Values are out of bounds
        """
        x, y = coords
        # same position, no movement needed
        if x == self.current_x and y == self.current_y:
            return

        if not (X_LEFT_BOUND <= x <= X_RIGHT_BOUND or Y_LOWER_BOUND <= y <= Y_UPPER_BOUND):
            raise ValueError('Values out of bounds')

        angle_x = (x - self.current_x) / angle_ratio['x']
        print('Angle X:', angle_x)
        angle_y = (y - self.current_y) / angle_ratio['y']
        print('Angle Y:', angle_y)

        # make sure to lift before moving, but retain old lift status
        was_lifted = self.lifted
        if not self.lifted:
            self.lift()

        self.motor_x.run_angle(X_MAX_ANGLE_SPEED, angle_x, wait=not parallel)
        self.motor_y.run_angle(Y_MAX_ANGLE_SPEED, angle_y, wait=wait)

        if not was_lifted:
            self.lower()

        self.current_x = x
        self.current_y = y


def draw(self, expr):
    """Main Logic. Draws the function on the paper.
    First moves the pen to the visible start of the function.
    Starts the x-motor, calculates speed of y-motor with help of
    the first derivative. If pen exceeds borders, stop y-motor.
    Adjust x-speed if y-speeds exceeds the maximum to retain x to y
    ratio. Calculate the time it should spent with help of the
    variation of the x speeds and the average x-speed and wait.

    :param expr: Expression to draw
    :type expr: Expression
    :yield: Progress of drawing. Ranging from 0 - 1.
    :rtype: float
    """
    # first derivative
    f_prime = expr.diff()

    self.lift()

    # calculate timings
    x_speed = (X_MAX_ANGLE_SPEED * angle_ratio['x'])
    total_time = X_LENGTH / x_speed  # t = s / v
    average_time = total_time / PRECISION

    self.move_to(find_start(expr))

    # draw loop
    while self.current_x < X_RIGHT_BOUND:
        x_angle_speed = X_MAX_ANGLE_SPEED
        self.motor_x.run(x_angle_speed)

        # stop y-motor if pen is not in bounds
        if not Y_LOWER_BOUND < expr.evaluate(self.current_x) < Y_UPPER_BOUND:
            y_speed = 0.0
        else:
            y_speed = f_prime.evaluate(self.current_x)
        y_angle_speed = y_speed / angle_ratio['y']

        # speed factor is the ratio of y to y_max
        speed_factor = 1.0
        # if y-speed exceeds, slow down x-motor to retain ratio
        if abs(y_angle_speed) > Y_MAX_ANGLE_SPEED:
            speed_factor = abs(y_angle_speed / Y_MAX_ANGLE_SPEED)
            # respect orientation
            y_angle_speed = math.copysign(Y_MAX_ANGLE_SPEED, y_speed)
            x_angle_speed /= speed_factor

        self.motor_y.run(y_angle_speed)
        self.motor_x.run(x_angle_speed)

        # average time multiplied with speed factor
        # gives the actual time for the current speeds
        time_spent = average_time * speed_factor

        # needed for loop
        # s = v · t
        self.current_y += (y_angle_speed * angle_ratio['y']) * time_spent
        self.current_x += (x_angle_speed * angle_ratio['x']) * time_spent

        percentage = (self.current_x + X_LENGTH / 2) / X_LENGTH
        yield percentage

        # adjust for ms
        wait_time(time_spent * 1000)

    self.motor_x.hold()
    self.motor_y.hold()

    self.move_to((X_LEFT_BOUND, Y_UPPER_BOUND))


brick = EV3Brick()

motor_x = Motor(Port.A, gears=[[24, 20], [16]])
motor_y = Motor(Port.C, gears=[24],
                positive_direction=Direction.COUNTERCLOCKWISE)
# motor_z = Motor(Port.C)


async def print_callback(reader, writer):
    """Gets executed everytime the TCP-Server receives a connection

    :param reader: Reader-Stream
    :type reader: StreamReader
    :param writer: Writer-Stream
    :type writer: StreamWriter
    """
    print('Connected with:', writer.get_extra_info('peername'))
    res = await reader.readline()

    try:
        response = json.loads((res.decode('ascii')))
    except json.JSONDecodeError as err:
        reader.aclose()
        return err

    expr = Expression(response['tokens'])
    lifted = response['lifted']
    print('Expression: ', expr)

    plotter = Plotter(motor_x, motor_y, None, lifted=lifted)
    for percentage in plotter.draw(expr):
        print(percentage)

    reader.aclose()


async def main():
    """Starts server"""
    print('Started Server')
    server = await uasyncio.start_server(print_callback, '0.0.0.0', 64010, 1)
    await server.wait_closed()
    print('Closed Server')


def debug():
    """Tries to draw without opening a server"""
    plotter = Plotter(motor_x, motor_y, None)
    tokens = ['(VAL:0.0003)', '(VAR:x)', '(VAL:3.0)', '(POW:^)', '(TIMES:*)']
    tokens = ['VAR:x']
    expr = Expression(tokens)
    for percentage in plotter.draw(expr):
        print(percentage)


DEBUG_MODE = True

if DEBUG_MODE:
    debug()
else:
    loop = uasyncio.core.get_event_loop()
    loop.run_until_complete(main())
