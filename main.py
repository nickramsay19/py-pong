import pygame
import random
import math
from player import Player
from game import Game

# Declare Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# Setup
pygame.init()
screen = pygame.display.set_mode((750, 500)) # set width & height
pygame.display.set_caption('Pong - Nick Ramsay')

# setup game
game = Game()

# define positions for players and puck
A = Player()
B = Player()

px = 100
py = 0
pxv = float(0)
pyv = float(0)

# setup players
def drawPlayers():
    pygame.draw.rect(screen, WHITE, (0, A.Y, 10, 75))
    pygame.draw.rect(screen, WHITE, (740, B.Y, 10, 75))
    
def drawPuck(x, y):
    pygame.draw.circle(screen, WHITE, (x,y), 10, 1)

def drawScores(screen):
    font = pygame.font.Font('freesansbold.ttf', 45)

    textA = font.render(str(A.Points), True, WHITE) 
    textRectA = textA.get_rect() 
    textRectA.center = (250, 425) 
    screen.blit(textA, textRectA) 

    textB = font.render(str(B.Points), True, WHITE) 
    textRectB = textA.get_rect() 
    textRectB.center = (500, 425) 
    screen.blit(textB, textRectB) 

# Game loop
while game.Running:
    # Check if game should quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.Running = False

    # clear the screen
    screen.fill(BLACK)

    '''
        --- Player Controls, Movement & Hit-reg ---
    '''
    # Controls
    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_w] or keys[pygame.K_s]:
        if keys[pygame.K_w] and A.V > -9: A.V -= 1
        if keys[pygame.K_s] and A.V < 9: A.V += 1
    elif A.V != 0:
        if abs(A.V) < 1:
            A.V = 0
        else:
            A.V -= .6 * A.V / abs(A.V) 
    if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        if keys[pygame.K_UP] and B.V > -9: B.V -= 1
        if keys[pygame.K_DOWN] and B.V < 9: B.V += 1
    elif B.V != 0:
        if abs(B.V) < 1:
            B.V = 0
        else:
            B.V -= .6 * B.V / abs(B.V)

    # Movement & Hit-reg
    if A.Y < 0: 
        A.Y = 0
        A.V = A.V * -0.3
    elif A.Y > 425:
        A.Y = 425
        A.V = A.V * -0.3
    else:
        A.Y += A.V 
    
    if B.Y < 0: 
        B.Y = 0
        B.V = B.V * -0.3
    elif B.Y > 425:
        B.Y = 425
        B.V = B.V * -0.3
    else:
        B.Y += B.V 
    
    '''
        --- Handle Puck Movement & Hit-reg ---
    '''
    # Serve the Puck
    if game.Serving:
        px = 375
        py = 250

        # Randomly choose A or B to start
        if random.randint(0, 3) == 3:
            pxv = 4
        else:
            pxv = -4
        
        game.Serving = False

    # Check for Hit-reg
    else:
        # Hit-reg: Ceiling * Floor
        if py < 1 and pyv < 0:
            py = 1
            pyv = pyv * -1
        elif py > 499 and pyv > 0:
            py = 499
            pyv = pyv * -1

        # Hit-reg: Left/Right Walls
        if px - 5 <= 10 and (py + 5 < A.Y or py + 5 > A.Y + 75):
            B.Points += 1
            game.Serving = True 
        elif px + 5 >= 740 and (py + 5 < B.Y or py + 5 > B.Y + 75):
            A.Points += 1
            game.Serving = True 
        
        # Hit-reg: Player (A)
        if px - 5 <= 10 and py + 5 >= A.Y and py - 5 <= A.Y + 75:
            pxv = abs(pxv * 1.05)
            pyv = 0.09 * (py - A.Y - 37.5)

        # Hit-reg: Player (B)
        elif px + 5 >= 740 and py + 5 >= B.Y and py - 5 <= B.Y + 75:
            pxv = abs(pxv * 1.05) * -1 # send to right
            pyv = 0.09 * (py - B.Y - 37.5)


    # Apply Puck Movement
    px += int(pxv)
    py += int(pyv) 

    
    # draw players
    drawPlayers()
    drawPuck(px,py)
    drawScores(screen)

    # Update Screen
    pygame.display.update()

'''
        Todo:
        * add puck physics
        * add scoreboard
        * add puck speed limit
'''