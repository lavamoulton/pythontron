# imports
import pygame
import random


class Cycle(object):
    """an object representing a cycle in the game
    can be an AI or a player, represented by the name
    takes initial x, y location, color, head_color, and direction as constructor variables
    also sets the dead boolean variable to False"""
    def __init__(self, name, pos_x, pos_y, direction, color, head_color):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        self.color = color
        self.head_color = head_color
        self.dead = False

    def set_name(self, name):
        """sets the name of this cycle object
            :param name: new name to use"""

        self.name = name

    def get_name(self):
        """gets the name of this cycle object"""

        return self.name

    def draw_cycle(self, display, box_width, box_height):
        """draws the cycle as a rectangle within the box dimensions
            :param display: the display to draw on passed in as an arg
            :param box_width: the width of one box on the grid
            :param box_height: the height of one box on the grid"""

        if not self.dead:
            cycle_rect = (self.pos_x * box_width+1, self.pos_y * box_height+1, box_width - 1, box_height - 1)
            pygame.draw.rect(display, self.head_color, cycle_rect)

    def update_cycle(self, grid):
        """updates the cycle if it is not dead based on its current position and the direction it is heading
            :param grid: grid representing all game objects present in the game"""

        grid[self.pos_x][self.pos_y] = self.color

        if not self.dead:
            if self.direction == "R":
                self.pos_x += 1
            elif self.direction == "L":
                self.pos_x -= 1
            elif self.direction == "U":
                self.pos_y -= 1
            elif self.direction == "D":
                self.pos_y += 1

    def set_direction(self, direction):
        """sets the direction the cycle is heading
            constraint that it cannot do a 180 degree turn
            :param direction: the direction to change to"""

        if direction == "U" and self.direction != "D":
            self.direction = direction
        elif direction == "D" and self.direction != "U":
            self.direction = direction
        elif direction == "R" and self.direction != "L":
            self.direction = direction
        elif direction == "L" and self.direction != "R":
            self.direction = direction

    def check_collision(self, grid):
        """checks if the cycle has collided with another object
            :param grid: the game grid passed in containing all other game objects"""

        if self.pos_x < 1 or self.pos_x > len(grid) - 2:
            self.kill_cycle(grid)
        elif self.pos_y < 1 or self.pos_y > len(grid[0]) - 2:
            self.kill_cycle(grid)
        elif grid[self.pos_x][self.pos_y]:
            self.kill_cycle(grid)

    def kill_cycle(self, grid):
        """sets the dead boolean to True
            calls the kill_walls method
            :param grid: the game grid passed in containing all other game objects"""

        self.dead = True
        self.kill_walls(grid)

        return grid

    def revive_cycle(self):
        """sets the dead boolean to False"""

        self.dead = False

    def kill_walls(self, grid):
        """destroys surrounding walls upon death of a cycle
            :param grid: the game grid passed in containing all other game objects"""

        # TODO: handle cases where the other object is another cycle
        # TODO: case where something is driving against the wall, walls not disappearing as intended

        if self.pos_x != len(grid) - 1:
            grid[self.pos_x + 1][self.pos_y] = False
        if self.pos_x != 0:
            grid[self.pos_x - 1][self.pos_y] = False
        if self.pos_y != len(grid[0]) - 1:
            grid[self.pos_x][self.pos_y + 1] = False
        if self.pos_y != 0:
            grid[self.pos_x][self.pos_y - 1] = False
        grid[self.pos_x][self.pos_y] = False

    def reset_position(self, pos_x, pos_y, direction):
        """puts the cycle in the given position with the given direction
            :param pos_x: x position to use
            :param pos_y: y position to use
            :param direction: direction to use"""

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction

    def is_dead(self):
        """returns True if the cycle is dead
            returns False otherwise"""

        return self.dead

    def call_ai(self, game_grid):
        """method to call AI for the non-human players in the game
            :param game_grid: 2D array representation of the game grid"""

        random_num = random.randint(1, 4)
        if random_num == 1 and self.direction != "R":
            self.set_direction("L")
        elif random_num == 2 and self.direction != "L":
            self.set_direction("R")
        elif random_num == 3 and self.direction != "D":
            self.set_direction("U")
        elif random_num == 4 and self.direction != "U":
            self.set_direction("D")

    def get_direction(self):
        """returns the direction the cycle is currently heading
            used for debugging purposes"""

        return self.direction

    def get_position(self):
        """returns the x and y coordinates of this cycle
            used for debugging purposes"""

        return self.pos_x, self.pos_y

    def set_position(self, pos_x, pos_y):
        """sets the x and y coordinates of the cycle
            :param pos_x: the x coordinate to shift to
            :param pos_y: the y coordinate to shift to"""

        self.pos_x = pos_x
        self.pos_y = pos_y

    def set_color(self, color):
        """sets the color of the cycle
            :param color: the color to change to"""

        self.color = color

    def get_color(self):
        """gets the color of the cycle"""

        return self.color

    def set_head_color(self, head_color):
        """sets the head color of the cycle
            :param head_color: the head color to change to"""

        self.head_color = head_color

    def get_head_color(self):
        """gets the head color of the cycle"""

        return self.head_color


