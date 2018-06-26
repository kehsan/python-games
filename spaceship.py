

                     ###### The program should be loaded on to             ####
                     ###### http://www.codeskulptor.org/ to be able to run ####
		### UP Arrow for thrusters
                ### Left arrow for turning left
                ### Right arrow for turning right
                ### Space bar to fire missiles

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface          
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

FIRING_POSITION = [WIDTH // 2, HEIGHT]
FIRING_LINE_LENGTH = 60
FIRING_ANGLE_VEL_INC= 0.03
firing_angle = 0
firing_angle_vel = [0,0]

thruster = False
forward = 0

rock_group = set([])
missile_group = set([])
explosion_group = set([])


started = False
                   
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 100)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def group_collide(group,sprite_other_object):
    
    rs = set([]) # temp set for removing 
    for g in group:       
        if g.collision(sprite_other_object):         
            rs.add(g)
            group.difference_update(rs) # removes rs from group
            sound = explosion_sound
            sound.play()
            explosion_group.add(Sprite((g.pos[0], g.pos[1]), [0,0], 0, 0, explosion_image, explosion_info))
            return True # it is hit
        #sound.rewind()   
    return False
    
def group_group_collide( rock_grp,missile_grp):
    no_of_hits = 0
    for r in rock_grp:
        for m in missile_grp:
            if r.collision(m):
                 no_of_hits += 1
                 rock_grp.discard(r)
                 sound = explosion_sound
                 sound.play()
                 explosion_group.add(Sprite((r.pos[0], r.pos[1]), [0,0], 0, 0, explosion_image, explosion_info))
                 
    return no_of_hits
    
    #sprite1.collide(sprite2)

# Ship 

class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        
        global thruster, FIRING_POSITION, lives, score, started
        if started == True :
            canvas.draw_text('lives '+ str(lives),(80,50),24,'White')
        else:
            canvas.draw_text('lives '+ str(0),(80,50),24,'White')

        canvas.draw_text('Score '+ str(score),(680,50),24,'White')
       
        if started == True:
            sound=soundtrack
            sound.play()
            
        if thruster == False:
            sound=ship_thrust_sound
            sound.rewind()
        if thruster == True:
            self.trust = True
            self.thrusters(canvas)
      
        else:
            #draw ship without thrusters
            canvas.draw_image(self.image,self.image_center,self.image_size,
                                 self.pos,self.image_size,self.angle)
       
        if group_collide(rock_group,my_ship):
            lives -= 1
            if lives <= 0:
                sound=soundtrack
                sound.rewind()
                started = False
            
        score += group_group_collide(rock_group,missile_group)
       
            
    def shoot(self):
        
        self.miss_x=0
        self.miss_y=0
        global a_missile, FIRING_POSITION
        
        #Missile orientation is and position is updated
        # in update
        missile_x = FIRING_POSITION[0]        
        missile_y = FIRING_POSITION[1]        
               
        self.miss_x += self.vel[0] + forward[0] * 3
        self.miss_y += self.vel[1] + forward[1] * 3
             
        missile_group.add(Sprite([missile_x, missile_y], [self.miss_x,self.miss_y], 0, 0, 
                                  missile_image, missile_info, missile_sound))
     
    def thrusters(self,canvas):
        global thruster
        #draws ship with thrusters
       
        canvas.draw_image(self.image,(self.image_center[0]+85,self.image_center[1]),self.image_size,
                          self.pos,self.image_size,self.angle)
        
        sound=ship_thrust_sound
        sound.play()
        
    def update(self):
        global firing_angle, thruster, FIRING_POSITION, forward
       # self.angle_vel =0.05 #shoulb be very low below 0.1
        forward=angle_to_vector(self.angle) 
        
     
        self.pos[0] += self.vel[0] 
        self.pos[1] += self.vel[1] 
        self.angle += firing_angle
        
        # adding friction
        
        self.vel[0] *= 0.99   #(1-c)
        self.vel[1] *= 0.99
        
        # adding velocity 
        if thruster:
            self.vel[0]+=forward[0] *0.06 
            self.vel[1]+=forward[1] *0.06
            
        if self.pos[0] >= 800:
            self.pos[0] = 0
        elif self.pos[0] <= 0:
            self.pos[0] = 800
        elif self.pos[1] >= 600:
            self.pos[1] = 0
        elif self.pos[1] <= 0:
            self.pos[1] = 600
        
        # Takes the missile to the tip of the ship
        x = self.radius * forward[0]     
        y = self.radius * forward[1]
       
        FIRING_POSITION[0]=self.pos[0] + x 
        FIRING_POSITION[1]=self.pos[1] + y  
         
    
# Sprite class
class Sprite:
    global my_Ship
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
       # canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
         if self.animated == True:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0]*self.age,self.image_center[1]], self.image_size,
                            self.pos, self.image_size, self.angle)
            
         else:
            canvas.draw_image(self.image,self.image_center,self.image_size,
                          self.pos,self.image_size,self.angle)
    def update(self):
        
      
        self.pos[0] += self.vel[0] 
        self.pos[1] += self.vel[1] 
        
        self.angle += random.randrange(0,4)
        
        if self.pos[0] >= 800:
            self.pos[0] = 0
        elif self.pos[0] <= 0:
            self.pos[0] = 800
        elif self.pos[1] >= 600:
            self.pos[1] = 0
        elif self.pos[1] <= 0:
            self.pos[1] = 600
            
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
        
    def collision(self,other_object):         
        distance=dist(self.pos, other_object.pos)     
     
        if distance  <= self.radius + other_object.radius:
    
            return True
        else:
            return False

def process_sprite_group(group,canvas):
    for g in group:
        g.draw(canvas)
        if g.update() :
             rs = set([]) # temp set for removing 
             rs.add(g)           
             group.difference_update(rs)
            
        
def keydown(key):
    global my_ship, firing_angle_vel, firing_angle, my_ship_stuck, thruster
    global FIRING_ANGLE_VEL_INC, FIRING_POSITION, started, lives, score
    if simplegui.KEY_MAP["space"] == key:
        my_ship_stuck = False
        orient = angle_to_vector(firing_angle)    
        my_ship.shoot()
              
    elif simplegui.KEY_MAP["right"] == key:       
        firing_angle+= FIRING_ANGLE_VEL_INC
    elif simplegui.KEY_MAP["left"] == key:
        firing_angle -= FIRING_ANGLE_VEL_INC
    elif simplegui.KEY_MAP['up'] == key:
        thruster = True
    
    if started == False:
        score = 0
        sound=soundtrack
        sound.rewind()
        started = True
    
        

def keyup(key):
    global firing_angle, FIRING_ANGLE_VEL_INC, thruster
    if simplegui.KEY_MAP["right"] == key:
        firing_angle -= FIRING_ANGLE_VEL_INC
    elif simplegui.KEY_MAP["left"] == key:
        firing_angle += FIRING_ANGLE_VEL_INC
    elif  simplegui.KEY_MAP['up'] == key:
        thruster = False
        
    
def draw(canvas):
    global time, rock_group, missile_group, score, lives, started
    global explosion_group
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    #a_rock.draw(canvas)
    process_sprite_group(rock_group,canvas)
    
    process_sprite_group(missile_group,canvas)
    
    process_sprite_group(explosion_group,canvas)
    
   # explosion_group=set([]) # clean out the explosion set after printing
   

    my_ship.update()
    
    if started == False:
        canvas.draw_image(splash_image,[200,150],[400,300],
                          [WIDTH/2,HEIGHT/2],[400,300])
        rock_group = set([])
        missile_group = set([])
        lives = 3
     #   score =0
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, a_rock
    if len(rock_group) <= 6:
        vel1 = random.randrange(1,3)
        vel2 = random.randrange(1,3)
        x = random.randrange(10,700)
        y = random.randrange(10,500)
    
        x += vel1 
        y += vel2

        rock_group.add(Sprite([x,y], [vel1, vel2],0,0, asteroid_image, asteroid_info)) 
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0,0], firing_angle, ship_image, ship_info)
rock_group.add(Sprite([WIDTH / 3, HEIGHT / 2], [8,9], 0, 0, asteroid_image, asteroid_info))

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling

timer.start()
frame.start()
