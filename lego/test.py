from calculus.expression import Expression
import math

X_LENGTH = 100
Y_LENGTH = 60
X_MAX_SPEED = 360

# wir gehen jetzt davon aus, dass eine Umdrehung (360°) 20mm Distanz enstpricht
# 

class Plot:
    def __init__(self, max_x, max_y, current_x = 0, current_y = 0) -> None:
        """from top left to bottom right"""
        self.max_x = max_x
        self.max_y = max_y
        self.current_x = current_x
        self.current_y = current_y

        self.CONVERSION_RATIO = 10

    @property
    def ratio(self):
        return self.max_x / self.max_y

    def move_to(self, x, y):
        if x > self.max_x or y > self.max_y:
            raise ValueError('Values out of bounds')
        
        distance_x = x - self.current_x
        distance_y = y - self.current_y

        


def int_length(n):
    if 0 > n > 1:
        return int(math.log10(n))-1
    elif n > 0:
        return int(math.log10(n))+1
    elif n < 0:
        return int(math.log10(n))+1
    else:
        return 1

def draw_expr(f, start = -5, end = 5):
    f_prime = f.diff()

    # calculate min and max
    y_values = set()
    step = (end - start) / 1000
    round_to = max(4 - int_length(end - start), 0)
    print(round_to)

    count = 0
    while True:
        n = round(start + count * step, round_to)
        if n > end:
            break
        print(n)
        y_values.add(f.evaluate(n))
        count += 1
    
    max_value = max(y_values) # margin
    min_value = min(y_values)



    return max_value, min_value


def test():
    f = Expression('x ^ 2')
    print(draw_expr(f, 0, 1))


if __name__ == '__main__':
    test()
