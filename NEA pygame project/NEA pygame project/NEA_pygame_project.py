#Imports
from random import randint
import pygame
import sys
import os
from pygame.locals import *


os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.display.set_caption("NEA maze generation software")

pygame.init()
clock = pygame.time.Clock()

#Screen creation
SCREENWIDTH = 1150 #Width of the screen.
SCREENHEIGHT = 600 #Height of the screen.
SCREENSIZE = [SCREENWIDTH, SCREENHEIGHT] #Array to create the screen.
SCREEN = pygame.display.set_mode(SCREENSIZE) #Variable to display the screen.

#Game states:
start_screen = True
game_start = False
settings = False
game_over = False
paused = False

#Colours:
#Using the RGB scale
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (194, 197, 204)
ORANGE = (255, 165, 0)
BROWN = (127, 72, 41)

#Button class:
class Button(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height,  text, text_color, font_size): #Constructer: Parameters to be passed if an object is to be made.
        pygame.sprite.Sprite.__init__(self) #Sets the class as a sprite.
        #Attributes:
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_color = text_color
        self.font_size = font_size
        self.shape = pygame.Rect(self.x, self.y, self.width, 60) #Creates rectangle for the button.
        self.text = text
        self.x1 = self.x + self.width #Finds the coordinates for the right side of the rectangle.
        self.y1 = self.y + self.height #Finds the coordinates for the bottoms side of the rectangle.
        button = pygame.Rect(self.x, self.y, self.width, 60) #Updates the rectangle shape to be displayed on screen.
        pygame.draw.rect(SCREEN, self.color, button) #Displays the button on screen.
        font = pygame.font.Font('freesansbold.ttf', self.font_size) #Sets the font for the text to be displayed on the button.
        text1 = font.render(self.text, True, WHITE) #Renders the text and sets the color as white so it is easily visible.
        textRect = text1.get_rect()
        textRect.center = (self.x1 - (self.width / 2), self.y1 - (self.height / 2) + 10) #Calculates the coordinates for the centre of the button so the text
        #can be positioned correctly
        SCREEN.blit(text1, (textRect))
       
    #Methods:
    def draw_updatescreen(self): #Method to update the display of the button.
        button = pygame.Rect(self.x, self.y, self.width, 60) #Updates the rectangle shape to be displayed on screen.
        pygame.draw.rect(SCREEN, self.color, button) #Displays the button on screen.
        font = pygame.font.Font('freesansbold.ttf', self.font_size) #Sets the font for the text to be displayed on the button.
        text1 = font.render(self.text, True, self.text_color) #Renders the text and sets the color as white so it is easily visible.
        textRect = text1.get_rect()
        textRect.center = (self.x1 - (self.width / 2), self.y1 - (self.height / 2) + 10) #Calculates the coordinates for the centre of the button so the text
    #can be positioned correctly
        SCREEN.blit(text1, (textRect))
         
    def update(self, x, y, width, height, color, text): #Method to update the attributes of the button.
         self.x = x
         self.y = y
         self.height = height
         self.width = width
         self.color = color
         self.text = text
         self.shape = (self.color, self.x, self.y, self.width)

#Player class:
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y, velocity, radius): 
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.shape = pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)
        self.hitbox = (self.x - 20, self.y - 20, 40, 40)

    

    def draw_updatescreen(self):
        self.shape = pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)
        self.hitbox = (self.x - 20, self.y - 20, 40, 40)
        #pygame.draw.rect(SCREEN, WHITE, self.hitbox, 2)

    def update(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

 
#Enemy class:
class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, x, y, velocity, radius):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.shape = pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)
        self.hitbox = (self.x - 20, self.y - 20, 40, 40)

    def draw_updatescreen(self):
        self.shape = pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)
        self.hitbox = (self.x - 20, self.y - 20, 40, 40)
        #pygame.draw.rect(SCREEN, WHITE, self.hitbox, 2)

    def update(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y

#Wall class:
class Wall(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shapeoutput = pygame.draw.rect(SCREEN, self.color, self.shape, 0)
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw_updatescreen(self):
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shapeoutput = pygame.draw.rect(SCREEN, self.color, self.shape, 0)
        self.hitbox = (self.x, self.y, self.width, self.height)
        #pygame.draw.rect(SCREEN, WHITE, self.hitbox, 2)

    def update(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

        

#Star class (Scoring system):
class Star(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = height
        self.width = width
        self.hitbox = (self.rect.x + 10, self.rect.y + 10, 55, 55)

    def draw_updatescreen(self):
        star = SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        self.hitbox = (self.rect.x + 10, self.rect.y + 10, 55, 55)
        #pygame.draw.rect(SCREEN, WHITE, self.hitbox, 2)
    

    def update(self, image, x, y):
        self.rect.x = x
        self.rect.y = y
        self.image = image

#Pathfinding nodes class (Enemy pathfinding):
class Nodes(pygame.sprite.Sprite):
    def __init__(self, color, x, y, radius):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.neighbours = []
        self.shape = pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)
      
    def draw_updatescreen(self):
        self.shape = pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius, 2)

    def draw_line(self):
        for x in range (len(self.neighbours)):
            pygame.draw.line(SCREEN, WHITE, (self.x, self.y), (self.neighbours[x][0].x, self.neighbours[x][0].y))

    def update(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
#Objects:

#Buttons:
MAZE_SOFTWARE = Button(GREEN, 200, 25, 700, 50, "MAZE SOFTWARE", WHITE, 60) #Title of the game.
CLICK_TO_START_GAME = Button(GRAY, 200, 250, 700, 50, "CLICK TO START GAME", WHITE, 60) #Starts the levels.
SETTINGS = Button(GRAY, 10, 400, 500, 50, "SETTINGS", WHITE, 60) #Modifys the settings.
END_GAME = Button(GRAY, 550, 400, 500, 50, "END GAME", WHITE, 60) #Ends the game.
TRY_AGAIN = Button(GRAY, 30, 400, 400, 50, "TRY AGAIN", WHITE, 60)
PAUSE = Button(GRAY, 410, 535, 300, 50, "PAUSE", WHITE, 60)
CONTINUE_GAME = Button(GRAY, 10, 400, 530, 50, "CONTINUE GAME", WHITE, 60)
COLOURBLIND_MODE = Button(GRAY, 480, 150, 650, 50, "COLOURBLIND MODE", WHITE, 60)
GO_BACK = Button(GRAY, 50, 150, 300, 50, "GO BACK", WHITE, 60)
SETTINGS2 = Button(GRAY, 200, 25, 700, 50, "SETTINGS", WHITE, 60)
NORMAL_MODE = Button(GRAY, 480, 235, 650, 50, "NORMAL MODE", WHITE, 60)
PLAYER_SPEED = Button(GREEN, 480, 315, 650, 50, "PLAYER SPEED: SLOW", WHITE, 50)
HARD_MODE = Button(RED, 480, 395, 650, 50, "HARD MODE: OFF", WHITE, 60)
END_PROGRAM = Button(GRAY, 200, 500, 650, 50, "END PROGRAM", WHITE, 60)
MOVEMENT = Button(GRAY, 480, 475, 650, 50, "MOVEMENT: GENERAL", WHITE, 50)

#Characters:
player = Player(GREEN, 50, 65, 0.5, 20)
enemy = Enemy(RED, 1050, 65, 1, 20)

#Walls (Borders of maze):
wall = Wall(BLUE, 100, 100, 30, 400)
wall2 = Wall(BLUE, 100, 0, 930, 30)
wall3 = Wall(BLUE, 1000, 100, 30, 400)
wall4 = Wall(BLUE, 100, 500, 930, 30)

#Walls (inside of maze):
wall5 = Wall(BLUE, 210, 100, 180, 50)
wall6 = Wall(BLUE, 475, 100, 180, 50)
wall7 = Wall(BLUE, 740, 100, 180, 50)
wall8 = Wall(BLUE, 215, 230, 50, 180)
wall9 = Wall(BLUE, 340, 230, 50, 180)
wall10 = Wall(BLUE, 480, 225, 50, 180)
wall11 = Wall(BLUE, 605, 225, 50, 180)
wall12 = Wall(BLUE, 740, 225, 50, 180)
wall13 = Wall(BLUE, 870, 225, 50, 180)


#Nodes for pathfinding:
node = Nodes(WHITE, 960, 65, 30)
node2 = Nodes(WHITE, 700, 65, 30)
node3 = Nodes(WHITE, 430, 65, 30)
node4 = Nodes(WHITE, 165, 65, 30)
node5 = Nodes(WHITE, 960, 180, 30)
node6 = Nodes(WHITE, 700, 180, 30)
node7 = Nodes(WHITE, 165, 180, 30)
node8 = Nodes(WHITE, 430, 180, 30)
node9 = Nodes(WHITE, 960, 450, 30)
node10 = Nodes(WHITE, 700, 450, 30)
node11 = Nodes(WHITE, 165, 450, 30)
node12 = Nodes(WHITE, 430, 450, 30)

#Connecting nodes together with neighbours array:
node.neighbours.append([node2, 2])
node.neighbours.append([node5, 5])

node2.neighbours.append([node, 1])
node2.neighbours.append([node3, 3])
node2.neighbours.append([node6, 6])

node3.neighbours.append([node2, 2])
node3.neighbours.append([node4, 4])
node3.neighbours.append([node8, 8])

node4.neighbours.append([node3, 3])
node4.neighbours.append([node7, 7])

node5.neighbours.append([node, 1])
node5.neighbours.append([node6, 6])
node5.neighbours.append([node9, 9])

node6.neighbours.append([node2, 2])
node6.neighbours.append([node5, 5])
node6.neighbours.append([node8, 8])
node6.neighbours.append([node10, 10])

node7.neighbours.append([node4, 4])
node7.neighbours.append([node8, 8])
node7.neighbours.append([node11, 11])

node8.neighbours.append([node3, 3])
node8.neighbours.append([node6, 6])
node8.neighbours.append([node7, 7])
node8.neighbours.append([node12, 12])

node9.neighbours.append([node5, 5])
node9.neighbours.append([node10, 10])

node10.neighbours.append([node6, 6])
node10.neighbours.append([node9, 9])
node10.neighbours.append([node12, 12])

node11.neighbours.append([node7, 7])
node11.neighbours.append([node12, 12])

node12.neighbours.append([node8, 8])
node12.neighbours.append([node10, 10])
node12.neighbours.append([node11, 11])

player_node_distance = [[], [], [], [], [], [], [], [], [], [], [], []]
enemy_node_distance = [[], [], [], [], [], [], [], [], [], [], [], []]

#Lists for objects
all_walls_hitbox = (wall.hitbox, wall2.hitbox, wall3.hitbox, wall4.hitbox, wall5.hitbox, wall6.hitbox, wall7.hitbox, wall8.hitbox, wall9.hitbox, wall10.hitbox, wall11.hitbox, wall12.hitbox, wall13.hitbox)
all_buttons = (CLICK_TO_START_GAME, SETTINGS, END_GAME, PAUSE, TRY_AGAIN, CONTINUE_GAME, COLOURBLIND_MODE, GO_BACK, SETTINGS2, NORMAL_MODE, END_PROGRAM)
all_characters = (player.hitbox, enemy.hitbox)
all_nodes = (node, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12)
all_walls = (wall, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11, wall12, wall13)

#Star
star = Star("starwithnobackground.png", 525, 417, 70, 70)

display_text_color = WHITE

#Text display (Scores and lives):

lives = 3
lives_and_score_font = pygame.font.Font('freesansbold.ttf', 50)
lives_text = lives_and_score_font.render("LIVES = " + str(lives), True, display_text_color)
lives_rect = lives_text.get_rect()
lives_rect.center = (120, 575)

score = 0
score_text = lives_and_score_font.render("SCORE = " + str(score), True, display_text_color)
score_rect = score_text.get_rect()
score_rect.center = (990, 575)

#Text display (Game over):
game_over_font = pygame.font.Font('freesansbold.ttf', 75)
game_over_text = game_over_font.render("GAME OVER ", True, display_text_color)
game_over_rect = game_over_text.get_rect()
game_over_rect = (300, 150)

#Text display (Paused):
paused_font = pygame.font.Font('freesansbold.ttf', 75)
paused_text = paused_font.render("GAME PAUSED", True, display_text_color)
paused_rect = paused_text.get_rect()
paused_rect = (300, 150)

#Enemy movement preset variables
previous_node = 0
current_node = all_nodes.index(all_nodes[0])
new_node_position = randint(0, len(all_nodes[current_node].neighbours))
new_node_position = all_nodes[current_node].neighbours[new_node_position - 1][1]

player_difficulty = [["PLAYER SPEED: SLOW", GREEN, 0.75], ["PLAYER SPEED: MEDIUM", ORANGE, 2], ["PLAYER SPEED: QUICK", RED, 4]]
hard_mode_states = [["HARD MODE: OFF", RED, 0], ["HARD MODE: ON", GREEN, 1]]
movement_states = [["MOVEMENT: GENERAL", RED, 0], ["MOVEMENT: STRAIGHT", GREEN, 1]]

#player difficulty preset variables
current_player_difficulty = 0
PLAYER_SPEED.text = player_difficulty[current_player_difficulty][0]
PLAYER_SPEED.color = player_difficulty[current_player_difficulty][1]
player.velocity = player_difficulty[current_player_difficulty][2]

#Hardmode button preset variables
current_hard_mode_state = 0
HARD_MODE.text = hard_mode_states[current_hard_mode_state][0]
HARD_MODE.color = hard_mode_states[current_hard_mode_state][1]

#Player  movement preset variables
current_movement_state = 0
MOVEMENT.text = movement_states[current_movement_state][0]
MOVEMENT.color = movement_states[current_movement_state][1]

mouse_clicked = False

#Finding difficulty function:
def find_current_difficulty(player_difficulty, current_player_difficulty):
    for x in range(len(player_difficulty)):
        if PLAYER_SPEED.text == player_difficulty[x][0]:
            current_player_difficulty = x
    return (current_player_difficulty)

#Changing difficulty function:
def changing_difficulty(current_player_difficulty):
    if current_player_difficulty == 2:
        current_player_difficulty = 0
    else:
        current_player_difficulty += 1
    PLAYER_SPEED.text = player_difficulty[current_player_difficulty][0]
    PLAYER_SPEED.color = player_difficulty[current_player_difficulty][1]
    player.velocity = player_difficulty[current_player_difficulty][2]


#Finding current hardmode function:
def find_current_hard_mode(hard_mode_states, current_hard_mode_state):
    for x in range(len(hard_mode_states)):
        if HARD_MODE.text == hard_mode_states[x][0]:
            current_hard_mode_state = x
    return (current_hard_mode_state)
   

#Changing current hardmode function:
def changing_hard_mode(current_hard_mode_state):
    if current_hard_mode_state == 1:
        current_hard_mode_state = 0
    else:
        current_hard_mode_state += 1
    HARD_MODE.text = hard_mode_states[current_hard_mode_state][0]
    HARD_MODE.color = hard_mode_states[current_hard_mode_state][1]
    current_hard_mode_state = hard_mode_states[current_hard_mode_state][2]
    return (current_hard_mode_state)

#Finding current movement state function:
def find_current_movement(movement_states, current_movement_state):
    for x in range(len(movement_states)):
        if MOVEMENT.text == movement_states[x][0]:
            current_movement_state = x
    return (current_movement_state)

#Changing current movement state function:
def changing_movement(current_movement_state):
    if current_movement_state == 1:
        current_movement_state = 0
    else:
        current_movement_state = 1
    MOVEMENT.text = movement_states[current_movement_state][0]
    MOVEMENT.color = movement_states[current_movement_state][1]
    current_movement_state = movement_states[current_movement_state][2]
    return (current_movement_state)


#Main loop:
while True:
    SCREEN.fill(BLACK) #Fills the screen with black.
    pos = pygame.mouse.get_pos() #Gets position of mouse.
    player_input = pygame.key.get_pressed() #Detects when keys have been pressed by user.

    #Detects when user has exited the game and clicked the mouse.
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if events.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
        else:
            mouse_clicked = False
    
    #Start screen:
    if start_screen == True:
        #Button displays:
        SCREEN.fill(BLACK)
        MAZE_SOFTWARE.draw_updatescreen()
        CLICK_TO_START_GAME.draw_updatescreen()
        SETTINGS.draw_updatescreen()
        END_GAME.draw_updatescreen()
        END_PROGRAM.draw_updatescreen()
    
        #Mouse clicking on buttons outputs:
        #Mouse and click to start game button output:
        if pygame.mouse.get_pos()[1]  < CLICK_TO_START_GAME.shape[1] + CLICK_TO_START_GAME.shape[3] and pygame.mouse.get_pos()[1] > CLICK_TO_START_GAME.shape[1]:
            if pygame.mouse.get_pos()[0]  > CLICK_TO_START_GAME.shape[0] and pygame.mouse.get_pos()[0] < CLICK_TO_START_GAME.shape[0] + CLICK_TO_START_GAME.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    start_screen = False
                    game_start = True

        #Mouse and settings button output:
        if pygame.mouse.get_pos()[1]  < SETTINGS.shape[1] + SETTINGS.shape[3] and pygame.mouse.get_pos()[1] > SETTINGS.shape[1]:
            if pygame.mouse.get_pos()[0]  > SETTINGS.shape[0] and pygame.mouse.get_pos()[0] < SETTINGS.shape[0] + SETTINGS.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    settings = True
                    start_screen = False

        #Mouse and end game button output:
        if pygame.mouse.get_pos()[1]  < END_GAME.shape[1] + END_GAME.shape[3] and pygame.mouse.get_pos()[1] > END_GAME.shape[1]:
            if pygame.mouse.get_pos()[0]  > END_GAME.shape[0] and pygame.mouse.get_pos()[0] < END_GAME.shape[0] + END_GAME.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    game_start = False
                    start_menu = True
                    (player.x, player.y) = (50, 65)
                    (enemy.x, enemy.y) = (1050, 65)
                    lives = 3
                    score = 0
                    (star.x, star.y) = (525, 417)

        #Mouse and end program button output:
        if pygame.mouse.get_pos()[1]  < END_PROGRAM.shape[1] + END_PROGRAM.shape[3] and pygame.mouse.get_pos()[1] > END_PROGRAM.shape[1]:
            if pygame.mouse.get_pos()[0]  > END_PROGRAM.shape[0] and pygame.mouse.get_pos()[0] < END_PROGRAM.shape[0] + END_PROGRAM.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()

 
    #Main game:
    if game_start == True:
        #Displays of all the characters and objects.
        SCREEN.fill(BLACK)
        player.draw_updatescreen()
        player.update(player.x, player.y, player.color)
        enemy.draw_updatescreen()
        enemy.update(enemy.x, enemy.y, enemy.color)

        #Loop to display all the walls:
        for x in range(len(all_walls)):
            all_walls[x].draw_updatescreen()
            all_walls[x].update(all_walls[x].x, all_walls[x].y, all_walls[x].color)

        
        for x in range(len(all_nodes)):
            #all_nodes[x].draw_updatescreen()
            all_nodes[x].update(all_nodes[x].x, all_nodes[x].y, all_nodes[x].radius)
            #all_nodes[x].draw_line()

        #Displays lives and score at the bottom corners of the screen:
        lives_text = lives_and_score_font.render("LIVES = " + str(lives), True, display_text_color)
        SCREEN.blit(lives_text, (lives_rect))
        score_text = lives_and_score_font.render("SCORE = " + str(score), True, display_text_color)
        SCREEN.blit(score_text, (score_rect))
        
        #Displays the pause button and detects when user has clicked on it.
        PAUSE.draw_updatescreen()
        if pygame.mouse.get_pos()[1]  < PAUSE.shape[1] + PAUSE.shape[3] and pygame.mouse.get_pos()[1] > PAUSE.shape[1]:
            if pygame.mouse.get_pos()[0]  > PAUSE.shape[0] and pygame.mouse.get_pos()[0] < PAUSE.shape[0] + PAUSE.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    paused = True
        
        #Displays the star.
        star.draw_updatescreen()
        star.update(star.image, star.rect.x, star.rect.y)

        #For loop to detects player and other object interactions.
        for x in range(13):
            if player.hitbox[1] < all_walls_hitbox[x][1] + all_walls_hitbox[x][3] and player.hitbox[1] + player.hitbox[3] > all_walls_hitbox[x][1]:
                if player.hitbox[0] + player.hitbox[2] > all_walls_hitbox[x][0] and player.hitbox[0] < all_walls_hitbox[x][0] + all_walls_hitbox[x][2]:
                        player.x = 50  
                        player.y = 65
                        if current_hard_mode_state == 1:
                            lives = lives - 1

            if enemy.hitbox[1] < all_walls_hitbox[x][1] + all_walls_hitbox[x][3] and enemy.hitbox[1] + enemy.hitbox[3] > all_walls_hitbox[x][1]:
                if enemy.hitbox[0] + enemy.hitbox[2] > all_walls_hitbox[x][0] and enemy.hitbox[0] < all_walls_hitbox[x][0] + all_walls_hitbox[x][2]:
                    enemy.x = 1050
                    enemy.y = 65
            
            if star.hitbox[1] < all_walls_hitbox[x][1] + all_walls_hitbox[x][3] and star.hitbox[1] + star.hitbox[3] > all_walls_hitbox[x][1]:
                if star.hitbox[0] + star.hitbox[2] > all_walls_hitbox[x][0] and star.hitbox[0] < all_walls_hitbox[x][0] + all_walls_hitbox[x][2]:
                    star.rect.x = randint(130, 970)
                    star.rect.y = randint(30, 470)
            
        #Player and enemy hitbox function:
        if player.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and player.hitbox[1] + player.hitbox[3] > enemy.hitbox[1]:
            if player.hitbox[0] + player.hitbox[2] > enemy.hitbox[0] and player.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                player.x = 50
                player.y = 65
                enemy.x = 1050
                enemy.y = 65
                lives -= 1

        
        #Player and star hitbox function (Scoring system):
        if player.hitbox[1] < star.hitbox[1] + star.hitbox[3] and player.hitbox[1] + player.hitbox[3] > star.hitbox[1]:
            if player.hitbox[0] + player.hitbox[2] > star.hitbox[0] and player.hitbox[0] < star.hitbox[0] + star.hitbox[2]:
                player.x = 50
                player.y = 65
                star.rect.x = randint(130, 970)
                star.rect.y = randint(30, 470)
                score += 1
        
        if enemy.hitbox[1] < star.hitbox[1] + star.hitbox[3] and enemy.hitbox[1] + enemy.hitbox[3] > star.hitbox[1]:
            if enemy.hitbox[0] + enemy.hitbox[2] > star.hitbox[0] and enemy.hitbox[0] < star.hitbox[0] + star.hitbox[2]:
                #enemy.x = 1050
                #enemy.y = 65
                star.rect.x = randint(130, 970)
                star.rect.y = randint(30, 470)
                score -= 1
        
        #Player and screen boundary functions:
        if player.x > 1150:
            player.x = -49
        if player.x < -50:
             player.x = 1149
        if player.y > 630:
            player.y = -29
        if player.y < -30:
            player.y = 629


        #Movement/Inputs:
        if current_movement_state == 0:
            if (player_input[pygame.K_LEFT]) or (player_input[K_a]):
                player.x -= player.velocity
            if (player_input[pygame.K_UP]) or (player_input[K_w]):
                player.y -= player.velocity
            if (player_input[pygame.K_DOWN]) or (player_input[K_s]):
                player.y += player.velocity
            if (player_input[pygame.K_RIGHT]) or (player_input[K_d]):
                player.x += player.velocity
        elif current_movement_state == 1:
            if (player_input[pygame.K_LEFT]) or (player_input[K_a]):
                player.x -= player.velocity
            elif (player_input[pygame.K_UP]) or (player_input[K_w]):
                player.y -= player.velocity
            elif (player_input[pygame.K_DOWN]) or (player_input[K_s]):
                player.y += player.velocity
            elif (player_input[pygame.K_RIGHT]) or (player_input[K_d]):
                player.x += player.velocity
        if (player_input[pygame.K_SPACE]):
            paused = True

        #Enemy random movement
        if new_node_position == previous_node:
            new_node_position = randint(0, len(all_nodes[current_node].neighbours))
            new_node_position = all_nodes[current_node].neighbours[new_node_position - 1][1]
            current_node = new_node_position

        #Enemy random movement:
        if new_node_position != previous_node:
            if enemy.x != all_nodes[new_node_position - 1].x:
                if enemy.x > all_nodes[new_node_position - 1].x:
                    enemy.x -= enemy.velocity
                elif enemy.x < all_nodes[new_node_position - 1].x:
                    enemy.x += enemy.velocity
            elif enemy.x == all_nodes[new_node_position - 1].x and enemy.y != all_nodes[new_node_position - 1].y:
                if enemy.y > all_nodes[new_node_position - 1].y:
                    enemy.y -= enemy.velocity
                elif enemy.y < all_nodes[new_node_position - 1].y:
                    enemy.y += enemy.velocity
            else: #Checks if the enemy is repeating movements:
                previous_node = current_node
                new_node_position = randint(0, len(all_nodes[current_node - 1].neighbours))
                new_node_position = all_nodes[current_node - 1].neighbours[new_node_position - 1][1]
                current_node = new_node_position
        
        if lives <= 0:
            game_over = True
        
    #Settings screen:
    if settings == True:
        #Text/buttons display
        SCREEN.fill(BLACK)
        SETTINGS2.draw_updatescreen()
        COLOURBLIND_MODE.draw_updatescreen()
        NORMAL_MODE.draw_updatescreen()
        GO_BACK.draw_updatescreen()
        PLAYER_SPEED.draw_updatescreen()
        HARD_MODE.draw_updatescreen()
        MOVEMENT.draw_updatescreen()

        #Mouse and colourblind button output:
        if pygame.mouse.get_pos()[1]  < COLOURBLIND_MODE.shape[1] + COLOURBLIND_MODE.shape[3] and pygame.mouse.get_pos()[1] > COLOURBLIND_MODE.shape[1]:
            if pygame.mouse.get_pos()[0]  > COLOURBLIND_MODE.shape[0] and pygame.mouse.get_pos()[0] < COLOURBLIND_MODE.shape[0] + COLOURBLIND_MODE.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    for x in range(len(all_buttons)):
                        all_buttons[x].color = RED
                        all_buttons[x].text_color = BLUE
                    for x in range(len(all_walls)):
                        all_walls[x].color = LIGHT_GREEN
                    MAZE_SOFTWARE.color = BLUE
                    MAZE_SOFTWARE.text_color = ORANGE
                    player.color = ORANGE
                    enemy.color = BROWN
                    display_text_color = BLUE
                    PLAYER_SPEED.text_color = BLUE
                    HARD_MODE.text_color = BLUE
                    MOVEMENT.text_color = BLUE

        #Mouse and normal mode button output:
        if pygame.mouse.get_pos()[1]  < NORMAL_MODE.shape[1] + NORMAL_MODE.shape[3] and pygame.mouse.get_pos()[1] > NORMAL_MODE.shape[1]:
            if pygame.mouse.get_pos()[0]  > NORMAL_MODE.shape[0] and pygame.mouse.get_pos()[0] < NORMAL_MODE.shape[0] + NORMAL_MODE.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    for x in range(len(all_buttons)):
                        all_buttons[x].color = GRAY
                        all_buttons[x].text_color = WHITE
                    for x in range(len(all_walls)):
                        all_walls[x].color = BLUE
                    MAZE_SOFTWARE.color = GREEN
                    MAZE_SOFTWARE.text_color = WHITE
                    player.color = GREEN
                    enemy.color = RED
                    display_text_color = WHITE
                    PLAYER_SPEED.text_color = WHITE
                    HARD_MODE.text_color = WHITE
                    MOVEMENT.text_color = WHITE

        #Mouse and go back output:
        if pygame.mouse.get_pos()[1]  < GO_BACK.shape[1] + GO_BACK.shape[3] and pygame.mouse.get_pos()[1] > GO_BACK.shape[1]:
            if pygame.mouse.get_pos()[0]  > GO_BACK.shape[0] and pygame.mouse.get_pos()[0] < GO_BACK.shape[0] + GO_BACK.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    start_screen = True
                    settings = False
        
        #Mouse and player speed output:
        if pygame.mouse.get_pos()[1]  < PLAYER_SPEED.shape[1] + PLAYER_SPEED.shape[3] and pygame.mouse.get_pos()[1] > PLAYER_SPEED.shape[1]:
            if pygame.mouse.get_pos()[0]  > PLAYER_SPEED.shape[0] and pygame.mouse.get_pos()[0] < PLAYER_SPEED.shape[0] + PLAYER_SPEED.shape[2]:
                if mouse_clicked:
                    changing_difficulty(find_current_difficulty(player_difficulty, current_player_difficulty))
                mouse_clicked = False
        
        #Mouse and hard mode output:
        if pygame.mouse.get_pos()[1]  < HARD_MODE.shape[1] + HARD_MODE.shape[3] and pygame.mouse.get_pos()[1] > HARD_MODE.shape[1]:
            if pygame.mouse.get_pos()[0]  > HARD_MODE.shape[0] and pygame.mouse.get_pos()[0] < HARD_MODE.shape[0] + HARD_MODE.shape[2]:
                if mouse_clicked:
                    current_hard_mode_state = (changing_hard_mode(find_current_hard_mode(hard_mode_states, current_hard_mode_state)))
                mouse_clicked = False

        #Mouse and movement output:
        if pygame.mouse.get_pos()[1]  < MOVEMENT.shape[1] + MOVEMENT.shape[3] and pygame.mouse.get_pos()[1] > MOVEMENT.shape[1]:
            if pygame.mouse.get_pos()[0]  > MOVEMENT.shape[0] and pygame.mouse.get_pos()[0] < MOVEMENT.shape[0] + MOVEMENT.shape[2]:
                if mouse_clicked:
                    current_movement_state = (changing_movement(find_current_movement(movement_states, current_movement_state)))
                mouse_clicked = False


    #Pause screen:              
    if paused == True:
        #Text/buttons display:
        game_start = False
        SCREEN.fill(BLACK)
        paused_text = paused_font.render("GAME PAUSED", True, display_text_color)
        SCREEN.blit(paused_text, (paused_rect))
        END_GAME.draw_updatescreen()
        CONTINUE_GAME.draw_updatescreen()
        
        #Mouse clicking end game button output:
        if pygame.mouse.get_pos()[1]  < END_GAME.shape[1] + END_GAME.shape[3] and pygame.mouse.get_pos()[1] > END_GAME.shape[1]:
            if pygame.mouse.get_pos()[0]  > END_GAME.shape[0] and pygame.mouse.get_pos()[0] < END_GAME.shape[0] + END_GAME.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    SCREEN.fill(BLACK)
                    start_screen = True
                    paused = False
        
        #Mouse clicking continue game button output:
        if pygame.mouse.get_pos()[1]  < CONTINUE_GAME.shape[1] + CONTINUE_GAME.shape[3] and pygame.mouse.get_pos()[1] > CONTINUE_GAME.shape[1]:
            if pygame.mouse.get_pos()[0]  > CONTINUE_GAME.shape[0] and pygame.mouse.get_pos()[0] < CONTINUE_GAME.shape[0] + CONTINUE_GAME.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    game_start = True
                    paused = False


    #Game over screen:
    if game_over == True:
        #Text/button display
        game_start = False
        SCREEN.fill(BLACK)
        game_over_text = game_over_font.render("GAME OVER ", True, display_text_color)
        SCREEN.blit(game_over_text, (game_over_rect))
        TRY_AGAIN.draw_updatescreen()
        END_GAME.draw_updatescreen()
        END_PROGRAM.draw_updatescreen()
        lives_and_score_font = pygame.font.Font('freesansbold.ttf', 75)
        score_text = lives_and_score_font.render("SCORE = " + str(score), True, display_text_color)
        score_rect.center = (425, 300)
        SCREEN.blit(score_text, (score_rect))
        
        #Mouse and try again button output:
        if pygame.mouse.get_pos()[1]  < TRY_AGAIN.shape[1] + TRY_AGAIN.shape[3] and pygame.mouse.get_pos()[1] > TRY_AGAIN.shape[1]:
            if pygame.mouse.get_pos()[0]  > TRY_AGAIN.shape[0] and pygame.mouse.get_pos()[0] < TRY_AGAIN.shape[0] + TRY_AGAIN.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    SCREEN.fill(BLACK)
                    lives = 3
                    score = 0
                    lives_and_score_font = pygame.font.Font('freesansbold.ttf', 35)
                    score_rect.center = (990, 575)
                    game_start = True
                    game_over = False
        
        #Mouse and end game button output:
        if pygame.mouse.get_pos()[1]  < END_GAME.shape[1] + END_GAME.shape[3] and pygame.mouse.get_pos()[1] > END_GAME.shape[1]:
            if pygame.mouse.get_pos()[0]  > END_GAME.shape[0] and pygame.mouse.get_pos()[0] < END_GAME.shape[0] + END_GAME.shape[2]:
                if mouse_clicked:
                    start_screen = True
                    (player.x, player.y) = (50, 65)
                    (enemy.x, enemy.y) = (1050, 65)
                    lives = 3
                    score = 0
                    (star.x, star.y) = (525, 417)
                    lives_and_score_font = pygame.font.Font('freesansbold.ttf', 35)
                    score_rect.center = (990, 575)
                    game_over = False

        #Mouse and end game button output:
        if pygame.mouse.get_pos()[1]  < END_PROGRAM.shape[1] + END_PROGRAM.shape[3] and pygame.mouse.get_pos()[1] > END_PROGRAM.shape[1]:
            if pygame.mouse.get_pos()[0]  > END_PROGRAM.shape[0] and pygame.mouse.get_pos()[0] < END_PROGRAM.shape[0] + END_PROGRAM.shape[2]:
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
    pygame.display.update()