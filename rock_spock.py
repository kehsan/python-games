# Rock-paper-scissors-lizard-Spock template

                ## This is the game from Big Bang Theory show 
                ## It is a game betwee you and random choosing by the computer
			
                     ###### The program should be loaded on to             ####
                     ###### http://www.codeskulptor.org/ to be able to run ####

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    # delete the following pass statement and fill in your code below
    if name== 'rock':
        number=0
        return number
    elif name=='Spock':
        number=1
        return number
    elif name=='paper':
        number=2
        return number
    elif name=='lizard':
        number=3
        return number
    elif name =='scissors':
        number=4
        return number
    else:
        print 'wrong name'
        return 

    # convert name to number using if/elif/else
    # don't forget to return the result!


def number_to_name(number):
    # delete the following pass statement and fill in your code below
    if number==0:
        name='rock'
        return name
    elif number==1:
        name='Spock'
        return name
    elif number==2:
        name='paper'
        return name
    elif number==3:
        name='lizard'
        return name
    elif number==4:
        name='scissors'
        return name
    else:
        print 'wrong number'
        return
   
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    

def rpsls(player_choice): 
    import random
    # delete the following pass statement and fill in your code below
    
    
    # print a blank line to separate consecutive games
    print ' '

    # print out the message for the player's choice
    player_choice=raw_input(' choose a name') 
    print ('player chooses %s') %player_choice
  

    # convert the player's choice to player_number using the function name_to_number()
    player_number=name_to_number(player_choice)
    
    
    # compute random guess for comp_number using random.randrange()
    comp_number=random.randrange(0,5)
    

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice=number_to_name(comp_number)
    
    # print out the message for computer's choice
    print ('computer choice %s') %comp_choice

    # compute difference of comp_number and player_number modulo five
    difference = (player_number - comp_number) % 5
    # use if/elif/else to determine winner, print winner message
    if difference == 0:
        print ('it is a tie!')
    elif (difference ==1) or (difference == 2):
        print ('palyer wins!')
    elif (difference ==3) or (difference ==4):
        print ('computer wins!')
    else:
        print (' we have wrong choices')
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")



# always remember to check your completed program against the grading rubric


