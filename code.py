import pygame #pygame allows screen output
import math #math allows math functions
import time #time allows time between frames to be calculated (delta_time)

pygame.init() #pygame required function

def add(vector1, vector2):
    return Vector(vector1.x + vector2.x, vector1.y + vector2.y)
def subtract(vector1, vector2):
    return Vector(vector1.x - vector2.x, vector1.y - vector2.y)
def multiply(vector, scalar):
    return Vector(vector.x * scalar, vector.y * scalar)
def normalize(vector):
    return Vector(vector.x / vector.get_length(), vector.y / vector.get_length())
def length(vector):
    return math.sqrt(vector.x * vector.x + vector.y * vector.y)
def angle(vector):
    return math.atan(vector.y/(vector.x + 0.0001))
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)
def rotate(vector, degrees):
    radians = math.radians(degrees)
    x = vector.x * math.cos(radians) - vector.y * math.sin(radians)
    y = vector.x * math.sin(radians) + vector.y * math.cos(radians)
    return Vector(x, y)

class Vector:
    def __init__(self, x, y):
        self.x = x #creates x and y values for the vector
        self.y = y
    def add(self, vector):  # math operation functions for vector math
        self = add(self, vector)
    def subtract(self, vector):
        self = subtract(self, vector)
    def multiply(self, scalar):
        self = mutliply(self, scalar)
    def normalize(self):
        self = normalize(self)
    def get_angle(self):
        return angle(self)
    def get_length(self):
        return length(self)
    def pair(self):
        return (self.x, self.y)

class Player:
    def __init__(self, x, y, vx, vy, radius):
        self.position = Vector(x, y) #player has an position vector, a velocity vector, and a circle object attached 
        self.velocity = Vector(vx, vy)
        self.circle = Circle(x, y, radius)
    def move(self, vector):
        self.position.x += vector.x
        self.position.y += vector.y
    def goto(self, vector):
        self.position = vector
    def rect_update(self):
        self.circle.position.x = self.position.x
        self.circle.position.y = self.position.y
         
circle_obstacle_list = []
class Circle:
    def __init__(self, x, y, radius):


        self.position = Vector(x, y)
        self.radius = radius

        circle_obstacle_list.append(self)
    def distance_to(self, circle):
        x_distance = self.position.x - circle.position.x
        y_distance = self.position.y - circle.position.y
        return abs(Vector(x_distance, y_distance).get_length())
    def distance_to_point(self, point):
        x_distance = self.position.x - point[0]
        y_distance = self.position.y - point[1]
        return abs(Vector(x_distance, y_distance).get_length())
    def collided_with(self, circle):
        if self.distance_to(circle) <= self.radius + circle.radius: return True
        else: return False
    def collided_with_point(self, point):
        if self.distance_to_point(point) <= self.radius: return True
        else: return False
    def delete(self):
        circle_obstacle_list.remove(self)
 
line_list = []
class Line():
    def __init__(self, x1, y1, x2, y2):

        point_distance = 1

        vector = normalize(Vector(x2 - x1, y2-y1))
        self.length = math.sqrt( (x2 - x1) ** 2 + (y2 - y1) ** 2 )
        self.slope = (y2-y1) / (x2 - x1)
        self.direction = abs(x2-x1) == x2-x1
        self.points = []
        self.points.append((x1, y1))
        self.circles = []
        self.normal_force = Vector(-vector.y, vector.x)
        self.angle = math.atan(self.slope)
        
        i = 1
        while True:
            
            x = x1 + (i * vector.x * point_distance)
            y = y1 + (i * vector.y * point_distance)

            if self.direction == True and x > x2:

                self.points.append((x2, y2))
                break
            elif self.direction == False and x < x2:
                self.points.append((x2, y2))
                break
            
            self.points.append( (x,y) )

            i += 1

        line_list.append(self)
    
    def display_points(self):
        for point in self.points:
            pygame.draw.circle(screen, BLACK, (point[0], point[1]), 3)

    def display_line(self):
        pygame.draw.line(screen, RED, self.points[0], self.points[len(self.points) - 1])

COLOR_INACTIVE = (0, 0, 0)
COLOR_ACTIVE = (175, 175, 175)
FONT = pygame.font.Font(None, 32)

input_box_list = []
class InputBox():
    def __init__(self, x, y, w, h, identification, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.id = identification
        input_box_list.append(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_INACTIVE if self.active else COLOR_ACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

text_box_list = []
class TextBox():
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        
        text_box_list.append(self)
    def draw(self):
        text_surface = FONT.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface,(self.x,self.y))

run = True # game runs while run == True

screen_width = 1600 #width of screen in pixels
screen_height = 900 #height of screen in pixels

#rgb values for common colors
WHITE = (255,255,255) 
RED = (255, 0, 0)
BLACK = (0,0,0)

#constants
GRAVITY = 400
AIR_RESISTANCE = 100
FLAP_FORCE = 300

screen = pygame.display.set_mode((screen_width, screen_height))  #creates screen with specified width and height
pygame.display.set_caption("Physics Simulation by Sean Harwick")

#creating objects
player = Player(0, 0, 0, 0, 10) #player

#lines
line1 = Line(100, 100, 400, 400) 
line2 = Line(400, 400, 401, 500)
line3 = Line(400, 500, 600, 400)
line4 = Line(800, 100, 900, 600)
line5 = Line(100, 800, 700, 801)

#input boxes
gravity_input = InputBox(screen_width - 300, 100, 140, 32, 1, text=str(GRAVITY)) 
air_resistance_input = InputBox(screen_width - 300, 200, 140, 32, 2, text=str(AIR_RESISTANCE))
flap_force_input = InputBox(screen_width - 300, 300, 140, 32, 3, text=str(FLAP_FORCE))

#text boxes
TextBox(screen_width - 300, 60, "Gravity")
TextBox(screen_width - 300, 160, "Air Resistance (x)")
TextBox(screen_width - 300, 260, "Flap Force")
TextBox(screen_width - 300, screen_height - 300, "Controls:")
TextBox(screen_width - 300, screen_height - 270, "Arrow keys:")
TextBox(screen_width - 300, screen_height - 250, "add velocity in")
TextBox(screen_width - 300, screen_height - 230, "opposite direction")
TextBox(screen_width - 300, screen_height - 200, "Space:")
TextBox(screen_width - 300, screen_height - 180, "set velocity to zero")

delta_time = 0
while run:
    frame_start = time.perf_counter()
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    
    #draws and updates player
    player.position.x += player.velocity.x * delta_time
    player.position.y += player.velocity.y * delta_time
    player.rect_update()
    pygame.draw.circle(screen, RED, (player.position.x, player.position.y), player.circle.radius)

    #gravity and air resistance
    player.velocity.y += GRAVITY * delta_time
    player.velocity.x += ((player.velocity.x > 0) * -AIR_RESISTANCE + (player.velocity.x < 0) * AIR_RESISTANCE) * delta_time

    #screen wrap
    if player.position.x > screen_width: player.position.x = 0
    if player.position.x < 0: player.position.x = screen_width
    if player.position.y > screen_height: player.position.y = 0
    if player.position.y < 0: player.position.y = screen_height
    

    for line in line_list:

        line.display_line() #displays line

        for point in line.points:

            if player.circle.collided_with_point(point):

                #static collision
                distance = player.circle.distance_to_point(point)
                overlap = player.circle.radius - distance
                player.position.x += overlap * ((player.position.x - point[0]) / distance)
                player.position.y += overlap * ((player.position.y - point[1]) / distance)
                player.rect_update()
                
                #bounce
                player.velocity = rotate(player.velocity, -math.degrees(line.angle))
                player.velocity = Vector(player.velocity.x, -player.velocity.y)
                player.velocity = rotate(player.velocity, math.degrees(line.angle))
        
    for box in input_box_list:
        box.update()
        box.draw(screen)
    
    for box in text_box_list:
        box.draw()

    if keys[pygame.K_SPACE]: #set velocity to zero while  space is held
        player.velocity = Vector(0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit on close
            run = False

        for box in input_box_list:
            user_input = box.handle_event(event) #handle event returns the input of the box
            
            if user_input != None:

                try:
                    #sets corresponding variables for the box input
                    if box.id == 1: 
                        GRAVITY = int(user_input)
                    elif box.id == 2:
                        AIR_RESISTANCE = int(user_input)
                    elif box.id == 3:
                        FLAP_FORCE = int(user_input)
                except:
                    pass

        #single flap motion with arrow keys
        if event.type == pygame.KEYDOWN:  
            if  event.key == pygame.K_UP:
                player.velocity.y += FLAP_FORCE

            if  event.key == pygame.K_DOWN:
                player.velocity.y -= FLAP_FORCE

            if  event.key == pygame.K_LEFT:
                player.velocity.x += FLAP_FORCE

            if  event.key == pygame.K_RIGHT:
                player.velocity.x -= FLAP_FORCE

    pygame.display.update() #updates the screen
    delta_time = (time.perf_counter() - frame_start) #calculation for delta time