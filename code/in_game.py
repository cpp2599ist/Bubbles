###Module Description###
#----------------------------------------------
# Function: Deals with all things game-related

import classes 
import numpy as np
import pygame
import game_graphics as ggraph
import random
import math
import time

#launched= False

#----------------------------------------------
# Function: 
# Input: config -> class that contains the info from the config file
# Output:
def game_loop(background_sized, config,bubbles, bubble_in_play, game ):
    #White Background 
    config.screen.blit(background_sized[0], (0, ggraph.SIZE_BOARD))
    config.screen.blit(background_sized[1], (0,0))
    
    #Draw Control Board
    controls=ggraph.control_board(config)

    #Draw Bubbles
    ggraph.draw_bubbles(config, bubbles)
    ggraph.draw_next_bubble(config,bubble_in_play[0])

    #If a bubble is not in movement
    if bubble_in_play[1].launched == False:
        #Pointer
        (x,y), alpha=line(config)
        ggraph.draw_line(config, (x,y), alpha)
        
        #Draw bubble
        ggraph.draw_one_bubble(config,bubble_in_play[1])
        
        #Events
        bubbles=check_num_plays(config, bubbles)
        game, new_game=events(controls, config, bubble_in_play, alpha, bubbles)
        
        #Check if it is a game over
        if game == True:
            game=game_over(bubbles)
        
        #Check new game
        if new_game== True:
            bubbles=init_board(config)
            config.score=0
        
    else:
        #Ball is in movement
        ggraph.launch_bubble(config, bubble_in_play, bubbles)
    
    #Update Screen
    pygame.display.update()
    return game, bubbles



#----------------------------------------------
# Function: initializes a game board, randomly generating bubbles
# Input: config -> class that contains the info from the config file
# Output: bubbles -> matrix with the bubbles generated
def init_board(config):
    #Generate game board
    n_bubbles = int (config.width / (2*config.r))
    #Calculate the max number of lines
    max_lines= int(config.height/(2*config.r) ) -config.initial_lines -1
    #Create Matrix
    bubbles= np.empty((max_lines+config.initial_lines, n_bubbles ), dtype=classes.bubble)
    
    #Fill matrix 
    for i in range(max_lines+ config.initial_lines):
        for j in range(n_bubbles):
            if i < config.initial_lines:
                #classes.bubble(x,y,color)
                bubbles[i][j]=classes.bubble(j*2*config.r + config.r,i*2*config.r + config.r + ggraph.SIZE_BOARD, random.randrange(1,10))
            else:
                #empty
                bubbles[i][j]=classes.bubble(j*2*config.r + config.r,i*2*config.r + config.r + ggraph.SIZE_BOARD, 0)
    return bubbles




#----------------------------------------------
# Function: handles the pygame events
# Input: controls -> list that contains the button's position in a rect object
# Output: game-> True while game is running, new_game-> True when a new game is created
def events(controls, config, bubble_in_play, alpha, bubbles):
    game=True
    new_game= False
    launched = False

    #Wait for an event
    for event in pygame.event.get():
        #Close Window
        if event.type == pygame.QUIT:
            game= False
        #Right Click
        if pygame.mouse.get_pressed()==(True,False,False):
            pos = pygame.mouse.get_pos()
            #Check if any buttons were pressed
            game, new_game= ggraph.check_buttons(controls, pos)
            if pos[1]>ggraph.SIZE_BOARD:
                bubble_in_play[1].launched = True
                #Define anlge of launch
                config.number_plays+= 1
                bubble_in_play[1].angle= alpha
                return game, new_game
    
    return game, new_game



#----------------------------------------------
# Function: 
# Input: 
# Output: 
def load_colors(config):
    colors_list=[]
    # 1-red
    colors_list.append(pygame.image.load("./images/red.png"))
    # 2 purple
    colors_list.append(pygame.image.load("./images/purple.png"))
    # 3 blue
    colors_list.append(pygame.image.load("./images/blue.png"))
    # 4 cyan
    colors_list.append(pygame.image.load("./images/cyan.png"))
    # 5 green
    colors_list.append(pygame.image.load("./images/green.png"))
    # 6 yellow
    colors_list.append(pygame.image.load("./images/yellow.png"))
    # 7 brown
    colors_list.append(pygame.image.load("./images/brown.png"))
    # 8 black
    colors_list.append(pygame.image.load("./images/black.png"))
    # 9 white 
    colors_list.append(pygame.image.load("./images/white.png"))

    for i, color in enumerate(colors_list):
        colors_list[i]=pygame.transform.scale(color, (2*config.r, 2*config.r))
    return colors_list


#----------------------------------------------
# Function: matches the number to a color
# Input: bubble -> the corresponding number of the bubble
# Output: color -> (R,G,B)
def pick_color(bubble, config):
    if bubble!=0:
        return (config.colors_list[bubble-1])
    else:
        return(config.colors_list[8])



#----------------------------------------------
# Function: 
# Input:
# Output: 
def bubble_in_play(bubble_in_play, config):
    bubble_in_play[1].color= bubble_in_play[0].color
    bubble_in_play[1].x=int(config.width/2)
    bubble_in_play[1].y=config.height+ggraph.SIZE_BOARD-config.r
    bubble_in_play[0].color=random.randrange(1,10)



#----------------------------------------------
# Function: 
# Input:
# Output: 
def line(config):
    y_base= config.height + ggraph.SIZE_BOARD - config.r
    x_base=int(config.width/2)
    
    #Define the points
    p1=pygame.mouse.get_pos()
    p2=(x_base, y_base)
    p3=(x_base+10, y_base)
    
    #Calculate the angle
    v0 = np.array(p1) - np.array(p2)
    v1 = np.array(p3) - np.array(p2)
    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    alpha= np.degrees(angle)
    
    if alpha<0:
        p1=list(p1)
        p1[1]=y_base
        p1=tuple(p1)
        if alpha>-90:
            alpha=0
        else:
            alpha=180
    
    #Calculate the line size
    base=p1[0]-p2[0]
    perpend=p1[1]-p2[1]
    dist=math.hypot(base,perpend)
    line_size=4*config.r
    alpha_rad = np.radians(alpha)
    
    #Reduce the line size
    p4=(x_base + line_size*math.cos(alpha_rad), y_base - line_size*math.sin(alpha_rad) )
    
    return p4, alpha_rad




#----------------------------------------------
# Function: 
# Input:
# Output: 
def calculate_distance(p1,p2):
    dist=math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2  )
    return dist



#----------------------------------------------
# Function: 
# Input:
# Output: 
def is_first_line(config, bubbles, bubble_in_play):
    if ggraph.SIZE_BOARD<=bubble_in_play.y<=ggraph.SIZE_BOARD+2*config.r: #is in the first line
        position= int(bubble_in_play.x / (2*config.r))
        if bubbles [0][position].color==0:
            bubbles[0][position].color= bubble_in_play.color
            bubble_in_play.j=position
            bubble_in_play.i=0
            bubble_in_play.launched = False
        return
    bubble_in_play.launched = True



#----------------------------------------------
# Function: 
# Input:
# Output:
def collision(bubbles, bubble_in_play, config):
    collide_dist=[]
    collide_pos=[]
    pre_collide_pos=[]
    boom=False
    game= True
    #Go through board
    for i in range (len(bubbles[:,0])):
        for j in range (len(bubbles[0])):
            if bubbles[i][j].color!=0:
                #Calculate distance between two bubbles
                dist=calculate_distance([bubble_in_play.x, bubble_in_play.y],[bubbles[i][j].x, bubbles[i][j].y])
                #There is a collision
                if dist < (2*config.r*config.dl):
                    #Save information
                    collide_dist.append(dist)
                    collide_pos.append([i,j])
                    pre_collide_pos.append([bubble_in_play.x, bubble_in_play.y])
                    boom= True
    
    #See which position is the closest
    if boom == True:
        index=collide_dist.index(min(collide_dist))
        #Where to attach the next bubble
        bubbles=collision_where(collide_pos[index], bubble_in_play, bubbles, config, pre_collide_pos[index] )



#----------------------------------------------
# Function: 
# Input:
# Output:
def collision_where(collide_pos, bubble_in_play, bubbles, config, position):
    i=collide_pos[0]
    j=collide_pos[1]
    b=[bubbles[i][j].x, bubbles[i][j].y]
    game= True
    #Attach
    
    #To the right
    if j+1<len(bubbles[0]) and  position[1]>=(-position[0]+b[0]+b[1]) and position[1]<=(position[0]-b[0]+b[1]) and bubbles[i][j+1].color==0:
        bubbles[i][j+1].color= bubble_in_play.color
        bubble_in_play.i=i
        bubble_in_play.j=j+1
        bubble_in_play.launched= False
    
    #Below
    elif position[1]>=(-position[0]+b[0]+b[1]) and position[1]>=(position[0]-b[0]+b[1])and bubbles[i+1][j].color==0:
        bubbles[i+1][j].color = bubble_in_play.color
        bubble_in_play.i=i+1
        bubble_in_play.j=j
        bubble_in_play.launched = False
    
    #To the left
    elif j-1>=0  and position[1]<=(-position[0]+b[0]+b[1]) and position[1]>=(position[0]-b[0]+b[1])and bubbles[i][j-1].color==0:
        bubbles[i][j-1].color = bubble_in_play.color
        bubble_in_play.i=i
        bubble_in_play.j=j-1
        bubble_in_play.launched= False
    
    #Above
    elif i-1>=0 and  position[1]<=(-position[0]+b[0]+b[1]) and position[1]<=(position[0]-b[0]+b[1])and bubbles[i-1][j].color==0:
        bubbles[i-1][j].color = bubble_in_play.color
        bubble_in_play.i=i-1
        bubble_in_play.j=j
        bubble_in_play.launched= False
    
    return bubbles



#----------------------------------------------
# Function: 
# Input:
# Output:
def pop_bubble(bubbles, color, i,j, pop_list):
    #print(i,j)
    bubbles[i][j].checked= True

    #Right
    if j+1<len(bubbles[0]) and bubbles[i][j+1].color== color and bubbles[i][j+1].checked == False:
        pop_list.append([i,j+1])
        pop_list=pop_bubble(bubbles, color, i, j+1, pop_list)

    #Below
    if i+1<len(bubbles[:,0]) and bubbles[i+1][j].color == color and bubbles[i+1][j].checked == False:
        pop_list.append([i+1,j])
        pop_list=pop_bubble(bubbles, color, i+1, j, pop_list)

    #Left
    if j-1>= 0 and bubbles[i][j-1].color == color and bubbles[i][j-1].checked == False:
        pop_list.append([i,j-1])
        pop_list=pop_bubble(bubbles, color, i, j-1, pop_list)

    #Above
    if i-1>=0 and bubbles[i-1][j].color == color and bubbles[i-1][j].checked == False:
        pop_list.append([i-1,j])
        pop_list=pop_bubble(bubbles, color, i-1, j, pop_list)

    #UpRight
    if i-1>=0 and j+1<len(bubbles[0]) and bubbles[i-1][j+1].color == color and bubbles[i-1][j+1].checked == False:
        pop_list.append([i-1,j+1])
        pop_list=pop_bubble(bubbles, color, i-1, j+1, pop_list)

    #UpLeft
    if i-1>=0 and j-1>= 0 and bubbles[i-1][j-1].color == color and bubbles[i-1][j-1].checked == False:
        pop_list.append([i-1,j-1])
        pop_list=pop_bubble(bubbles, color, i-1, j-1, pop_list)

    #DownRight
    if i+1<len(bubbles[:,0]) and j+1<len(bubbles[0]) and bubbles[i+1][j+1].color == color and bubbles[i+1][j+1].checked == False:
        pop_list.append([i+1,j+1])
        pop_list=pop_bubble(bubbles, color, i+1, j+1, pop_list)

    #DownLeft
    if i+1<len(bubbles[:,0]) and j-1>=0 and bubbles[i+1][j-1].color == color and bubbles[i+1][j-1].checked == False:
        pop_list.append([i+1,j-1])
        pop_list=pop_bubble(bubbles, color, i+1, j-1, pop_list)

    return pop_list



#----------------------------------------------
# Function: 
# Input:
# Output:
def clean_board(bubbles, pop_list, config):
    for [i,j] in pop_list:
        if len(pop_list)>=3:
            bubbles[i][j].color=0
            config.score = config.score + 1
        bubbles[i][j].checked = False

#----------------------------------------------
# Function: 
# Input:
# Output:
def game_over(bubbles):
    (rows,cols)=bubbles.shape
    for i in range(cols):
        if bubbles[rows-1][i].color!=0:
            print('Game Over')
            return False
    return True



#----------------------------------------------
# Function: 
# Input:
# Output:
def check_num_plays(config, bubbles):
    if config.number_plays == config.N_moves:

        #Generate a new line
        lines=(int(config.width/(2*config.r)))
        new_line= np.empty((lines ,1), dtype=classes.bubble)
            #Fill array 
        for j in range(len(new_line)):
            new_line[j]=classes.bubble(j*2*config.r + config.r, config.r + ggraph.SIZE_BOARD, random.randrange(1,10))
        #Move all lines one down
        for i in range (len(bubbles[:,0])-1,0, -1):
            for j in range(len (bubbles[0])):
                bubbles[i][j].color=bubbles[i-1][j].color

        #Add new line to the matrix
        bubbles[0]=new_line.T
        config.number_plays=0
    return bubbles