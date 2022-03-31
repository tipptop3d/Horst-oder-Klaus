#!/usr/bin/env pybricks-micropython

"""
Main File that gets executed by the Lego Robot
"""
import json
import math

from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

import uasyncio
from calculus.expression import Expression

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

# Distance driven = the amount of degrees multiplied by the angle ratio
# distance = angle * ANGLE_RATIO
# Angle needed for given distance = distance divided by angle ratio
# angle = distance / ANGLE_RATIO
# Same for speeds (replace distance with distance/time or angle with angle/time)
SIXTEEN_TEETH_GEAR_DIAMETER = 17.5  # mm
CIRCUMFERENCE = SIXTEEN_TEETH_GEAR_DIAMETER * math.pi
ANGLE_RATIO = CIRCUMFERENCE * (1/360)

# somehow the precision alters the speed, so maybe resulting in bugs
# if these bugs influences influence the real drawings, fuck a
# new algorithm is needed
PRECISION = 100  # intervals


class Plotter:
    def __init__(self, current_x=X_LEFT_BOUND, current_y=Y_UPPER_BOUND, lifted=False):
        self.current_x = current_x
        self.current_y = current_y

        self.lifted = lifted

        # testing range
        self.move_to(0, 0)
        self.move_to(X_RIGHT_BOUND, Y_UPPER_BOUND)
        self.move_to(y=Y_LOWER_BOUND)
        self.move_to(x=X_LEFT_BOUND)
        self.move_to(y=Y_UPPER_BOUND)

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

    def move_to(self, x=None, y=None, wait=True, x_wait=False):
        # no value, no movement
        if x is None:
            x = self.current_x
        if y is None:
            y = self.current_y

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

    def draw(self, expression):
        """Draws the expression.

        Args:
            expression (Expression): Expression to draw
        """
        # first derative
        fp = expression.diff()

        self.lift()
        self.move_to(X_LEFT_BOUND, Y_UPPER_BOUND)

        # calculate timings
        x_speed = (X_MAX_ANGLE_SPEED * ANGLE_RATIO)
        total_time = X_LENGTH / x_speed
        average_time = total_time / PRECISION

        # draw loop
        while self.current_x < X_RIGHT_BOUND:
            print(f'Coords: {self.current_x:.2f} {self.current_y:.2f}')
            x_angle_speed = X_MAX_ANGLE_SPEED
            y_speed = fp.evaluate(self.current_x)
            y_angle_speed = y_speed / ANGLE_RATIO
            abs_y_angle_speed = abs(y_angle_speed)

            speed_factor = 1.0
            # if y-speed exceeds, slow down x-motor to retain ratio
            # speed factor is the ratio of y to y_max
            # dividing it with our x-speed gives the lowered x-speed retaining ratio
            if abs_y_angle_speed > Y_MAX_ANGLE_SPEED:
                speed_factor = abs_y_angle_speed / Y_MAX_ANGLE_SPEED
                y_angle_speed = math.copysign(Y_MAX_ANGLE_SPEED, y_speed)
                x_angle_speed /= speed_factor

            motor_y.run(y_angle_speed)
            motor_x.run(x_angle_speed)

            # average time multiplied with speed factor gives the time
            time_spent = average_time * speed_factor

            # distance = velocity * time | s = v · t
            self.current_y += (y_angle_speed * ANGLE_RATIO) * time_spent
            self.current_x += (x_angle_speed * ANGLE_RATIO) * time_spent

            wait(time_spent)

        motor_x.hold()
        motor_y.hold()


async def print_callback(reader, writer):
    print('Connected with:', writer.get_extra_info('peername'))
    res = await reader.readline()
    try:
        obj = json.loads((res.decode('ascii')))
        expr = Expression(obj['tokens'])
        print('Expression: ', expr)
        plotter = Plotter()
        plotter.draw_test(expr)
    except Exception as e:
        print(e)
    reader.aclose()
    print('Released')


async def main():
    print('Started Server')
    server = await uasyncio.start_server(print_callback, '0.0.0.0', 64010, 1)
    await server.wait_closed()
    print('Closed Server')


loop = uasyncio.core.get_event_loop()
loop.run_until_complete(main())
