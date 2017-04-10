from flask import Flask
from flask_ask import Ask, statement, question
from win32api import keybd_event
import random, math, pygame, _thread, time
from pygame.locals import *

### Virtual keyboard codes. win32api has to be installed, and the library needs to be imported.
### Key codes available: https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx
base = {
    'n': 78,
    'p': 80,
    'q': 81,
    'r': 82,
    's': 83,
    'DOWN': 40,
    'LEFT': 37,
    'UP': 38,
    'RIGHT': 39,
 }

## Released Key
def key_up(key):
    keybd_event(key, 0, 2, 0)
## Pressed Key
def key_down(key):
    keybd_event(key, 0, 1, 0)
## Imitate pressing key
def press(key, speed=1):
    rest_time = 0.05/speed
    if key in base:
        key = base[key]
        key_down(key)
        time.sleep(rest_time)
        key_up(key)
        return True
    return False

## end virtual keyboard

## global variable that is equal to a local "score" variable
voice_score = 0
## Begining of the Snake Game Engine
def main():
    showstartscreen = 1
    while 1:
        ######## CONSTANTS
        WINSIZE = [1000,700]
        WHITE = [255,255,255]
        BLACK = [0,0,0]
        RED = [255,0,0]
        GREEN = [0,255,0]
        BLUE = [0,0,255]
        BLOCKSIZE = [20,20]
        MAXX = 960
        MINX = 20
        MAXY = 660
        MINY = 80
        SNAKESTEP = 20
        TRUE = 1
        FALSE = 0
        UP = 1
        DOWN = 3
        RIGHT = 2
        LEFT = 4

        ## VARIABLES
        direction = RIGHT # 1=up,2=right,3=down,4=left
        snakexy = [300,400]
        snakelist = [[300,400],[280,400],[260,400]]
        counter = 0
        score = 0
        appleonscreen = 0 #applexy = [0,0]
        newdirection = RIGHT
        snakedead = FALSE
        gameregulator = 6
        gamepaused = 0
        growsnake = 0  # added to grow tail by two each time
        snakegrowunit = 2 # added to grow tail by two each time
        voice_score = score

        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption('SNAKER')
        screen.fill(BLACK)

        #### show initial start screen
        if showstartscreen == TRUE:
            showstartscreen = FALSE
            ## S letter that is shown on the start screen
            s = [[180,120],[180,100],[160,100],[140,100],[120,100],[100,100],[100,120],[100,140],[100,160],[120,160],[140,160],[160,160],[180,160],[180,180],[180,200],[180,220],[160,220],[140,220],[120,220],[100,220],[100,200]]
            apple = [100,200]

            pygame.draw.rect(screen,GREEN,Rect(apple,BLOCKSIZE))
            pygame.display.flip()
            clock.tick(8)

            for e in s:
                pygame.draw.rect(screen,BLUE,Rect(e,BLOCKSIZE))
                pygame.display.flip()
                clock.tick(8)

            font = pygame.font.SysFont("arial", 64)
            text_surface = font.render("NAKER", True, BLUE)
            screen.blit(text_surface, (220,180))
            font = pygame.font.SysFont("arial", 24)
            text_surface = font.render("Move the snake with voce commands UP, DOWN, LEFT, RIGHT to eat the apples", True, BLUE)
            screen.blit(text_surface, (50,300))
            text_surface = font.render("Avoid yourself!", True, BLUE)
            screen.blit(text_surface, (50,350))
            text_surface = font.render("Say PLAY SNAKE to start and QUIT SNAKE to quit the game", True, BLUE)
            screen.blit(text_surface, (50,400))
            text_surface = font.render("Say PAUSE THE GAME to pause, or START AGAIN to resume at any time", True, BLUE)
            screen.blit(text_surface, (50,450))

            pygame.display.flip()
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]: exit()
                if pressed_keys[K_s]: break

                clock.tick(10)

        ## if snake is not dead, proceed with the following functions
        while not snakedead:
            ###### get input events  ####
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_LEFT]: newdirection = LEFT
            if pressed_keys[K_RIGHT]: newdirection = RIGHT
            if pressed_keys[K_UP]: newdirection = UP
            if pressed_keys[K_DOWN]: newdirection = DOWN
            if pressed_keys[K_q]: snakedead = TRUE
            if pressed_keys[K_p]: gamepaused = 1

            ### wait here if p key is pressed until p key is pressed again
            while gamepaused == 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_r]:
                        gamepaused = 0
                clock.tick(10)

            """ Gameregulator: setting a very low clock ticks
            caused the keyboard input to be hit or miss.  Therefore,
            gameticks, the input, and screen refresh are at the rate of gameticks,
            but the snake moving and all other logic is at the slower
            "regulated" speed"""


            if gameregulator == 6:

                ## Stop snake from going in reverse direction
                if newdirection == LEFT and not direction == RIGHT:
                    direction = newdirection

                elif newdirection == RIGHT and not direction == LEFT:
                    direction = newdirection

                elif newdirection == UP and not direction == DOWN:
                    direction = newdirection

                elif newdirection == DOWN and not direction == UP:
                    direction = newdirection

                ## Snake's navigation based on input (LEFT, RIGHT, UP, DOWN)
                if direction == RIGHT:
                    snakexy[0] = snakexy[0] + SNAKESTEP
                    if snakexy[0] > MAXX:
                        snakexy[0] = snakexy[0] - snakexy[0]

                elif direction == LEFT:
                    snakexy[0] = snakexy[0] - SNAKESTEP
                    if snakexy[0] < MINX:
                        snakexy[0] = snakexy[0] + 1000

                elif direction == UP:
                    snakexy[1] = snakexy[1] - SNAKESTEP
                    if snakexy[1] < MINY:
                        snakexy[1] = snakexy[1] + 700

                elif direction == DOWN:
                    snakexy[1] = snakexy[1] + SNAKESTEP
                    if snakexy[1] > MAXY:
                        snakexy[1] = snakexy[1] - snakexy[1]

                ## Snake dies if it hits itself
                if len(snakelist) > 3 and snakelist.count(snakexy) > 0:
                    snakedead = TRUE



                ##Generating apple at a random position if there is no apple at the screen
                ##Apple's position has to be different than the snake's position
                if appleonscreen == 0:
                    good = FALSE
                    while good == FALSE:
                        x = random.randrange(1,39)
                        y = random.randrange(5,29)
                        applexy = [int(x*SNAKESTEP),int(y*SNAKESTEP)]
                        if snakelist.count(applexy) == 0:
                            good = TRUE
                    appleonscreen = 1

                ## Add new position of snake head
                #### If snake eats the apple, the tail doesn't move forward while the rest ofbody moves. (grow snake)
                #### If anake doesn't eat the apple, then the tail moves forward along with the body.( snake same size )

                snakelist.insert(0,list(snakexy))
                if snakexy[0] == applexy[0] and snakexy[1] == applexy[1]:
                    appleonscreen = 0
                    score = score + 1
                    growsnake = growsnake + 1
                elif growsnake > 0:
                    growsnake = growsnake + 1
                    if growsnake == snakegrowunit:
                        growsnake = 0
                else:
                    snakelist.pop()
                gameregulator = 0

            ## RENDER THE SCREEN ##
            ## Clear the screen
            screen.fill(BLACK)

            ##Draw the screen borders
            ## horizontals
            pygame.draw.line(screen,BLUE,(0,9),(999,9),20)
            pygame.draw.line(screen,BLUE,(0,690),(999,690),20)
            pygame.draw.line(screen,BLUE,(0,69),(999,69),20)
            ## verticals
            pygame.draw.line(screen,BLUE,(9,0),(9,799),20)
            pygame.draw.line(screen,BLUE,(989,0),(989,799),20)
            ##Print the score
            font = pygame.font.SysFont("arial", 38)
            text_surface = font.render("SNAKE!          Score: " + str(score), True, BLUE)
            screen.blit(text_surface, (50,18))

            ## Output the array elements to the screen as rectangles ( the snake)
            for element in snakelist:
                pygame.draw.rect(screen,RED,Rect(element,BLOCKSIZE))
            ## Draw the apple
            pygame.draw.rect(screen,GREEN,Rect(applexy,BLOCKSIZE))
            ## Flip the screen to display everything we just changed
            pygame.display.flip()

            gameregulator = gameregulator + 1
            clock.tick(25)
        ## If the snake is dead then the game is over

        if snakedead == TRUE:
            screen.fill(BLACK)
            font = pygame.font.SysFont("arial", 48)
            text_surface = font.render("GAME OVER", True, BLUE)
            screen.blit(text_surface, (350,200))
            text_surface = font.render("Your Score: " + str (score), True, BLUE)
            screen.blit(text_surface, (350,300))
            font = pygame.font.SysFont("arial", 24)
            text_surface = font.render("Say GUIT to quit", True, BLUE)
            screen.blit(text_surface, (400,400))
            text_surface = font.render("Say PLAY THE GAME AGAIN, to play again", True, BLUE)
            screen.blit(text_surface, (375,450))

            pygame.display.flip()
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]: exit()
                if pressed_keys[K_n]: break

                clock.tick(10)
## END of the SNAKE GAME ENGINE

## ALEXA interaction
app = Flask(__name__)
ask = Ask(app,'/')

@ask.launch
def start_skill():
    return question("Welcome to Snake Game. Use voice commands to navigate the snake. Say open to open the game.")

@ask.intent("OpenIntent")
def start_game():
    _thread.start_new_thread(main,())
    return question("Say play snake whenever you are ready. To pause say pause. To quit say quit snake.")

@ask.intent("StartIntent")
def begin_game():
    press("s", 1)
    return question("Here we go!")

@ask.intent("RightIntent")
def turn_right():
    press("RIGHT", 1)
    return question("Right")

@ask.intent("LeftIntent")
def turn_left():
    press("LEFT", 1)
    return question("Left")

@ask.intent("UpIntent")
def turn_up():
    press("UP", 1)
    return question("Up")

@ask.intent("DownIntent")
def turn_down():
    press("DOWN", 1)
    return question("Down")

@ask.intent("PauseIntent")
def turn_down():
    press("p", 1)
    return question("Say go back to resume")

@ask.intent("ReturnIntent")
def turn_down():
    press("r", 1)
    return question("Welcome again.")

@ask.intent("StopIntent")
def turn_down():
    press("q", 1)
    return question("Thank you for playing with me. Your score is %s" % voice_score)

@ask.intent("PlayAgainIntent")
def turn_down():
    press("n", 1)
    return question("Let us start again")

if __name__ == '__main__':
    app.run(debug=True)
