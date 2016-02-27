# necessary imports
from button import *
from pygame import *
import sys

'''initial vars'''
GAME_CLOCK = 30
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
GRID_WIDTH = 128
GRID_HEIGHT = 128
BOX_WIDTH = SCREEN_WIDTH / GRID_WIDTH
BOX_HEIGHT = SCREEN_HEIGHT / GRID_HEIGHT

'''colors, colors everywhere'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


def main():
    """main function, contains the main game loop"""

    # this game has got to start somewhere, let's initialize some things
    pygame.init()
    global FPS_CLOCK
    global GRID_DISPLAY
    global TITLE_FONT
    global BUTTON_FONT
    global HELP_FONT
    global button_list

    # create some fonts for later
    TITLE_FONT = pygame.font.SysFont("monospace", SCREEN_WIDTH / 15)
    BUTTON_FONT = pygame.font.SysFont("monospace", SCREEN_WIDTH / 20)
    HELP_FONT = pygame.font.SysFont("monospace", SCREEN_WIDTH / 40)

    # and now some important vars
    FPS_CLOCK = pygame.time.Clock()
    GRID_DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_status = "Menu"
    num_players = 0
    game_grid = gen_grid()  # initializes 2D array representing the grid
    button_list = create_buttons()  # creates all necessary buttons

    # misc
    pygame.display.set_caption("PyTron!")

    # it's time to loop!
    while True:
        # gotta reset some stuff each time
        GRID_DISPLAY.fill(BLACK)
        reset_buttons()

        # what state are we in?
        if game_status == "Menu":
            display_menu()
        elif game_status == "Help":
            display_help()
        elif game_status == "Playing":
            pass
        elif game_status == "Paused":
            pass

        # the user can do things too, right? let's check those events
        for game_event in pygame.event.get():

            # I don't know why'd they ever quit, but let's give them the option
            if game_event.type == QUIT:
                pygame.quit()
                sys.exit()

            # mouse is clicked, check if it is pressing a button
            elif game_event.type == MOUSEBUTTONDOWN:
                pos_x, pos_y = game_event.pos
                for button in button_list:
                    if button.check_click(pos_x, pos_y):
                        if button.info == "Help":
                            game_status = "Help"
                        elif button.info == "1":
                            num_players = 1
                            game_status = "Playing"
                        elif button.info == "2":
                            num_players = 2
                            game_status = "Playing"
                        elif button.info == "3":
                            num_players = 3
                            game_status = "Playing"
                        elif button.info == "Back":
                            game_status = "Menu"
                        elif button.info == "Continue":
                            game_status = "Playing"
                        elif button.info == "Reset":
                            pass

            elif game_event.type == KEYDOWN and game_status == "Playing":
                if game_event.key == K_UP:
                    # Player1.setDirection('up')
                    pass
                elif game_event.key == K_DOWN:
                    # Player1.setDirection('down')
                    pass
                elif game_event.key == K_LEFT:
                    # Player1.setDirection('left')
                    pass
                elif game_event.key == K_RIGHT:
                    # Player1.setDirection('right')
                    pass
                elif game_event.key == K_SPACE:
                    game_status = "Paused"

        # draw current state of screen
        pygame.display.update()

        # tick tock tick tock
        FPS_CLOCK.tick(GAME_CLOCK)


def gen_grid():
    """creates a 2D array representing the grid"""
    grid = []
    for x in range(0, GRID_WIDTH):
        grid.append([])
        for y in range(0, GRID_HEIGHT):
            grid[x].append(False)
    return grid


def reset_buttons():
    """sets all buttons to be non clickable"""
    for button in button_list:
        button.reset_click()


def display_menu():
    """Functions to display the main menu and activate relevant buttons"""
    draw_menu_text()

    for button in button_list:
        if button.info != "Back" and button.info != "Continue" and button.info != "Reset":
            button.draw_button(GRID_DISPLAY)
            button.set_click()


def draw_menu_text():
    """Draws text present in the main menu, not including the buttons"""
    menu_font = TITLE_FONT.render("PyTron!", 1, WHITE)
    center_text = menu_font.get_rect()
    center_text.centerx = GRID_DISPLAY.get_rect().centerx
    GRID_DISPLAY.blit(menu_font, center_text)

    more_players = TITLE_FONT.render("Number of Players:", 1, WHITE)
    center_text = more_players.get_rect()
    center_text.centerx = GRID_DISPLAY.get_rect().centerx
    center_text.centery = SCREEN_HEIGHT * .25
    GRID_DISPLAY.blit(more_players, center_text)


def display_help():
    """Draws text on the help menu, including controls for all potential players"""

    # All text for player 1
    p1_font = HELP_FONT.render("Player 1 Controls:", 1, WHITE)
    p1_left = HELP_FONT.render("Left: Left Arrow Key", 1, WHITE)
    p1_right = HELP_FONT.render("Right: Right Arrow Key", 1, WHITE)
    p1_up = HELP_FONT.render("Up: Up Arrow Key", 1, WHITE)
    p1_down = HELP_FONT.render("Down: Down Arrow Key", 1, WHITE)

    center_text = p1_font.get_rect()
    center_text.centerx = SCREEN_WIDTH * .15
    center_text.centery = SCREEN_HEIGHT * .1
    GRID_DISPLAY.blit(p1_font, center_text)
    center_text.centery += (SCREEN_HEIGHT * .15)
    GRID_DISPLAY.blit(p1_left, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p1_right, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p1_up, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p1_down, center_text)

    # All text for player 2
    p2_font = HELP_FONT.render("Player 2 Controls:", 1, WHITE)
    p2_left = HELP_FONT.render("Left: A", 1, WHITE)
    p2_right = HELP_FONT.render("Right: D", 1, WHITE)
    p2_up = HELP_FONT.render("Up: W", 1, WHITE)
    p2_down = HELP_FONT.render("Down: S", 1, WHITE)

    center_text = p2_font.get_rect()
    center_text.centerx = SCREEN_WIDTH * .5
    center_text.centery = SCREEN_HEIGHT * .1
    GRID_DISPLAY.blit(p2_font, center_text)
    center_text.centery += (SCREEN_HEIGHT * .15)
    GRID_DISPLAY.blit(p2_left, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p2_right, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p2_up, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p2_down, center_text)

    # draws dividing line between the first and second set of instructions
    pygame.draw.line(GRID_DISPLAY, WHITE, (center_text.left - 15, SCREEN_HEIGHT * .08),
                     (center_text.left - 15, SCREEN_HEIGHT * .6))

    # All text for player 3
    p3_font = HELP_FONT.render("Player 3 Controls:", 1, WHITE)
    p3_left = HELP_FONT.render("Left: J", 1, WHITE)
    p3_right = HELP_FONT.render("Right: L", 1, WHITE)
    p3_up = HELP_FONT.render("Up: I", 1, WHITE)
    p3_down = HELP_FONT.render("Down: K", 1, WHITE)

    center_text = p3_font.get_rect()
    center_text.centerx = SCREEN_WIDTH * .85
    center_text.centery = SCREEN_HEIGHT * .1
    GRID_DISPLAY.blit(p3_font, center_text)
    center_text.centery += (SCREEN_HEIGHT * .15)
    GRID_DISPLAY.blit(p3_left, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p3_right, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p3_up, center_text)
    center_text.centery += (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p3_down, center_text)

    # draws divide line between the 2nd and 3rd set of instructions
    pygame.draw.line(GRID_DISPLAY, WHITE, (center_text.left - 15, SCREEN_HEIGHT * .08),
                     (center_text.left - 15, SCREEN_HEIGHT * .6))

    # makes the back button visible
    for button in button_list:
        if button.info == "Back":
            button.draw_button(GRID_DISPLAY)
            button.set_click()


def create_buttons():
    """creates ALL buttons used in the various menus in game

        various methods activate the click capabilities and visuals of the buttons"""
    all_button = []

    # help button
    temp_font = TITLE_FONT.render("test", 1, WHITE)
    center_text = temp_font.get_rect()
    center_text.centery = SCREEN_HEIGHT * .75
    center_text.width = SCREEN_WIDTH * .5
    center_text.centerx = SCREEN_WIDTH * .5
    help_button = Button(center_text, "Help", GRAY, BUTTON_FONT)
    all_button.append(help_button)

    # 1 player button
    center_text = pygame.Rect.copy(center_text)
    center_text.left = SCREEN_WIDTH * .27
    center_text.width = SCREEN_WIDTH * .12
    center_text.top = SCREEN_HEIGHT * .5
    center_text.height = SCREEN_HEIGHT * .1
    one_button = Button(center_text, "1", GRAY, BUTTON_FONT)
    all_button.append(one_button)

    # 2 player button
    center_text = pygame.Rect.copy(center_text)
    center_text.left = SCREEN_WIDTH * .44
    two_button = Button(center_text, "2", GRAY, BUTTON_FONT)
    all_button.append(two_button)

    # 3 player button
    center_text = pygame.Rect.copy(center_text)
    center_text.left = SCREEN_WIDTH * .6
    three_button = Button(center_text, "3", GRAY, BUTTON_FONT)
    all_button.append(three_button)

    # back button
    center_text = pygame.Rect.copy(center_text)
    center_text.width = SCREEN_WIDTH * .25
    center_text.centerx = GRID_DISPLAY.get_rect().centerx
    center_text.centery = SCREEN_HEIGHT * .8
    back_button = Button(center_text, "Back", GRAY, BUTTON_FONT)
    all_button.append(back_button)

    # continue button
    center_text = pygame.Rect.copy(center_text)
    center_text.centery = SCREEN_HEIGHT * .75
    center_text.centerx = SCREEN_WIDTH * .5
    pause_button = Button(center_text, "Continue", GRAY, BUTTON_FONT)
    all_button.append(pause_button)

    # reset button
    center_text = pygame.Rect.copy(center_text)
    center_text.centery = SCREEN_HEIGHT * .88
    center_text.centerx = SCREEN_WIDTH * .5
    reset_button = Button(center_text, "Reset", GRAY, BUTTON_FONT)
    all_button.append(reset_button)

    return all_button


'''You've reached the end of the file?'''
main()
