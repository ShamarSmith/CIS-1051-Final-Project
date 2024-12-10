import random, pygame, sys
from pygame.locals import*

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWWIDTH / CELLSIZE)

#         R   G   B
WHITE    =  (255,255,255)
BLACK    =  (0,   0,   0)
RED      =  (255, 0,   0)
GREEN    =  (0, 255,   0)
DARKGREEN = (0, 155,   0)
DARKGRAY =  (40, 40,  40)
ORANGE =    (255,140,  0)

BGCOLOR = GREEN

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def main() :
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('Georgia.ttf',18)
    pygame.display.set_caption('Centi')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()
def runGame():
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    centipedeCoords = [{'x': startx,    'y': starty},
                       {'x': startx - 1,'y': starty},
                       {'x': startx - 2,'y': starty}]
    direction = RIGHT
    apple = getRandomLocation()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction  != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        if centipedeCoords[HEAD]['x'] == -1 or centipedeCoords[HEAD]['x'] == CELLWIDTH or centipedeCoords[HEAD]['y'] == -1 or centipedeCoords[HEAD]['y'] == CELLHEIGHT:
            return
        for centipedeBody in centipedeCoords[1:]:
            if centipedeBody['x'] == centipedeCoords[HEAD]['x'] and centipedeBody['y'] == centipedeCoords[HEAD]['y']:
                return

        if centipedeCoords[HEAD]['x'] == apple['x'] and centipedeCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()
        else:
            del centipedeCoords[-1]
        if direction == UP:
            newHead = {'x': centipedeCoords[HEAD]['x'], 'y': centipedeCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': centipedeCoords[HEAD]['x'], 'y': centipedeCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': centipedeCoords[HEAD]['x'] - 1, 'y': centipedeCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': centipedeCoords[HEAD]['x'] + 1, 'y': centipedeCoords[HEAD]['y']}
        centipedeCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawCentipede(centipedeCoords)
        drawApple(apple)
        drawScore(len(centipedeCoords)- 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
        
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    titleFont = pygame.font.Font('Georgia.ttf', 100)
    titleSurf1 = titleFont.render('Centi!', True, ORANGE, BLACK)
    titleSurf2 = titleFont.render('Centi!', True, RED)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3
        degrees2 += 7

def terminate():
    pygame.quit()
    sys.exit()
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def showGameOverScreen():
    gameOverFont = pygame.font.Font('Georgia.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawCentipede(centipedeCoords):
    for coord in centipedeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        centipedeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, centipedeSegmentRect)
        centipedeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, ORANGE, centipedeInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, BLACK, appleRect)
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

if __name__ =='__main__':
    main()
    
# Credit goes to https://inventwithpython.com/pygame/chapter6.html 