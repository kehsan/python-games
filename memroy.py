# implementation of card game - Memory

		

                     ###### The program should be loaded on to             ####
                     ###### http://www.codeskulptor.org/ to be able to run ####

            ## You flip two cards if the same they remain visible 
	    ## Need to remeber the cards that were fliped and not visible
            ## How many turns it takes to uncover all the cards

import simplegui
import random

lst1=range(8)
random.shuffle(lst1)
lst2=range(8)
random.shuffle(lst2)
lst = lst1 + lst2

turns = 0

exposed = range(16)
for i in exposed:
    exposed[i]=False
    

# helper function to initialize globals
def new_game():
    global state, turns, exposed
    state = 0
    turns = 0
   
    random.shuffle(lst1)
    
    random.shuffle(lst2)
    lst = lst1 + lst2

    label.set_text('turns = '+str(turns))
     
    for i in range(len(exposed)):
        exposed[i]=False
       
    
# define event handlers
def mouseclick(pos):
    global first, second, state, turns
    
        
    index = pos[0]/50
    if exposed[index] != True:   
        exposed[index]= True
        if state == 0:
            first = index
   
        elif state == 1:
            second = index      
       
        if state == 2:   #must find out if the two exposed are the same
    
            if (lst[first]!=lst[second]):
            
                exposed[first]= False
                exposed[second] = False
        
           
            first = index
            state = 0
            turns += 1
            label.set_text('turns = '+str(turns))
       
           
        if state == 0:
            state =1
        elif state == 1:
            state = 2
        else:
            state = 0 
   
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    x,y = 0,100
    for i in range(len(lst)):               
        canvas.draw_text(str(lst[i]), (x+10,y/2+10),35,'White') 
        
        if exposed[i] == False:
            canvas.draw_polygon([(x, y), (x+50, y), (x+50, y-100),(x,y-100)],
                        1, 'Gold','Green')
        x += 50
    


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
