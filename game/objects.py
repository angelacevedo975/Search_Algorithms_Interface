import pygame

class Node:
    def __init__(self, pos_x, pos_y, size, color, surface):
        self.pos_x= pos_x
        self.pos_y= pos_y
        self.color= color
        self.surface= surface
        self.size= size
        pygame.draw.rect(self.surface, self.color, (self.pos_x, self.pos_y, size, size ) )
        
    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.pos_x, self.pos_y, self.size, self.size ) )