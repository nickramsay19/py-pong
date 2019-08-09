# Pong - Made with Python3 & Pygame
> Created by Nicholas Ramsay

## Features
* Velocity based movement for players and the ball/puck
* Realistic bounce/hit-reg physics

## To do
* Move puck variables(px,py,pxv,etc) into a Puck class
* Move player movements and hit-reg into class methods of Player

## player.py
```python
class Player:
    def __init__(self):
        self.Y = 213
        self.V = 0
        self.Points = 0
```

## game.py
```python
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)

class Game:
    def __init__(self, screen):
        self.Serving = True
        self.Running = True
        self.screen = screen

    def drawPlayers(self, A, B):
        pygame.draw.rect(self.screen, WHITE, (0, A.Y, 10, 75))
        pygame.draw.rect(self.screen, WHITE, (740, B.Y, 10, 75))
        
    def drawPuck(self,x, y):
        pygame.draw.circle(self.screen, WHITE, (x,y), 10, 1)
    
    def drawScores(self,screen, A, B):
        font = pygame.font.Font('freesansbold.ttf', 45)
    
        textA = font.render(str(A.Points), True, WHITE) 
        textRectA = textA.get_rect() 
        textRectA.center = (250, 425) 
        screen.blit(textA, textRectA) 
    
        textB = font.render(str(B.Points), True, WHITE) 
        textRectB = textA.get_rect() 
        textRectB.center = (500, 425) 
        screen.blit(textB, textRectB) 
        
```

## main.py
```python
import pygame
import random
import math
from player import Player
from game import Game

WHITE = (255,255,255)
BLACK = (0,0,0)

# Setup
pygame.init()
screen = pygame.display.set_mode((750, 500)) # set width & height
pygame.display.set_caption('Pong - Nick Ramsay')

# setup game
game = Game(screen)

# define positions for players and puck
A = Player()
B = Player()

px = 100
py = 0
pxv = float(0)
pyv = float(0)

# setup players

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

    game.drawPlayers(A, B)
    game.drawPuck(px,py)
    game.drawScores(screen, A, B)

    # Update Screen
    pygame.display.update()
```