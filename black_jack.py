# Mini-project #6 - Blackjack


  		     ###### The program should be loaded on to             ####
                     ###### http://www.codeskulptor.org/ to be able to run ####
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
player_loses = False
outcome = ""
score=0
player_score = 0
dealer_Score = 0
count_once = True
deck = []
player = []
dealer = []

value = 0
player_value = 0
dealer_value = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class

class Hand:
    global player_value, dealer_value
    def __init__(self):
        # listt holding what is in the hand
        # maybe divide into two for suit and rank
        #
        self.suit = []
        self.rank = []
        self.value = 0
        card= Card('S','A')
        pass	# create Hand object

    def __str__(self):
        # returns string presentation of a hand
        s = ''
        for i in range(len(self.suit)):
        
            s += str(self.suit[i])
            s += str(self.rank[i])
            s += ' '
        return 'the hand contains ' + s
                                         
        

    def add_card(self, card):
              
        self.suit.append(card[0]) # adds the suit
        self.rank.append(card[1]) # adds the rank
        #print 'suit ', self.suit
        #print 'rank ', self.rank
        
        #player.append(self.rank)
        
        
        return self.rank
        
        

    def get_value(self):
        
        global value, in_play, player,dealer, player_value, dealer_value
        self.value = 0
        self.hand=[]
        #choose who hand to count
        if in_play==True:
            self.hand=player
       #     print 'player', self.hand
        else:
            self.hand=dealer
       #     print ' dealer', self.hand
            
        for i in range(len(self.hand)):
            #split=player[i]
            split=self.hand[i]
            
            self.value += VALUES[split[1]]
        if in_play==True:
            player_value = self.value
        else:
            dealer_value=self.value
        
            
        if self.value>21:
            in_play = False
        
        value = self.value
        
       
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, card_size, [pos[0] + card_size[0] / 2, pos[1] + card_size[1] / 2], card_size)
  
# define deck class 
class Deck:
    def __init__(self):
       
        self.deck=[]
        self.suits = SUITS
        self.ranks = RANKS
        self.deal = []
        
        
        for i in range(len(self.suits)):
            for j in range(len(self.ranks)):
                self.deck.append(str(self.suits[i])+str(self.ranks[j]))
        # create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)
        # use random.shuffle()

    def deal_card(self):
        self.deal=self.deck.pop(len(self.deck)-1) #taking the first element of deck
                            # must delete it
        
        return self.deal	# deal a card object from the deck
    
    def __str__(self):
        return str(self.deck) 
            # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play,player,dealer,count_once
    global player_loses,player_value, dealer_value
    game_deck = Deck()
   
    player_hand = Hand()
    dealer_hand = Hand()
   
    player_value, dealer_value = 0, 0
    dealer = []
    player = []
    
    count_once=True
    in_play = True
    player_loses = False
    # your code goes here
    game_deck.shuffle()
    
    
    for i in range(2): 
        # adds player cards
        player_card=game_deck.deal_card()
        #hand.add_card(player_card)
        player_hand.add_card(player_card)
        player.append(player_card)
        
        
        # adds dealer cards
        dealer_card=game_deck.deal_card()
        #hand.add_card(player_card)
        dealer_hand.add_card(dealer_card)
        dealer.append(dealer_card) 
        
       
    #print 'dealer=',dealer,'player', player
    in_play = True

def hit():
    global value, player_value, dealer_value,player, score, in_play
    global player_loses
    hand = Hand()
    game_deck  = Deck()
    
 
    # if the hand is in play, hit the player
    if in_play==True:
    
        player_card=game_deck.deal_card()
        hand.add_card(player_card)
        player.append(player_card)
       #print player
        player_value=hand.get_value()
              
    player_value = value
    
   
    # if busted, assign a message to outcome, update in_play and score
    
    if player_value > 21:
        print ' Busted'
        score -= 1
        
        player_loses = True
        value = 0
       
        print 'hit deal for a new game'
      
def stand():
    global in_play,value, dealer_value,player_value,score,count_once
    global player_loses
    hand = Hand()
    game_deck  = Deck()
    
    in_play=True
    hand.get_value()
   
    in_play=False
    
    if player_loses ==False:
    
        if player_value <= 21 :
            in_play = False
            hand.get_value()
            
    
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while value<17:
        # adds dealer cards
            dealer_card=game_deck.deal_card()
            hand.add_card(dealer_card)
            dealer.append(dealer_card)
            hand.get_value()
            
            
        else:
            print 'Player Busted: Deal New Game:'
        
        
        dealer_value = value 
  
    
        if count_once==True and player_loses==False:
            if dealer_value>=player_value and dealer_value<=21 and player_value<=21:
                print 'Dealer Wins'
                score -=1
            else:
                print 'The  player wins'
                score += 1
            count_once=False
    in_play=False
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global score, in_play, player_loses, CARD_SIZE
    # test to make sure that card.draw works, replace with your code below
    global hand_value, dealer_value
    
    canvas.draw_text('Dealer', (120, 80), 30, 'Red')    
    for j in range(len(dealer)):
        split=dealer[j]      
        card=Card(split[0],split[1])
        card.draw(canvas,[100+j*CARD_SIZE[0],100])
    
    
    
    if in_play==True:
        x=96
        y=200
        canvas.draw_polygon([(x, y), (x+76, y), (x+76, y-100),(x,y-100)],
                        1, 'Gold','Red')
    if in_play == True and player_loses == False:
        canvas.draw_text('Hit or Stand?', (220, 300), 40, 'Blue')

    if in_play==False or player_loses == True:   
        if player_value > 21:
            canvas.draw_text('Player loses ', (300, 300), 40, 'Blue')
        elif dealer_value > 21:
            canvas.draw_text('dealer loses ', (300, 300), 40, 'Blue')
        elif dealer_value >= player_value:       
            canvas.draw_text('Player loses ', (300, 300), 40, 'Blue')
        elif dealer_value < player_value:       
            canvas.draw_text('Dealer loses ', (300, 300), 40, 'Blue')
        canvas.draw_text('Hit Deal For New Game', (40, 550), 40, 'Red')

    canvas.draw_text('Player', (120, 380), 30, 'Red')
    for i in range(len(player)):      
        split=player[i]      
        card=Card(split[0],split[1])
        card.draw(canvas,[100+i*CARD_SIZE[0],400])
    
    
    canvas.draw_text('score = ', (400, 80), 30, 'Red')
    canvas.draw_text(str(score), (540, 80), 30, 'Red')
    
  
        
  
#    card.draw(canvas, [300, 300])
   


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
