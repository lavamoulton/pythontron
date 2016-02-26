import sys, pygame
from pygame.locals import *

#local imports
import button
from button import *

#initial vars
GAME_CLOCK = 30
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
GRID_WIDTH = 128
GRID_HEIGHT = 128
BOX_WIDTH = SCREEN_WIDTH / GRID_WIDTH
BOX_HEIGHT = SCREEN_HEIGHT / GRID_HEIGHT

#colors, colors everywhere
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def main():
    #this game has got to start somewhere, let's initialize some things
    pygame.init()
    global FPS_CLOCK
    global GRID_DISPLAY
    global TITLE_FONT
    global BUTTON_FONT
    global HELP_FONT
    global buttonList

    #create some fonts for later
    TITLE_FONT = pygame.font.SysFont("monospace", SCREEN_WIDTH / 15)
    BUTTON_FONT = pygame.font.SysFont("monospace", SCREEN_WIDTH / 20)
    HELP_FONT = pygame.font.SysFont("monospace", SCREEN_WIDTH / 40)

    #and now some important vars
    FPS_CLOCK = pygame.time.Clock()
    GRID_DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    gameStatus = "Menu"
    numPlayers = 0
    gameGrid = genGrid() #initializes 2D array representing the grid
    buttonList = createButtons() #creates all necessary buttons

    #misc
    pygame.display.set_caption("PyTron!")

    #it's time to loop!
    while True:
        #gotta reset some stuff each time
        GRID_DISPLAY.fill(BLACK)
        resetButtons()

        #what state are we in?
        if gameStatus == "Menu":
            displayMenu()
        elif gameStatus == "Help":
            displayHelp()
        elif gameStatus == "Playing":
            pass
        elif gameStatus == "Paused":
            pass

        #the user can do things too, right? let's check those events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                posX, posY = event.pos
                for button in buttonList:
                    if button.checkClick(posX, posY):
                        if button.info == "Help":
                            gameStatus = "Help"
                        elif button.info == "1":
                            numPlayers = 1
                            gameStatus = "Playing"
                        elif button.info == "2":
                            numPlayers = 2
                            gameStatus = "Playing"
                        elif button.info == "3":
                            numPlayers = 3
                            gameStatus = "Playing"
                        elif button.info == "Back":
                            gameStatus = "Menu"
                        elif button.info == "Continue":
                            gameStatus = "Playing"
                        elif button.info == "Reset":
                            pass

            elif event.type == KEYDOWN and gameStatus == "Playing":
                if event.key == K_UP:
                    #Player1.setDirection('up')
                    pass
                elif event.key == K_DOWN:
                    #Player1.setDirection('down')
                    pass
                elif event.key == K_LEFT:
                    #Player1.setDirection('left')
                    pass
                elif event.key == K_RIGHT:
                    #Player1.setDirection('right')
                    pass
                elif event.key == K_SPACE:
                    gameStatus = "Paused"

        pygame.display.update()
        FPS_CLOCK.tick(GAME_CLOCK)

#creates a 2D array representing the grid
def genGrid():
    grid = []
    for x in range(0, GRID_WIDTH):
        grid.append([])
        for y in range(0, GRID_HEIGHT):
            grid[x].append(False)
    return grid

#sets all buttons to be non clickable
def resetButtons():
    for button in buttonList:
        button.resetClick()

#Functions to display the main menu and activate relevant buttons
def displayMenu():
    drawMenuText()

    for button in buttonList:
        if button.info != "Back" and button.info != "Continue" and button.info != "Reset":
            button.drawButton(GRID_DISPLAY)
            button.setClick()

#Draws text present in the main menu, not including the buttons
def drawMenuText():
    menuFont = TITLE_FONT.render("PyTron!", 1, WHITE)
    centerText = menuFont.get_rect()
    centerText.centerx = GRID_DISPLAY.get_rect().centerx
    GRID_DISPLAY.blit(menuFont, centerText)

    morePlayers = TITLE_FONT.render("Number of Players:", 1, WHITE)
    centerText = morePlayers.get_rect()
    centerText.centerx = GRID_DISPLAY.get_rect().centerx
    centerText.centery = SCREEN_HEIGHT * .25
    GRID_DISPLAY.blit(morePlayers, centerText)

#Draws text on the help menu, including controls for all potential players
def displayHelp():

    #All text for player 1
    p1Font = HELP_FONT.render("Player 1 Controls:", 1, WHITE)
    p1Left = HELP_FONT.render("Left: Left Arrow Key", 1, WHITE)
    p1Right = HELP_FONT.render("Right: Right Arrow Key", 1, WHITE)
    p1Up = HELP_FONT.render("Up: Up Arrow Key", 1, WHITE)
    p1Down = HELP_FONT.render("Down: Down Arrow Key", 1, WHITE)

    centerText = p1Font.get_rect()
    centerText.centerx = SCREEN_WIDTH * .15
    centerText.centery = SCREEN_HEIGHT * .1
    GRID_DISPLAY.blit(p1Font, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery+(SCREEN_HEIGHT*.15)
    GRID_DISPLAY.blit(p1Left, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery+(SCREEN_HEIGHT*.1)
    GRID_DISPLAY.blit(p1Right, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery+(SCREEN_HEIGHT*.1)
    GRID_DISPLAY.blit(p1Up, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery+(SCREEN_HEIGHT*.1)
    GRID_DISPLAY.blit(p1Down, centerText)

    #All text for player 2
    p2Font = HELP_FONT.render("Player 2 Controls:", 1, WHITE)
    p2Left = HELP_FONT.render("Left: A", 1, WHITE)
    p2Right = HELP_FONT.render("Right: D", 1, WHITE)
    p2Up = HELP_FONT.render("Up: W", 1, WHITE)
    p2Down = HELP_FONT.render("Down: S", 1, WHITE)

    centerText = pygame.Rect.copy(centerText)
    centerText = p2Font.get_rect()
    centerText.centerx = SCREEN_WIDTH * .5
    centerText.centery = SCREEN_HEIGHT * .1
    GRID_DISPLAY.blit(p2Font, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery + (SCREEN_HEIGHT * .15)
    GRID_DISPLAY.blit(p2Left, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery + (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p2Right, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery + (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p2Up, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery + (SCREEN_HEIGHT * .1)
    GRID_DISPLAY.blit(p2Down, centerText)

    #draws dividing line between the first and second set of instructions
    pygame.draw.line(GRID_DISPLAY, WHITE, (centerText.left-15, SCREEN_HEIGHT * .08),
                     (centerText.left-15, SCREEN_HEIGHT*.6))

    #All text for player 3
    p3Font = HELP_FONT.render("Player 3 Controls:", 1, WHITE)
    p3Left = HELP_FONT.render("Left: J", 1, WHITE)
    p3Right = HELP_FONT.render("Right: L", 1, WHITE)
    p3Up = HELP_FONT.render("Up: I", 1, WHITE)
    p3Down = HELP_FONT.render("Down: K", 1, WHITE)

    centerText = pygame.Rect.copy(centerText)
    centerText = p3Font.get_rect()
    centerText.centerx = SCREEN_WIDTH * .85
    centerText.centery = SCREEN_HEIGHT * .1
    GRID_DISPLAY.blit(p3Font, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery + (SCREEN_HEIGHT*.15)
    GRID_DISPLAY.blit(p3Left, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery + (SCREEN_HEIGHT*.1)
    GRID_DISPLAY.blit(p3Right, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery + (SCREEN_HEIGHT*.1)
    GRID_DISPLAY.blit(p3Up, centerText)
    centerText = pygame.Rect.copy(centerText)
    centerText.centery = centerText.centery + (SCREEN_HEIGHT*.1)
    GRID_DISPLAY.blit(p3Down, centerText)

    #draws divide line between the 2nd and 3rd set of instructions
    pygame.draw.line(GRID_DISPLAY, WHITE, (centerText.left-15, SCREEN_HEIGHT*.08),
                     (centerText.left-15, SCREEN_HEIGHT*.6))

    #makes the back button visible
    for button in buttonList:
        if button.info == "Back":
            button.drawButton(GRID_DISPLAY)
            button.setClick()

def createButtons():
    buttonList = []

    tempFont = TITLE_FONT.render("test", 1, WHITE)
    centerText = tempFont.get_rect()
    centerText.centery = SCREEN_HEIGHT * .75
    centerText.width = SCREEN_WIDTH * .5
    centerText.centerx = SCREEN_WIDTH * .5
    helpButton = Button(centerText, "Help", GRAY, BUTTON_FONT)
    buttonList.append(helpButton)

    centerText = pygame.Rect.copy(centerText)
    centerText.left = SCREEN_WIDTH * .27
    centerText.width = SCREEN_WIDTH * .12
    centerText.top = SCREEN_HEIGHT * .5
    centerText.height = SCREEN_HEIGHT * .1
    oneButton = Button(centerText, "1", GRAY, BUTTON_FONT)
    buttonList.append(oneButton)

    centerText = pygame.Rect.copy(centerText)
    centerText.left = SCREEN_WIDTH * .44
    twoButton = Button(centerText, "2", GRAY, BUTTON_FONT)
    buttonList.append(twoButton)

    centerText = pygame.Rect.copy(centerText)
    centerText.left = SCREEN_WIDTH * .6
    threeButton = Button(centerText, "3", GRAY, BUTTON_FONT)
    buttonList.append(threeButton)

    centerText = pygame.Rect.copy(centerText)
    centerText.width = SCREEN_WIDTH * .25
    centerText.centerx = GRID_DISPLAY.get_rect().centerx
    centerText.centery = SCREEN_HEIGHT * .8
    backButton = Button(centerText, "Back", GRAY, BUTTON_FONT)
    buttonList.append(backButton)

    centerText = pygame.Rect.copy(centerText)
    centerText.centery = SCREEN_HEIGHT*.75
    centerText.centerx = SCREEN_WIDTH*.5
    pauseButton = Button(centerText, "Continue", GRAY, BUTTON_FONT)
    buttonList.append(pauseButton)

    centerText = pygame.Rect.copy(centerText)
    centerText.centery = SCREEN_HEIGHT*.88
    centerText.centerx = SCREEN_WIDTH*.5
    resetButton = Button(centerText, "Reset", GRAY, BUTTON_FONT)
    buttonList.append(resetButton)
    return buttonList

main()