# necessary imports
from button import *
from cycle import *
from pygame import *
import sys
import os


def main():
    """main function, contains the main game loop"""

    # this game has got to start somewhere, let's initialize some things
    pygame.init()
    game_clock = 30
    screen_width = 1024
    screen_height = 1024
    grid_width = 64
    grid_height = 64
    box_width = screen_width / grid_width
    box_height = screen_height / grid_height

    # and now some important vars
    fps_clock = pygame.time.Clock()
    grid_display = pygame.display.set_mode((screen_width, screen_height))
    game_status = "Menu"
    num_players = 0
    game_grid = gen_grid(grid_width, grid_height)  # initializes 2D array representing the grid
    button_list = create_buttons(grid_display, Color("Gray"), Color("Blue"),
                                 screen_width, screen_height)  # creates all necessary buttons
    cycle_img, cycle_rect = begin_anim("assets", "lightcycle.png", screen_width, screen_height)
    player_list = []  # list of players in the game, will change based on number of human players

    # misc
    pygame.display.set_caption("PyTron!")

    # it's time to loop!
    while True:
        # gotta reset some stuff each time
        grid_display.fill(Color("Black"))
        reset_buttons(button_list)

        # what state are we in?
        if game_status == "Menu":
            display_menu(grid_display, button_list, Color("White"), screen_width, screen_height, cycle_img,
                         cycle_rect)
        elif game_status == "Help":
            display_help(grid_display, button_list, Color("White"), screen_width, screen_height)
        elif game_status == "Playing":
            play_game(grid_display, screen_width, screen_height, box_width, box_height, game_grid, player_list)
        elif game_status == "Paused":
            pause_game(grid_display, button_list, Color("White"), screen_width, screen_height, game_status)
        elif game_status == "Dead":
            pause_game(grid_display, button_list, Color("Red"), screen_width, screen_height, "Game Over")

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
                            player_list = create_player_list(num_players, game_grid)
                            game_status = "Playing"
                        elif button.info == "2":
                            num_players = 2
                            player_list = create_player_list(num_players, game_grid)
                            game_status = "Playing"
                        elif button.info == "3":
                            num_players = 3
                            player_list = create_player_list(num_players, game_grid)
                            game_status = "Playing"
                        elif button.info == "Back":
                            game_status = "Menu"
                        elif button.info == "Menu":
                            game_status = "Menu"
                        elif button.info == "Continue":
                            game_status = "Playing"
                        elif button.info == "Reset":
                            # TODO: Add methods to reset the state of the game
                            game_status = "Playing"

            # these key stroke events will only occur if the game is currently "Playing"
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
                # pause the game with the "space" button
                elif game_event.key == K_SPACE:
                    game_status = "Paused"
                # go back to main menu with the "escape" button
                elif game_event.key == K_ESCAPE:
                    game_status = "Menu"

        # draw current state of screen
        pygame.display.update()

        # tick tock tick tock
        fps_clock.tick(game_clock)


'''grid methods'''


def gen_grid(grid_width, grid_height):
    """creates a 2D array representing the grid
        :param grid_width: the number of squares in the grid's width
        :param grid_height: the number of squares in the grid's height"""
    grid = []
    for x in range(0, grid_width):
        grid.append([])
        for y in range(0, grid_height):
            grid[x].append(False)
    return grid


def draw_grid_lines(grid_display, screen_width, screen_height, box_width, box_height, line_color):
    """draws the lines of the grid during each play tick based on the screen and box dimensions
        :param grid_display: the game display passed in as an arg
        :param screen_width: the width of the screen
        :param screen_height: the height of the screen
        :param box_width: the screen_width divided by the number of boxes to have in the grid
        :param box_height: the screen_height divided by the number of boxes to have in the grid
        :param line_color: the color to make the grid lines"""
    for x in range(0, screen_width, box_width):
        for y in range(0, screen_height, box_height):
            pygame.draw.line(grid_display, line_color, (x, 0), (x, screen_height))
            pygame.draw.line(grid_display, line_color, (0, y), (screen_width, y))


def draw_grid(grid_display, game_grid, box_width, box_height, border_color):
    """draws the updated grid state
        :param grid_display: the game display passed in as an arg
        :param game_grid: the 2D array representing the entire grid and objects within it
        :param box_width: width of each box in the grid
        :param box_height: height of each box in the grid
        :param border_color: color of the wall enclosing the entire grid"""

    for x in range(0, len(game_grid)):
        for y in range(0, len(game_grid[0])):
            if x == 0 or x == len(game_grid) - 1 or y == 0 or y == len(game_grid[0]) - 1:
                pygame.draw.rect(grid_display, border_color, (x * box_width + 1, y * box_height + 1,
                                                              box_width - 1, box_height - 1))
            elif game_grid[x][y]:
                pygame.draw.rect(grid_display, game_grid[x][y], (x * box_width + 1, y * box_height + 1,
                                                                 box_width - 1, box_height - 1))


'''end grid methods'''
'''game actor methods'''


def create_player_list(num_players, game_grid):
    """will create a list of players based on the number of human players selected and return it
        :param num_players: number of human players to include in the list
        :param game_grid: 2D array representing the grid"""
    if num_players == 0:
        print "something broke, 0 players added"
        return []
    elif num_players == 1:
        return [Cycle("Player1", 2, 2, "R", Color("Blue")),
                Cycle("AI", len(game_grid)- 3, len(game_grid[0]) - 3, "L", Color("Red")),
                Cycle("AI", len(game_grid) - 3, 2, "D", Color("Green")),
                Cycle("AI", 2, len(game_grid) - 3, "U", Color("Yellow"))]
    elif num_players == 2:
        return [Cycle("Player1", 2, 2, "R", Color("Blue")),
                Cycle("Player2", len(game_grid) - 3, len(game_grid[0]) - 3, "L", Color("Red")),
                Cycle("AI", len(game_grid) - 3, 2, "D", Color("Green")),
                Cycle("AI", 2, len(game_grid) - 3, "U", Color("Yellow"))]
    elif num_players == 3:
        return [Cycle("Player1", 2, 2, "R", Color("Blue")),
                Cycle("Player2", len(game_grid) - 3, len(game_grid[0]) - 3, "L", Color("Red")),
                Cycle("Player3", len(game_grid) - 3, 2, "D", Color("Green")),
                Cycle("AI", 2, len(game_grid) - 3, "U", Color("Yellow"))]


def draw_cycles(grid_display, box_width, box_height, player_list):
    """draws all the cycles present in the player list
        :param grid_display: game display passed in as an arg
        :param box_width: the width of each box in the grid
        :param box_height: the height of each box in the grid
        :param player_list: list of game actors"""

    for cycle in player_list:
        cycle.draw_cycle(grid_display, box_width, box_height)


def update_cycles(game_grid, player_list):
    """updates all cycles in the player list, handles grid updates on previous locations of cycles
        :param game_grid: grid of all game objects
        :param player_list: list of game actors in the game"""

    for cycle in player_list:
        game_grid = cycle.update_cycle(game_grid)


'''end game actor methods'''
'''play game methods'''


def play_game(grid_display, screen_width, screen_height, box_width, box_height, game_grid, player_list):
    """overall method to handle playing the game in the "Playing" game_state
        this is called from the main game loop, and all other additional methods are added here
        :param grid_display: the game display passed in as an arg
        :param screen_width: the width of the screen
        :param screen_height: the height of the screen
        :param box_width: the screen_width divided by the number of boxes to have in the grid
        :param box_height: the screen_height divided by the number of boxes to have in the grid
        :param game_grid: 2D array representing all objects in the grid
        :param player_list: list of game actors present"""

    # methods acting on the grid
    draw_grid_lines(grid_display, screen_width, screen_height, box_width, box_height, Color("Gray"))
    draw_grid(grid_display, game_grid, box_width, box_height, Color("Gray"))

    # methods acting on the cycles
    draw_cycles(grid_display, box_width, box_height, player_list)
    update_cycles(game_grid, player_list)

    pygame.time.wait(100)


'''end play game methods'''
'''main menu methods'''


def display_menu(grid_display, button_list, text_color, screen_width, screen_height, cycle_img, cycle_rect):
    """Functions to display the main menu and activate relevant buttons
        :param grid_display: the game display passed in as an arg
        :param button_list: list of all buttons present in the game
        :param text_color: color of the text created
        :param screen_width: the width of the screen
        :param screen_height: the height of the screen
        :param cycle_img: cycle image used in menu animation
        :param cycle_rect: rectangle containing the cycle used in menu animation"""

    draw_menu_text(grid_display, text_color, screen_width, screen_height)

    animate_menu(grid_display, cycle_img, cycle_rect, screen_width*.2,
                 screen_width*.8, 2, Color("Blue"))

    for button in button_list:
        if button.info != "Back" and button.info != "Continue" and button.info != "Reset" and \
                button.info != "Menu":
            button.draw_button(grid_display)
            button.set_click()


def draw_menu_text(grid_display, text_color, screen_width, screen_height):
    """Draws text present in the main menu, not including the buttons
        :param grid_display: the game display passed in as an arg
        :param text_color: color of the text created
        :param screen_width: the width of the screen
        :param screen_height: the height of the screen"""

    # create title font
    title_font = pygame.font.SysFont("monospace", screen_width / 15)

    menu_font = title_font.render("PyTron!", 1, text_color)
    center_text = menu_font.get_rect()
    center_text.centerx = grid_display.get_rect().centerx
    grid_display.blit(menu_font, center_text)

    more_players = title_font.render("Number of Players:", 1, text_color)
    center_text = more_players.get_rect()
    center_text.centerx = grid_display.get_rect().centerx
    center_text.centery = screen_height * .25
    grid_display.blit(more_players, center_text)


def begin_anim(folder_name, file_name, screen_width, screen_height):
    """creates the cycle image then converts it to a surface for use later in main menu animation
        :param folder_name: name of the folder to pull the image from
        :param file_name: name of the image file
        :param screen_width: width of the screen
        :param screen_height: height of the screen"""

    # get the image and rect of the lightcycle
    cycle_img, cycle_rect = get_image(folder_name, file_name)
    cycle_rect.top = screen_height * .1
    cycle_rect = cycle_rect.move(screen_width * .7, 0)

    return cycle_img, cycle_rect


def animate_menu(grid_display, cycle_img, cycle_rect, start_x, end_x, step, wall_color):
    """animates the cycle image present on the main menu during every tick
        :param grid_display: the game display passed in as an arg
        :param cycle_img: the image of the cycle used in the animation
        :param cycle_rect: the rectangle containing the image of the cycle in the animation
        :param start_x: leftmost point of the image during animation
        :param end_x: rightmost point of the image during animation
        :param step: pixels to move on each call
        :param wall_color: color of the wall to draw behind the cycle"""

    if cycle_rect.right >= end_x:
        cycle_rect.left = start_x
    else:
        cycle_rect.move_ip(step, 0)

    pygame.draw.rect(grid_display, wall_color, (start_x, cycle_rect.top + 5, cycle_rect.left - start_x + 40,
                                                cycle_rect.height - 10))
    grid_display.blit(cycle_img, cycle_rect)


def get_image(folder_name, file_name):
    """retrieves an image from a folder, implementing an exception in case it does not exist
        :returns final_image: a surface of the image that is attempting to be loaded
        :returns final_image.get_rect(): the rectangle surrounding this image
        :param file_name: the name of the image in the given folder
        :param folder_name: the name of the folder to look in"""
    file_path = os.path.join(folder_name, file_name)
    try:
        final_image = pygame.image.load(file_path)
    except pygame.error, message:
        print 'Cannot find image: ', folder_name, "/", file_name
        raise message
    final_image = final_image.convert()

    return final_image, final_image.get_rect()


'''end main menu methods'''
'''help menu methods'''


def display_help(grid_display, button_list, text_color, screen_width, screen_height):
    """Draws text on the help menu, including controls for all potential players
        :param grid_display: the game display passed in as an arg
        :param button_list: list of all buttons present in the game
        :param text_color: color of the text to be created
        :param screen_width: the width of the screen
        :param screen_height: the height of the screen"""

    # All text for player 1
    player_1_controls = ["Left Arrow Key", "Right Arrow Key", "Up Arrow Key",
                         "Down Arrow Key"]
    create_help_text("Player 1", player_1_controls, screen_width * .15,
                     screen_height * .1, grid_display, text_color, screen_width, screen_height)

    # All text for player 2
    player_2_controls = ["A", "D", "W", "S"]
    create_help_text("Player 2", player_2_controls, screen_width * .5,
                     screen_height * .1, grid_display, text_color, screen_width, screen_height)

    # draws dividing line between the first and second set of instructions
    pygame.draw.line(grid_display, text_color, (screen_width * .35, screen_height * .08),
                     (screen_width * .35, screen_height * .6))

    # All text for player 3
    player_3_controls = ["J", "L", "I", "K"]
    create_help_text("Player 3", player_3_controls, screen_width * .85,
                     screen_height * .1, grid_display, text_color, screen_width, screen_height)

    # draws divide line between the 2nd and 3rd set of instructions
    pygame.draw.line(grid_display, text_color, (screen_width * .66, screen_height * .08),
                     (screen_width * .66, screen_height * .6))

    # makes the back button visible
    for button in button_list:
        if button.info == "Back":
            button.draw_button(grid_display)
            button.set_click()


def create_help_text(player_name, control_list, start_x, start_y, grid_display, text_color,
                     screen_width, screen_height):
    """consolidated help texts to reuse one method, requires following parameters:
        :param player_name: string, the name to put before "controls"
        :param control_list: list of strings, list of 4 buttons, representing left, right, up, down
        :param start_x: int, the start x value of the CENTER of the rectangle
        :param start_y: int, the start y value of the CENTER of the rectangle
        :param grid_display: the game display passed in as an arg
        :param text_color: color of the text to be created
        :param screen_width: the width of the screen
        :param screen_height: the height of the screen"""

    # argument checks
    if not isinstance(player_name, basestring):
        print ("Player name arg is not a string")
        return
    elif len(control_list) is not 4:
        print ("List of controls is not the correct length")
        return
    elif type(start_x) is not float:
        print("X coordinate is not a number")
        return
    elif type(start_y) is not float:
        print("Y coordinate is not a number")
        return

    # create font for use in help text
    help_font = pygame.font.SysFont("monospace", screen_width / 40)

    # Fonts rendered initially
    text_font = help_font.render(player_name + " Controls:", 1, text_color)
    text_left = help_font.render("Left: " + control_list[0], 1, text_color)
    text_right = help_font.render("Right: " + control_list[1], 1, text_color)
    text_up = help_font.render("Up: " + control_list[2], 1, text_color)
    text_down = help_font.render("Down: " + control_list[3], 1, text_color)

    center_text = text_font.get_rect()
    center_text.centerx = start_x
    center_text.centery = start_y
    grid_display.blit(text_font, center_text)
    center_text.centery += (screen_height * .15)
    grid_display.blit(text_left, center_text)
    center_text.centery += (screen_height * .1)
    grid_display.blit(text_right, center_text)
    center_text.centery += (screen_height * .1)
    grid_display.blit(text_up, center_text)
    center_text.centery += (screen_height * .1)
    grid_display.blit(text_down, center_text)


'''end help menu methods'''
'''pause menu methods'''


def pause_game(grid_display, button_list, text_color, screen_width, screen_height, text):
    """creates the pause menu and all text, as well as activating the continue and reset button
        :param grid_display: the game display passed in as an arg
        :param button_list: list of all buttons present in the game
        :param text_color: color of the text to be created
        :param screen_width: the width of the screen
        :param screen_height: the height of the screen
        :param text: text to display at the top, either 'Game Over' or 'Paused'
            this will also affect button display"""

    # create a font for use in the menu
    pause_font = pygame.font.SysFont("monospace", 50)

    # display text
    pause_text = pause_font.render(text, 1, text_color)
    center_text = pause_text.get_rect()
    center_text.centerx = screen_width * .5
    center_text.centery = screen_height * .25
    grid_display.blit(pause_text, center_text)

    # will not draw continue button if the game has already ended
    for button in button_list:
        if (button.info == "Continue" and text != "Game Over") or button.info == "Reset" \
                or button.info == "Menu":
            button.draw_button(grid_display)
            button.set_click()


'''end pause menu methods'''
'''buttons buttons buttons'''


def create_buttons(grid_display, text_color, outline_color, screen_width, screen_height):
    """creates ALL buttons used in the various menus in game
        various methods activate the click capabilities and visuals of the buttons
        :param grid_display: the game display passed in as an arg
        :param text_color: color of the text inside the buttons
        :param outline_color: color of the rectangle surrounding the buttons
        :param screen_width: the width of the screen
        :param screen_height: the height of the screen"""

    all_button = []

    # create font used inside the buttons
    button_font = pygame.font.SysFont("monospace", screen_width / 20)

    # help button
    temp_font = button_font.render("test", 1, text_color)
    center_text = temp_font.get_rect()
    center_text.centery = screen_height * .75
    center_text.width = screen_width * .5
    center_text.centerx = screen_width * .5
    help_button = Button(center_text.copy(), "Help", text_color, outline_color, button_font)
    all_button.append(help_button)

    # 1 player button
    center_text.left = screen_width * .27
    center_text.width = screen_width * .12
    center_text.top = screen_height * .5
    center_text.height = screen_height * .1
    one_button = Button(center_text.copy(), "1", text_color, outline_color, button_font)
    all_button.append(one_button)

    # 2 player button
    center_text.left = screen_width * .44
    two_button = Button(center_text.copy(), "2", text_color, outline_color, button_font)
    all_button.append(two_button)

    # 3 player button
    center_text.left = screen_width * .6
    three_button = Button(center_text.copy(), "3", text_color, outline_color, button_font)
    all_button.append(three_button)

    # back button
    center_text.width = screen_width * .25
    center_text.centerx = grid_display.get_rect().centerx
    center_text.centery = screen_height * .8
    back_button = Button(center_text.copy(), "Back", text_color, outline_color, button_font)
    all_button.append(back_button)

    # continue button
    center_text.centery = screen_height * .62
    center_text.centerx = screen_width * .5
    pause_button = Button(center_text.copy(), "Continue", text_color, outline_color, button_font)
    all_button.append(pause_button)

    # reset button
    center_text.centery = screen_height * .75
    center_text.centerx = screen_width * .5
    reset_button = Button(center_text.copy(), "Reset", text_color, outline_color, button_font)
    all_button.append(reset_button)

    # return to menu button
    center_text.centery = screen_height * .88
    center_text.centerx = screen_width * .5
    back_to_menu_button = Button(center_text.copy(), "Menu", text_color, outline_color, button_font)
    all_button.append(back_to_menu_button)

    return all_button


def reset_buttons(button_list):
    """sets all buttons to be non clickable
        :param button_list: list of all buttons present in the game"""
    for button in button_list:
        button.reset_click()


'''end buttons buttons buttons'''
'''You've reached the end of the file?'''
main()
