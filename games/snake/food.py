import random


def create_food(snake, box):
    while True:
        food = [
            random.randint(box[0][0] + 1, box[1][0] - 1),
            random.randint(box[0][1] + 1, box[1][1] - 1)
        ]

        if food not in snake:
            return food
