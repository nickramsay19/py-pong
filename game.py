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
        