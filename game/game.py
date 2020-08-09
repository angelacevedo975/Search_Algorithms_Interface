import pygame
from .constants import *
from .objects import *
from collections import deque

class Game:
    
    def __init__(self):
        pygame.init()
        self.surface= pygame.display.set_mode( (WIDTH, WIDTH)  )
        pygame.display.set_caption( TITLE )
        self.clock= pygame.time.Clock()
        
        
    def start(self):
        while(True):
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    break
                
            pressed= pygame.key.get_pressed()
            if pressed[ pygame.K_1 ]:
                self.num=1
                break
            
            self.surface.fill( PURPLE )
            font = pygame.font.Font("freesansbold.ttf", 24)
            title_font = pygame.font.Font("freesansbold.ttf", 36)
            
            title= title_font.render("Path Finding Algorithms", True, (255,255,255) )
            title_rect= title.get_rect()
            title_rect.midtop= (WIDTH//2, WIDTH//2-100)
            
            text1=font.render("1- Breadth First Search", True, (255,255,255) )
            text_rect1= text1.get_rect()
            text_rect1.midtop= (WIDTH //2 , WIDTH//2+100)
            
            text2=font.render("2- Depth First Search", True, (255,255,255) )
            text_rect2= text2.get_rect()
            text_rect2.midtop= (WIDTH //2 , WIDTH//2+150)
            
            self.surface.blit( title, title_rect )
            self.surface.blit( text1, text_rect1 )
            self.surface.blit( text2, text_rect2 )
            pygame.display.flip()
            
        self.init()
        
    def init(self):
        self.running=True
        self.first=False
        self.last= False
        self.routing= False
        self.generate_grid()
        self.run()
    
    def generate_grid(self):
        size= WIDTH // NUM_COL
        grid=[]
        visited=[]
        route=[]
        for row in range(NUM_COL):
            grid.append([])
            visited.append([])
            route.append([])
            for col in range(NUM_COL):
                node= Node( row*size , col*size, size, WHITE, self.surface)
                grid[row].append( node )
                visited[row].append( False )
                route[row].append( None )
                
        self.grid= grid
        self.visited= visited
        self.route=route
        
    def get_pos(self, pos):
        pos_x, pos_y = pos
        size= WIDTH // NUM_COL
        return pos_x//size, pos_y//size
        
    
    def event(self):
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                self.running= False
        if pygame.mouse.get_pressed()[0]:
            pos_x, pos_y = self.get_pos( pygame.mouse.get_pos() )
            if not self.first:
                self.grid[ pos_x ][ pos_y ].color= PURPLE
                self.first_pos= pos_x, pos_y
                self.first=True
            
            if self.first and not self.last:
                if not ( pos_x, pos_y ) == self.first_pos:
                    self.grid[ pos_x ][ pos_y ].color= ORANGE
                    self.last_pos= pos_x, pos_y
                    self.last=True
            
            if self.first and self.last and not (pos_x, pos_y) == self.first_pos and not (pos_x, pos_y) == self.last_pos:
                pos_x, pos_y = self.get_pos( pygame.mouse.get_pos() )
                self.grid[ pos_x ][ pos_y ].color= BLACK
                
        pressed= pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            if self.routing:
                self.init()
            if not self.routing and self.last and self.num==1:
                self.bfs()
            
    def draw_grid(self):
        for row in self.grid:
            for node in row:
                node.draw()
    
    def draw_lines(self):
        size= WIDTH // NUM_COL
        for row in range( NUM_COL ):
            pygame.draw.line(self.surface, GREY, (0,row*size) , (WIDTH,row*size) )
            pygame.draw.line(self.surface, GREY, (row*size,0) , (row*size,WIDTH) )
            
            self.grid[row][0].color= BLACK
            self.grid[row][NUM_COL-1].color= BLACK
            self.grid[0][row].color= BLACK
            self.grid[NUM_COL-1][row].color= BLACK
    
    
    def draw(self):
        self.surface.fill( WHITE )
        self.draw_grid()
        self.draw_lines()
        
    
    def run(self):
        while self.running:
            self.clock.tick(120)
            self.event()
            self.draw()
            self.update()
        
        
    def update(self):
        pygame.display.flip()
        
        
    
    
    
    def get_neig( self, pos ):
        pos_x, pos_y = pos
        vector_x= [-1,1,0,0]
        vector_y= [0,0,-1,1]
        neig=[]
        for x, y in zip( vector_x, vector_y ):
            n_x, n_y = pos_x+x, pos_y+y
            if n_x < 0 or n_y < 0:
                continue
            if n_x >= NUM_COL or n_y >= NUM_COL:
                continue
            
            if self.grid[ n_x ][n_y ].color== BLACK:
                continue
            if self.visited[n_x][n_y]:
                continue
            if (n_x, n_y)!= self.last_pos:
                self.grid[n_x][n_y].color= GREY
                self.grid[n_x][n_y].draw()
            self.route[ n_x ][ n_y]= pos
            neig.append( (n_x,n_y) )
        return neig
    
    def create_route(self):
        pos_x, pos_y= self.route[self.last_pos[0]][self.last_pos[1]]
        while not self.route[pos_x][pos_y] == None:
            node= self.grid[pos_x][pos_y]
            node.color= RED
            node.draw()
            pos_x, pos_y = self.route[pos_x][pos_y]
        pygame.display.flip()
    
    def bfs(self):
        self.routing=True
        queue= deque()
        self.visited[self.first_pos[0]][self.first_pos[1]]= True
        queue+= self.get_neig(self.first_pos)
        while queue:
            pos_x, pos_y= queue.popleft()
            if self.visited[pos_x][pos_y]:
                continue
            
            self.visited[ pos_x ][ pos_y ]= True
            if (pos_x, pos_y) == self.last_pos:
                print("founddd")
                print( pos_x,pos_y )
                print( self.route[pos_x][pos_y] )
                self.create_route()
                break
            self.grid[pos_x][pos_y].color= GREEN
            self.grid[pos_x][pos_y].draw()
            pygame.display.flip()
            queue+= self.get_neig( (pos_x, pos_y) )
    
    
    