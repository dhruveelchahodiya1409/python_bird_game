import random  # For generating random numbers
import sys  # sys.exit for exit the game
import pygame
from Demos.SystemParametersInfo import x
from pygame.locals import *
from scipy.special import y1

# Global Variable for game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPIRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/Forest.png'
PIPE = 'gallery/sprites//pipe.png'


def welcomeScreen():
    playerX = int(SCREENWIDTH / 5)
    playerY = int((SCREENHEIGHT - GAME_SPIRITES['player'].get_height()) / 2)
    messageX = int((SCREENWIDTH - GAME_SPIRITES['message'].get_width()) / 2)
    messageY = int(SCREENHEIGHT * 0.13)
    baseX = 0

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == K_DOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPIRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPIRITES['player'], (playerX, playerY))
                SCREEN.blit(GAME_SPIRITES['message'], (messageX, messageY))
                SCREEN.blit(GAME_SPIRITES['base'], (baseX, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerX = int(SCREENWIDTH/5)
    playerY = int(SCREENHEIGHT/2)
    baseX = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    pipVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY =1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == K_DOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerX,playerY,upperPipes,lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

        # check for score
        playerMidPos = playerX + GAME_SPIRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPIRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score +=1
                print(f"Your Score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped =False
        playerHeight = GAME_SPIRITES['player'].get_height()
        playerY = playerY + min(playerVelY,GROUNDY - playerY - playerHeight)

        # move pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipVelX
            lowerPipe['x'] += pipVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPIRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPIRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPIRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPIRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
        SCREEN.blit(GAME_SPIRITES['player'],(playerX,playerY))
        SCREEN.blit(GAME_SPIRITES['base'],(baseX,GROUNDY))

        myDigit = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigit:
            width += GAME_SPIRITES['numbers'][digit].get_width()
        xOffSet = (SCREENWIDTH - width)/2

        for digit in myDigit:
            SCREEN.blit(GAME_SPIRITES['numbers'][digit],(xOffSet,SCREENHEIGHT*0.12))
            xOffSet += GAME_SPIRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerX,playerY,upperPipes,lowerPipes):
    if playerY > GROUNDY -25 or playerY<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPIRITES['pipe'][0].get_height()
        if (playerY < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < GAME_SPIRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return  True

    for pipe in lowerPipes:
        if (playerY + GAME_SPIRITES['player'].get_height()>pipe['y']) and abs(playerX - pipe['x']) < GAME_SPIRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False

def getRandomPipe():
    pipeHeight = GAME_SPIRITES['pipe'][0].get_height()
    offSet = SCREENHEIGHT/3
    y2 = offSet + random.randrange(0,int(SCREENHEIGHT - GAME_SPIRITES['base'].get_height() - 1.2*offSet))
    pipX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offSet
    pipe = [
        {'x': pipX, 'y': -y1},  # upper Pipe
        {'x': pipX, 'y': y2}  # lower Pipe
    ]
    return pipe

if __name__ == '__main__':

    pygame.init()  # initialize pygame Module 
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")

    # Sprites

    GAME_SPIRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),  # convert_alpha() used for set image in screen
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPIRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()

    GAME_SPIRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()

    GAME_SPIRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),  # Rotate image to 180 digree
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SPIRITES['background'] = pygame.image.load(BACKGROUND).convert()

    GAME_SPIRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()  # show welcome screen until any button press
        mainGame()  # this is the main game

