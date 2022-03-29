#!/usr/bin/env pybricks-micropython

"""
Main File that gets executed by the Lego Robot
"""
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
import uasyncio
from .calculus.expression import Expression

DRAW_ASPECT_RATIO = 10/6 # x:y

motorX = Motor(Port.A, gears=[20, 16])
motorY = Motor(Port.B, gears=[16])
motorZ = Motor(Port.C)

X_LENGTH = 100
X_LEFT_BOUND = -X_LENGTH/2
X_RIGHT_BOUND = X_LENGTH/2

Y_LENGTH = 60
Y_UPPER_BOUND = Y_LENGTH/2
Y_LOWER_BOUND = -Y_LENGTH/2

X_SPEED = 180
X_MAX_SPEED = 360
Y_MAX_SPEED = 360

ANGLE_LIFTED = 0
ANGLE_LOWERED = 180

PRECISION = 100 # 100 intervals

# wir gehen jetzt davon aus, dass eine Umdrehung (360°) 20mm Distanz enstpricht
# Distanz in mm * ANGLE_RATIO = Grad
# Grad / ANGLE_RATIO = Distanz
ANGLE_RATIO = 18



class Plotter:
    def __init__(self, expression, stream = None, current_x = X_LEFT_BOUND, current_y = Y_UPPER_BOUND, lifted = False):
        """from top left to bottom right"""
        self.f = expression
        self.stream = stream

        self.current_x = current_x
        self.current_y = current_y

        self.lifted = lifted
        if lifted:
            motorZ.reset_angle(ANGLE_LIFTED)
        else:
            motorZ.reset_angle(ANGLE_LOWERED)

    @property
    def ratio(self):
        return self.max_x / self.max_y

    def lift(self):
        if self.lifted:
            return

        motorZ.run_target(360, ANGLE_LIFTED)
        self.lifted = True
    
    def lower(self):
        if not self.lifted:
            return

        motorZ.run_target(360, ANGLE_LOWERED)
        self.lifted = False

    def move_to(self, x=None, y=None, wait=False):
        if x is None:
            x = self.current_x
        if y is None:
            y = self.current_y

        if x == self.current_x and y == self.current_y:
            return

        if not (X_LEFT_BOUND < x < X_RIGHT_BOUND or Y_LOWER_BOUND < y < Y_UPPER_BOUND):
            raise ValueError('Values out of bounds')
        
        angle_x = (x - self.current_x) * ANGLE_RATIO
        angle_y = (y - self.current_y) * ANGLE_RATIO

        was_lifted = self.lifted

        if not self.lifted:
            self.lift_up()

        motorX.run_angle(X_MAX_SPEED, angle_x, wait=False)
        motorY.run_angle(Y_MAX_SPEED, angle_y, wait=wait)

        if not was_lifted:
            self.lower()

        self.current_x = x
        self.current_y = y
    
    async def draw(self):
        fp = self.f.diff()
        self.lift_up()

         # find start
        coords = None
        for x in range(X_RIGHT_BOUND, X_LEFT_BOUND+1):
            y = self.f.evaluate(x)
            if -30 < y < 30:
                coords = x, y
                break
        
        self.move_to(*coords)

        # draw
        # 20 mm/s, Strecke := 100 - current_x, t := strecke / 20 mm/s
        s = X_LENGTH - self.current_x
        t = s / (X_SPEED / ANGLE_RATIO)
        interval = t / PRECISION
        current_time = 0
        motorX.run(X_SPEED)
        while current_time <= t:
            self.current_x += 1
            current_time += interval
            
            current_y = self.f.evaluate(self.current_x)
            y_speed = X_SPEED * fp.evaluate(self.current_x)

            if not Y_LOWER_BOUND > current_y > Y_UPPER_BOUND:
                self.lift_up()
                motorY.hold()
                wait(interval)
                continue

            self.current_y = current_y
            self.lower()

            y_speed = X_SPEED * fp.evaluate(self.current_x)
            motorY.run(y_speed)
            if self.stream:
                percentage = round(t / current_time * 255)
                byte = (percentage).to_bytes(1, 'big', signed=False)
                await self.stream.awrite(byte)
            wait(interval)
        motorX.hold()
        motorY.hold()


async def print_callback(reader, writer):
    print('Connected with:', writer.get_extra_info('peername'))
    res = await reader.readline()
    expr = Expression(res)
    print('Expression: ', expr)
    plotter = Plotter(expr, writer)
    await plotter.draw()
    await reader.aclose()
    print('Released')

async def main():
    print('Started Server')
    server = await uasyncio.start_server(print_callback, '0.0.0.0', 64010, 1)
    await server.wait_closed()
    print('Closed Server')



loop = uasyncio.core.get_event_loop()
loop.run_until_complete(main())