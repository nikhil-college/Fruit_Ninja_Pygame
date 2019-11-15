from __future__ import division
from pygame import *
from math import *
from random import randint, choice, uniform
from time import localtime as local
from time import time as clock
import datetime

#Initializations
init()
mixer.init()
font.init()

#Time object that helps set FPS
fps = time.Clock()

#Creating the display surface, setting the caption and icon
width, height = 1280,720
screen = display.set_mode((width, height))
display.set_caption("Fruitz by god")
icon = transform.scale(image.load("Other Images/Icon.png"), (64, 64))
display.set_icon(icon)

#Opening file for writing high scores
highFile = open("Files/High Scores.txt")
oldHS = int(highFile.read()); highscore = oldHS

#Variable for the current screen
mode = "Splash Screen"

'''Importing and setting up all gameplay images'''
apple_main = transform.scale(image.load("Fruit Images/apple.png"), (128, 128)).convert()
apple_bit1 = transform.scale(image.load("Fruit Images/applebit1.png"), (36, 48)).convert()
apple_bit2 = transform.scale(image.load("Fruit Images/applebit2.png"), (44, 68)).convert()

banana_main = transform.scale(image.load("Fruit Images/banana.png"), (128, 128)).convert()
banana_bit1 = transform.scale(image.load("Fruit Images/bananabit1.png"), (56, 56)).convert()
banana_bit2 = transform.scale(image.load("Fruit Images/bananabit2.png"), (92, 62)).convert()

coconut_main = transform.scale(image.load("Fruit Images/coconut.png"), (128, 128)).convert()
coconut_bit1 = transform.scale(image.load("Fruit Images/coconutbit1.png"), (74, 102)).convert()
coconut_bit2 = transform.scale(image.load("Fruit Images/coconutbit2.png"), (64, 100)).convert()

lemon_main = transform.scale(image.load("Fruit Images/lemon.png"), (128, 128)).convert()
lemon_bit1 = transform.scale(image.load("Fruit Images/lemonbit1.png"), (76, 70)).convert()
lemon_bit2 = transform.scale(image.load("Fruit Images/lemonbit2.png"), (74, 84)).convert()

pear_main = transform.scale(image.load("Fruit Images/pear.png"), (128, 128)).convert()
pear_bit1 = transform.scale(image.load("Fruit Images/pearbit1.png"), (56, 66)).convert()
pear_bit2 = transform.scale(image.load("Fruit Images/pearbit2.png"), (36, 68)).convert()

watermelon_main = transform.scale(image.load("Fruit Images/watermelon.png"), (128, 128)).convert()
watermelon_bit1 = transform.scale(image.load("Fruit Images/watermelonbit1.png"), (84, 98)).convert()
watermelon_bit2 = transform.scale(image.load("Fruit Images/watermelonbit2.png"), (128, 132)).convert()

#Correlating the fruit types with their respective images in dictionaries
Fruit_Images = {"apple": apple_main, "banana": banana_main, "coconut": coconut_main, "lemon": lemon_main, \
                "pear": pear_main, "watermelon": watermelon_main}

Bit_Images1 = {"apple": apple_bit1, "banana": banana_bit1, "coconut": coconut_bit1, "lemon": lemon_bit1, \
               "pear": pear_bit1, "watermelon": watermelon_bit1}

Bit_Images2 = {"apple": apple_bit2, "banana": banana_bit2, "coconut": coconut_bit2, "lemon": lemon_bit2, \
               "pear": pear_bit2, "watermelon": watermelon_bit2}


imgs = [apple_main, apple_bit1, apple_bit2, banana_main, banana_bit1, banana_bit2, 
        coconut_main, coconut_bit1, coconut_bit2, lemon_main, lemon_bit1, lemon_bit2, 
        pear_main, pear_bit1, pear_bit2, watermelon_main, watermelon_bit1, watermelon_bit2]


for img in imgs:
    img.set_colorkey((0, 0, 0))
    if imgs.index(img) % 3 == 0:
        img.set_alpha(250)
    else:
        img.set_alpha(125)


wall1 = image.load("Wallpapers/Wallpaper1.png").convert()
wall1.set_alpha(255)
wall1List = [(0, 0, 0), (235, 61, 0), (0, 0, 0), (247, 237, 0)]     

wall2 = image.load("Wallpapers/Wallpaper2.png").convert()
wall2.set_alpha(150)
wall2List = [(0, 179, 224), (247, 237, 0), (163, 232, 255), (188, 226, 158)]

wall3 = image.load("Wallpapers/Wallpaper5.png").convert()
wall3.set_alpha(255)
wall3List =  [(255, 250, 80), (255, 255, 255), (98, 222, 253), (244, 101, 36)]

wall4 = image.load("Wallpapers/Wallpaper4.png").convert()
wall4.set_alpha(255)
wall4List = [(247, 237, 0), (0, 0, 0), (245, 182, 203), (98, 222, 253)]


wallpaper = wall3
wallList = wall3List

#Importing the images for the knife blades in the game
kitchenblade = transform.scale(image.load("Other Images/KitchenBlade.png"), (128, 128))
fightingblade = transform.scale(image.load("Other Images/FightingBlade.png"), (128, 128))
blade = "kitchen"

blades = {"kitchen": kitchenblade, "fighting": fightingblade}

#Indexes of the respective colours (score, HS, time, FPS)
colS = 0
colHS = 1
colT = 2
colFPS = 3

#Loading of other screens in game (credits, options, pause menu, etc.)
load_screen = image.load("Screens/PythonLoader.png").convert()

splash_screen = image.load("Screens/Loading Screen.png").convert()

credits_screen = image.load("Screens/Untitled.png").convert()

options_screen = image.load("Screens/Options.png").convert()

customize_screen = image.load("Screens/Options_Customize.png").convert()

gameover_screen = image.load("Screens/Game Over.png").convert()

paused_screen = image.load("Screens/Paused.png").convert()

'''Importing Sound Effects and Background Music'''
#Sound effects
Press = mixer.Sound("Sounds/Press.wav"); Press.set_volume(0.5)
Tick = mixer.Sound("Sounds/Tick.wav"); Tick.set_volume(0.5)
Punch = mixer.Sound("Sounds/Punch.wav"); Punch.set_volume(0.5)
Splash = mixer.Sound("Sounds/Splash.wav"); Splash.set_volume(0.5)
Woosh = mixer.Sound("Sounds/Woosh.wav"); Woosh.set_volume(0.5)

#Background music
song1 = mixer.Sound("Sounds/Pompeii.wav"); song1.set_volume(0.25)
song2 = mixer.Sound("Sounds/All I Do Is Win.wav"); song2.set_volume(0.25)
song3 = mixer.Sound("Sounds/Animals.wav"); song3.set_volume(0.25)
song4 = mixer.Sound("Sounds/Wipe Out.wav"); song4.set_volume(0.25)
song = song3                
'''Importing fonts'''

smallFont = font.Font("Fonts/Avenir.ttc", 18)
medFont = font.Font("Fonts/Avenir.ttc", 40)
largeFont = font.Font("Fonts/Avenir.ttc", 60)

'''Function definitions'''

def mp():   
    return mouse.get_pos() 


def lclick():   
    if mouse.get_pressed()[0] == 1:
        return True
    else:
        return False


def collide(col_type, basepoint, movepoint, len1, len2 = None):
    if col_type == "circle":
        bx, by = basepoint
        mx, my = movepoint 
        if ((bx-mx)**2 + (by-my)**2)**0.5 <= len1 and lclick() == True:
            return True
        else:
            return False

    elif col_type == "rect":
        bx, by = basepoint
        mx, my = movepoint
        collideRect = Rect (bx-len1//2,by-len2//2,len1, len2)
        if collideRect.collidepoint((mx,my)) and lclick() == True:
            return True
        else:
            return False


def randfruit():
    fruits = ["apple", "banana", "coconut", "lemon", "pear", "watermelon"]
    return choice(fruits)

'''Setting up object classes'''
CollisionRadius = {"apple": 35, "banana": 64, "coconut": 40, "lemon": 50, "pear": 40, "watermelon": 50}

#List of the options of x starting values
x_choices = [x for x in range (0,width//4+1,2)] + [x for x in range (width//4, 3*width//4 + 1)] + [x for x in range (3*width//4, width+1,40)]

#Class Fruit: Contains all Fruits that have not yet been sliced, while they are on the screen
class Fruit:
    def __init__ (self, fruit_type, loading = False):
        self.x, self.y = choice(x_choices), height + 1

        self.fruit_type = fruit_type

        self.dist = abs(self.x - width//2)

        self.vx = self.dist//70

        self.vy = uniform (7,8)

        self.angle = 0

        #1 means moving from left to right, -1 means moving from right to left
        if self.x > width//2: 
            self.direction = -1

        elif 0 <= self.x <= width//4:
            self.direction = 1
            
        else:
            self.direction = choice ([1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1])

        if self.fruit_type == "banana":
            self.collide_type = "rect"
        else:
            self.collide_type = "circle"

        self.draw_image = transform.rotate(Fruit_Images[self.fruit_type], self.angle)
        self.dx, self.dy = int(self.x - (self.draw_image.get_width()//2)), int(self.y - (self.draw_image.get_height()//2))

        self.loading = loading 

    
    def updatePos(self):
        if self.loading == False:
            self.vy -= 0.07

            self.x += int(self.vx*self.direction)
            self.y -= int(self.vy)

        #Adds by self.direction so that the fruits rotate the same way they're moving
        self.angle += self.direction*choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3]) 

        self.draw_image = transform.rotate(Fruit_Images[self.fruit_type], self.angle)

        #By creating dx and dy, x and y are at the center of the fruit image and we can draw circles for collision
        self.dx, self.dy = int(self.x - (self.draw_image.get_width()//2)), int(self.y - (self.draw_image.get_height()//2))        

    def checkCollide(self):
        if self.fruit_type != "banana":
            if collide(self.collide_type, (self.x, self.y), mp(), CollisionRadius[self.fruit_type]) == True:
                return True
            else:
                return False
        else:
            if collide(self.collide_type, (self.x, self.y), mp(), self.draw_image.get_width(), self.draw_image.get_height()) == True:
                return True
            else:
                return False             #True means colliding, False means not colliding

    def drawFruit(self, surf):
        surf.blit(self.draw_image, (self.dx, self.dy))
        
    #Makes the corresponding sound if the fruit is sliced ("punch" for bananas, "woosh" otherwise)
    def makeSound(self):
        if self.fruit_type == "banana":
            Punch.play()
        else:
            Woosh.play()

air = []    
cut = []   

for i in range (choice([1, 1, 2, 2, 2, 3, 3, 4, 5])):
    air.append(Fruit(randfruit()))


class Bits:
    def __init__ (self, bit_type, startx, starty, ang, vy):
        self.bit_type = bit_type
        self.x1, self.x2, self.y = startx, startx, starty

        self.angle = ang

        self.vx = uniform (3, 4)        
        self.vy = vy                    

        self.draw_image1 = transform.rotate (Bit_Images1[self.bit_type], self.angle)
        self.draw_image2 = transform.rotate (Bit_Images2[self.bit_type], self.angle)

    def updatePos(self):
        self.vy += 0.3                  

        self.x1 -= self.vx              
        self.x2 += self.vx
        self.y += self.vy

        self.draw_image1 = transform.rotate (Bit_Images1[self.bit_type], self.angle)
        self.draw_image2 = transform.rotate (Bit_Images2[self.bit_type], self.angle)


    def drawBits(self, surf):
        surf.blit(self.draw_image1, (int(self.x1), int(self.y)))
        surf.blit(self.draw_image2, (int(self.x2), int(self.y)))  



class Button:
    def __init__ (self, rect, up, down, click = None):
        self.rect = rect
        self.up = up           
        self.down = down

        if click != None:
            self.click = click 

    #If the mouse is simply over the button, this returns true to draw the "Down" image
    def checkHover(self):
        if self.rect.collidepoint(mp()):
            return True
        else:
            return False

    #If the button is being clicked, this returns True
    def checkClicked(self):
        if self.checkHover() == True and lclick():
            return True
        else:
            return False

    def drawButton(self, surf):
        surf.blit(self.up, (self.rect.x, self.rect.y))
        if self.checkHover() == True:
            surf.blit(self.down, (self.rect.x, self.rect.y))

       
        elif hasattr(self, "click") and self.checkClicked() == True:
            surf.blit(self.click, (self.rect.x, self.rect.y))


class Blade:
    def __init__(self, blade_type):
        self.blade_type = blade_type
        self.original_image = blades[self.blade_type]

    def updateBlade(self, pos):
        x = pos[0]
        if x >= width//2:
            self.draw_image = transform.rotate(self.original_image, 45)
        else:
            self.draw_image = transform.rotate(self.original_image, 45)
            self.draw_image = transform.flip(self.draw_image, True, False)
        return self.draw_image

    def drawBlade(self, surf, pos):
        x = pos[0]
        if x < width//2:
            surf.blit(self.updateBlade(pos), (pos[0] - self.updateBlade(pos).get_width()//2 - 50, pos[1] - self.updateBlade(pos).get_height()//2 + 50))
        else:
            surf.blit(self.updateBlade(pos), (pos[0] - 40, pos[1] - self.updateBlade(pos).get_height()//2 + 50))

'''Creating buttons'''

Wall1_Button = Button(Rect (138, 396, 467, 72), image.load("Buttons/Wall1Up.png").convert(), \
        image.load("Buttons/Wall1Down.png").convert(), image.load("Buttons/Wall1Click.png").convert())

Wall2_Button = Button(Rect (675, 396, 467, 72), image.load("Buttons/Wall2Up.png").convert(), \
        image.load("Buttons/Wall2Down.png").convert(), image.load("Buttons/Wall2Click.png").convert())

Wall3_Button = Button(Rect (138, 492, 467, 72), image.load("Buttons/Wall5Up.png").convert(), \
        image.load("Buttons/Wall5Down.png").convert(), image.load("Buttons/Wall5Click.png").convert())

Wall4_Button = Button(Rect (675, 492, 467, 72), image.load("Buttons/Wall4Up.png").convert(), \
        image.load("Buttons/Wall4Down.png").convert(), image.load("Buttons/Wall4Click.png").convert())

Kitchen_Button = Button(Rect (138, 630, 467, 72), image.load("Buttons/KitchenUp.png").convert(), \
        image.load("Buttons/KitchenDown.png").convert())

Fighting_Button = Button(Rect (675, 630, 467, 72), image.load("Buttons/FightingUp.png").convert(), \
        image.load("Buttons/FightingDown.png").convert())

Done_Button = Button(Rect (50, 50, 150, 50), image.load("Buttons/DoneUp.png").convert(), \
        image.load("Buttons/DoneDown.png").convert())

Pause_Button = Button(Rect (50, 650, 150, 50), image.load("Buttons/PauseUp.png").convert(), \
        image.load("Buttons/PauseDown.png").convert())

Customize_Button = Button(Rect (406, 431, 467, 72), image.load("Buttons/CustomizeUp.png").convert(), \
        image.load("Buttons/CustomizeDown.png").convert())

Sound_Button = Button(Rect (406, 551, 467, 72), image.load("Buttons/SoundUp.png").convert(), \
        image.load("Buttons/SoundDown.png").convert())

PlayAgain_Button = Button(Rect (787, 428, 467, 72), image.load("Buttons/PlayAgainUp.png").convert(), \
        image.load("Buttons/PlayAgainDown.png").convert())

MainMenu_Button = Button(Rect (787, 526, 467, 72), image.load("Buttons/MainMenuUp.png").convert(), \
        image.load("Buttons/MainMenuDown.png").convert())

Quit_Button = Button(Rect (787, 624, 467, 72), image.load("Buttons/QuitUp.png").convert(), \
        image.load("Buttons/QuitDown.png").convert())

'''Creating blade'''
blade = Blade("kitchen")

'''Defining the functions for each screen'''
def splashScreen():
    global oldSec, oldMin, startSec, secLeft, mode, game

    splashChoice = None
    drawSplashBits = False

    #For these three fruit objects, "loading" is set to True: we don't want the x and y values to update
    splashFruits = [Fruit("banana", True), Fruit("apple", True), Fruit("watermelon", True)]
    for fruit in splashFruits:
        fruit.x = 653 + 225*splashFruits.index(fruit) + 64
        fruit.y = 394 + 64
        fruit.vx, fruit.vy = 0, 0

   
    modes = {"banana": "Credits", "apple": "Play", "watermelon": "Options"}

    running = True
    mouse.set_visible(False)

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        for fruit in splashFruits:
            fruit.updatePos()
            
        if drawSplashBits == True:
            splashChoice.updatePos()

        #If the bits fall off the screen, the mode is updated
        if drawSplashBits == True:
            if splashChoice.y > height:
                mode = modes[splashChoice.bit_type]
                if mode == "Play":
                    oldSec = local(clock())[5]
                    oldMin = local(clock())[4]
                    secLeft = 60

                    air = []    
                    cut = []    

                    for i in range (choice([1, 1, 2, 2, 2, 3, 3, 4, 5])):
                        air.append(Fruit(randfruit()))
                    song.play()

                running = False
                drawBits = False

        #Checking for collisions 
        for fruit in splashFruits:
            if fruit.checkCollide() == True:
                fruit.makeSound()
                splashChoice = Bits(fruit.fruit_type, fruit.x, fruit.y, fruit.angle, uniform(0.5, 1.5))
                del splashFruits[splashFruits.index(fruit)]
                drawSplashBits = True

        screen.blit(splash_screen, (0,0))

        for fruit in splashFruits:
            fruit.drawFruit(screen)

        if drawSplashBits == True:
            if splashChoice.y < height:
                splashChoice.drawBits(screen)

        blade.drawBlade(screen, mp())

        display.flip()

        fps.tick(60)  

    return mode

#Credits menu, accessed by swiping the banana on the splash screen
def creditsMenu():
    mouse.set_visible(True)
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        if Done_Button.checkClicked() == True:
            running = False

        screen.blit(credits_screen, (0, 0))

        Done_Button.drawButton(screen)
            
        display.flip()

    return "Splash Screen"

#Pause menu, accessed while playing the game
def pauseScreen():
    global mode, song, secLeft, pauseTime, score
    mouse.set_visible(True)
    mixer.pause()
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        if Done_Button.checkClicked() == True:
            running = False

        if MainMenu_Button.checkClicked() == True:
            score = 0
            return "Splash Screen"

        if Quit_Button.checkClicked() == True:
            return "exit"

        screen.blit(paused_screen, (0, 0))

        Done_Button.drawButton(screen)

        MainMenu_Button.drawButton(screen)
        Quit_Button.drawButton(screen)
        
        display.flip()

    
    mixer.unpause()
    secLeft = pauseTime
    return "Play"
    
def optionsScreen():
    global wallpaper, wallList, blade, song
    buttons = [Wall1_Button, Wall2_Button, Wall3_Button, Wall4_Button]
    wallpapers = [wall1, wall2, wall3, wall4]
    lists = [wall1List, wall2List, wall3List, wall4List]
    songs = [song1, song2, song3, song4]

    mouse.set_visible(True)

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        for button in buttons:
            if button.checkClicked() == True:
                wallpaper = wallpapers[buttons.index(button)]
                wallList = lists[buttons.index(button)]
                song = songs[buttons.index(button)]

        if Kitchen_Button.checkClicked() == True:
            blade = Blade("kitchen")

        if Fighting_Button.checkClicked() == True:
            blade = Blade("fighting")

        if Done_Button.checkClicked() == True:
            running = False 

        screen.blit(customize_screen, (0, 0))

        for button in buttons:
            if wallpaper == wallpapers[buttons.index(button)]:
                screen.blit(button.down, (button.rect.x, button.rect.y))
            else:
                button.drawButton(screen)

        if blade.blade_type == "kitchen":
            screen.blit(Kitchen_Button.down, (Kitchen_Button.rect.x, Kitchen_Button.rect.y))
        else:
            Kitchen_Button.drawButton(screen)

        if blade.blade_type == "fighting":
            screen.blit(Fighting_Button.down, (Fighting_Button.rect.x, Fighting_Button.rect.y))
        else:
            Fighting_Button.drawButton(screen)

        Done_Button.drawButton(screen)

        display.flip()

    return "Splash Screen"

def afterScreen():
    global score, oldSec, oldMin, secLeft, air, cut, wallList, oldScore
    mouse.set_visible(True)
    startCount = 0

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        startCount += 1
        if startCount >= 120:

            if PlayAgain_Button.checkClicked() == True:
                oldSec = local(clock())[5]
                oldMin = local(clock())[4]

                air = []
                cut = []
                for i in range (choice([1, 1, 2, 2, 2, 3, 3, 4, 5])):
                    air.append(Fruit(randfruit()))

                song.play()
                return "Play"

            if MainMenu_Button.checkClicked() == True:
                return "Splash Screen"

            if Quit_Button.checkClicked() == True:
                return "exit"

        screen.blit(gameover_screen, (0, 0))

        scoreBlit = largeFont.render("Score: " + str(oldScore), True, wallList[colS])
        screen.blit(scoreBlit, (950, 350))

        PlayAgain_Button.drawButton(screen)
        MainMenu_Button.drawButton(screen)
        Quit_Button.drawButton(screen)


        display.flip()

#Function for the actual game
score = 0         
def main():

    count = False
    counter = 0
    counter2 = 0

    
    global mode, song, secLeft, oldSec, oldMin, pauseTime, air, cut, score, blade, oldScore

    mouse.set_visible(False)

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        'Updating fruit positions'
        for fruit in air:
            fruit.updatePos()

        'Updating bit positions'
        for bit in cut:
            bit.updatePos()

        'Interactions'
        	#Instead, I created two "if" options: if the current second value doesn't equal the previous recorded second value OR the current second value equals
        	#the previous recorded second value however the minutes are different, then the seconds left counter should be decreased
        if local(clock())[5] != oldSec or (local(clock())[4] != oldMin and local(clock())[5] == oldSec):
        	secLeft -= 1
        	oldSec = local(clock())[5] 
        	oldMin = local(clock())[4]

        if secLeft <= 0:
            endScore = score
            running = False

        if count == True:
            counter += 1
        if count == False:
            counter = 0

        if counter >= choice ([10, 20, 20, 30, 30, 30, 50, 50, 100, 100, 100, 200, 200, 300]):
            for i in range (choice([1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5])):
                air.append(Fruit(randfruit()))
                count = False
        #this randomly adds more fruit to the "air" list after an interval of time
        counter2 += 1
        if counter2 >= choice ([100, 100, 100, 200, 200, 300, 300, 400]):
            for i in range (choice([1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5])):
                air.append(Fruit(randfruit()))
                counter2 = 0

        #Determines what the current high score is
        if oldHS > score:
            highscore = oldHS
        else:
            highscore = score

        'Checking for collision'
        for fruit in air:
            if fruit.checkCollide() == True:
                fruit.makeSound()
                if blade.blade_type == "kitchen":
                    point = choice ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10])
                    score += point
                else:
                    point = choice ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10])         #The fighting blade gives a higher change of getting 10 points on a slice (user doesn't need to know)
                    score += point
                del air[air.index(fruit)]
                cut.append(Bits(fruit.fruit_type, fruit.x, fruit.y, fruit.angle, fruit.vy))
                count = True

        'Checking if buttons are clicked'
        if Pause_Button.checkClicked() == True:
            pauseTime = secLeft
            return "Pause"

        'Deleting fruits from air list if they are off the screen'
        for fruit in air:
            if fruit.y > height:
                del air[air.index(fruit)]

        '''Drawing'''
        screen.blit(wallpaper, (0, 0))

        for fruit in air:
            fruit.drawFruit(screen)

        for bit in cut:
            bit.drawBits(screen)

        Pause_Button.drawButton(screen)

        blade.drawBlade(screen, mp())

        if secLeft % 10 == 0 or secLeft <= 9:
            timeCol = (255, 23, 34)
        else:
            timeCol = wallList[colT]
        secBlit = medFont.render(str(secLeft), True, timeCol)
        screen.blit(secBlit, (width//2 - (secBlit.get_width()//2), 15))

        #Current Score
        scoreBlit = largeFont.render(str(score), True, wallList[colS])
        screen.blit(scoreBlit, (50, 15))

        #High Score
        highBlit = smallFont.render("High Score: " + str(highscore), True, wallList[colHS])
        screen.blit(highBlit, (50, 88))

        #FPS
        fpsBlit = smallFont.render("FPS: " + str(fps.get_fps())[0:2], True, wallList[colFPS])
        screen.blit(fpsBlit, (1190, 15))

        display.flip()

    mouse.set_visible(True)
    mixer.stop()

    oldScore = score
    score = 0
    secLeft = 60

    return "After"

#Two second loading screen at the start of the program, I added this simply for effect
    #If the user presses enter or space it is skipped (like in a real game)
def loadingScreen():
    loadCount = 0
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                quit()
                raise SystemExit        

        keys = key.get_pressed()

        screen.blit(load_screen, (0, 0))

        if keys[K_RETURN] or keys[K_SPACE]:
                running = False

        loadCount += 1 
        if loadCount >= 120:
                running = False

        display.flip()
        fps.tick(60)
        
    return None

loadingScreen()

#Main game loop

while mode != "exit":        
                                    
    if mode == "Splash Screen":
        mode = splashScreen()

    elif mode == "Play":
        mode = main()

    elif mode == "Pause":
        mode = pauseScreen()

    elif mode == "Credits":
        mode = creditsMenu()

    elif mode == "Options":
        mode = optionsScreen()

    elif mode == "Options_Customize":
        mode = customizeScreen()

    elif mode == "After":
        mode = afterScreen()

#Writing the new high score to file if it is higher than the current high score
if highscore > oldHS:
    highFile = open("Untitled.txt", "w")
    highFile.write(str(highscore))

font.quit()
mixer.quit()
quit()
