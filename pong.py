# Implementation of classic arcade game Pong

                     ###### The program should be loaded on to             ####
                     ###### http://www.codeskulptor.org/ to be able to run ####

		## The classic Ping-pong video game from the 70s
		## Up and Down Arrow for the right player to move the pad
		## 'w', 's' key for the left player to move the pad
                ## Hit 'New Game' button to start the game

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
#
paddle1_pos= HEIGHT/2
paddle2_pos= HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
#
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel=[0,0]
#
left_score = 0
right_score = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists


    ball_pos = [WIDTH/2, HEIGHT/2]
    
   
    if direction == "RIGHT":
        ball_vel[1] = ball_vel[1] * -1
    if direction == "LEFT":
        ball_vel[0] =  ball_vel[0] * -1
        ball_vel[1] = ball_vel[1] * -1

 
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    global left_score, right_score
    global ball_vel, ball_pos
    

    paddle1_pos= HEIGHT/2
    paddle2_pos= HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0

    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel=[0,0]

    left_score = 0
    right_score = 0
    
    button.set_text('New Game')
    
#    ball_vel[0] = random.randrange(1, 4)
#    ball_vel[1] = random.randrange(4,8)
    #it seems that if vel[0] > 4 there is problem
    #print 'vel[0] ', ball_vel[0], 'vel[1] ', ball_vel[1]
    
    ball_vel[0] = 4
    ball_vel[1] = 11
    # need to draw a ball for new game
    spawn_ball('RIGHT')
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
    global WIDTH, HEIGHT
    global PAD_WIDTH, PAD_HEIGHT, HALF_PAD_HEIGHT, HALD_PAD_WIDTH
    global left_score, right_score
    
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
       
    # update ball  
    
    
    # calculate ball position
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
#*************    this is for hitting the side wall returns that has

    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH :
        ball_vel[0] = ball_vel[0] * -1     
    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        ball_vel[0] = ball_vel[0] * -1
#        
#*******Bouncing off the vertical and the floor ***************   

    if ball_pos[1] <= BALL_RADIUS   :
        ball_vel[1] = ball_vel[1] * -1
    if ball_pos[1] >= HEIGHT - BALL_RADIUS :
        ball_vel[1] = ball_vel[1] * -1 
   
# padd and ball collision 
    global RIGHT,LEFT
    
    #***** left side
    if ball_pos[0] == BALL_RADIUS + PAD_WIDTH:
        if (ball_pos[1]>= paddle2_pos - PAD_HEIGHT/2) and (ball_pos[1] <= paddle2_pos + PAD_HEIGHT/2):
            ball_vel[1] = (ball_vel[1] +ball_vel[1]*0.1) * -1            
            ball_pos[1] += ball_vel[1] 
       
            #LEFT = True           
        else:
            right_score += 1
            LEFT = False
            spawn_ball("LEFT")
            
     # ******  right side       
    if ball_pos[0] == WIDTH - BALL_RADIUS - PAD_WIDTH:
        if (ball_pos[1] >= paddle1_pos - PAD_HEIGHT/2) and (ball_pos[1] <= paddle1_pos + PAD_HEIGHT/2):          
            ball_vel[1] = (ball_vel[1] +ball_vel[1]*0.1) * -1        
            ball_pos[1] += ball_vel[1]             
            #RIGHT = True
        else:
            left_score += 1
            RIGHT = False
            spawn_ball("RIGHT")
            
#  Start a new game if score is 5
    if left_score == 5 or right_score == 5:
        #how to stop the game
        #button.set_text('Press for new game') 
        
        new_game()
        pass
        
        
    # draw ball
    
    #if button.get_text() == 'New Game':
    canvas.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 10, 'White','white')
    
    # update paddle's vertical position, keep paddle on the screen
# NEED CODE TO STOP THE PADDLE GO OFF THE SCREEN
    paddle1_pos += paddle1_vel   
    paddle2_pos += paddle2_vel
    
    if paddle1_pos <= PAD_HEIGHT/2 :
        paddle1_pos = PAD_HEIGHT/2       
    elif paddle1_pos >= HEIGHT - PAD_HEIGHT/2 :
        paddle1_pos = HEIGHT - PAD_HEIGHT/2        
          
    if paddle2_pos <= PAD_HEIGHT/2 :
        paddle2_pos = PAD_HEIGHT/2
    elif paddle2_pos >= HEIGHT - PAD_HEIGHT/2 :
        paddle2_pos = HEIGHT - PAD_HEIGHT/2        
               
    # draw paddles

    canvas.draw_line([WIDTH , paddle1_pos - HALF_PAD_HEIGHT],
                     [WIDTH , paddle1_pos + HALF_PAD_HEIGHT],          
                    PAD_WIDTH,'White')
    canvas.draw_line([0 , paddle2_pos - HALF_PAD_HEIGHT],
                     [0 , paddle2_pos + HALF_PAD_HEIGHT],          
                     PAD_WIDTH,'White')     
    # draw scores
    
    #if button.get_text() == 'New Game':
    canvas.draw_text(str(left_score), [250, 50], 20, 'Blue')
    canvas.draw_text(str(right_score), [350, 50], 20, 'Blue')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    global paddle1_pos,  paddle2_pos
    
    
    up_tick=6
    if key == simplegui.KEY_MAP['down']:  
        paddle1_vel += up_tick                             
          
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel  += up_tick * -1          
        
    if key == simplegui.KEY_MAP['s']:
        paddle2_vel += up_tick      
         
    if key == simplegui.KEY_MAP['w']:   
        paddle2_vel += up_tick * -1       
      
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel  = 0
    if key == simplegui.KEY_MAP['down']:
       paddle1_vel  = 0
    if key == simplegui.KEY_MAP['w']:
        paddle2_vel  = 0
    if key == simplegui.KEY_MAP['s']:
        paddle2_vel  = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
event=frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

button=frame.add_button('New Game', new_game,100)
 
# start frame
#new_game()
frame.start()
