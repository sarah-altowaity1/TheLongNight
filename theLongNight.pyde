add_library('minim')
import random, os, math
path = os.getcwd()
player = Minim(this)
# Set game dimensions as global variables.
WIDTH = 1280
HEIGHT = 720 
GROUND = 250
# The reason why sound booleans are global is to preserve the player's sound preferences throughout the duration of the program's execution, 
# through multiple instantiations of the game object.
playMusic = True 
playSound = True
# Sets the number of levels with the consideration that the last level will be against the Night King (NK).
LEVELS = 1
typing = "" # Is used to display the action of dynamic user input.
# These multiple deictionaries make it easier to change, store, and access all the images and sounds the program uses.
ANIMATION = {"Jon Walking": loadImage(path+"/images/jonSnowWalk.png"), "Jon Shooting": loadImage(path+"/images/jonSnowShoot.png") , "White Walker Walking": loadImage(path+"/images/whiteWalkerWalk.png"),
             "Smoke Animation": loadImage(path + "/images/smokeAnimation.png" ), "Night King Shooting": loadImage(path+"/images/nightKingShoot.png") , "Arrow": loadImage(path+"/images/Arrow.png"),
              "Night King Walking": loadImage(path+"/images/nightKingWalk.png"), "Spear": loadImage(path+"/images/Spear.png")}
GRAPHICS = {"Jon Snow Icon": loadImage(path + "/images/jonSnowIcon.png"), "White Walker Icon": loadImage(path + "/images/WhiteWalkerIcon.png"), "Night King Icon": loadImage(path + "/images/nightKingIcon.png"), 
            "Arrows Icon": loadImage(path + "/images/ArrowsIcon.png"), "Heart Icon": loadImage(path + "/images/heartIcon.png"),  "Sound Icon": loadImage(path + "/images/SoundIcon.png"), 
            "Music Icon": loadImage(path + "/images/MusicIcon.png")}
SCENES = {"Game Scene": loadImage(path+"/images/background.png"), "Intro Scene":  loadImage(path + "/images/Intro-TheLongNight.png"), "Instructions Scene": loadImage(path + "/images/Instructions.png"), 
          "Leaderboard Scene": loadImage(path + "/images/leaderboardScene.png")}
SOUNDS = {"Win" : player.loadFile(path + "/sounds/win.mp3"),"BG Music" : player.loadFile(path + "/sounds/backgroundMusic.mp3"), "Click" : player.loadFile(path + "/sounds/Click.mp3"), 
          "Shooting" : player.loadFile(path + "/sounds/fireBow.mp3"), "Death Screech": player.loadFile(path + "/sounds/deathScreech.mp3"), 
          "Bonus Item" : player.loadFile(path + "/sounds/insertDing.mp3"), "Footsteps": player.loadFile(path + "/sounds/footstepsOnSnow.mp3")}


# Create a Character superclass from which all subsequent character classes are to inherit.
class gameCharacter():
    def __init__(self, x, y, sradius, lradius, speed, img, img_w, img_h, num_frames, dir):
        self.x = x
        self.y = y 
        self.sradius = sradius
        self.lradius = lradius
        self.img_w = img_w
        self.img_h = img_h
        self.img = img
        self.frame = 0
        self.num_frames = num_frames
        self.speed = speed
        self.dir = dir
        self.footstepsSound = SOUNDS["Footsteps"]


    def update(self):  # Updates the position of the character.
        self.y += self.vy
        self.x += self.vx
        
        
    def display(self):
       self.update() # Call the update method so that changes in character locations are displayed.
       # Flips the image horizontally (mirrors the image across a vertical line to change the animation depending on the direction the character is taking).
       if self.dir == RIGHT:  # Display animation with changes in character position every frame.
           image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
       elif self.dir == LEFT:
           image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w , 0 , self.frame * self.img_w, self.img_h)
           
           
# Create the main character class that inehrits from the Character superclass.
class JonSnow(gameCharacter):
    def __init__(self, x, y, sradius, lradius, speed, img, img_w, img_h, num_frames, dir):
        gameCharacter.__init__(self,  x, y, sradius, lradius, speed, img, img_w, img_h, num_frames, dir)
        self.projectile_released = False
        # Initialize a dictionary attribute to control user-controlled character movements
        self.key_handler = {UP: False, DOWN: False, RIGHT: False, LEFT: False}
        self.dead = False
        self.total_arrows = 15
        self.quiver = [Projectile(self.x, self.y, 80, 15,  ANIMATION["Arrow"], self.dir) for i in range(self.total_arrows)]
        self.bow = [] 
        self.shootingAnimation = ANIMATION["Jon Shooting"]
        self.shootingSound = SOUNDS["Shooting"]
        self.shootingFrames = 10
        self.walkingAnimation = self.img
        self.arrow_bar = StatsBar(120, self.total_arrows, 1130, 150, GRAPHICS["Jon Snow Icon"], 980, 110, GRAPHICS["Arrows Icon"], 1100, 140, color(43, 240, 48)) 
        self.lives = 0 # This attribute is incremented or decremented when Jon collects "life" bonus items and when he is touched or attacked by the Night King in the last level; respectively.
     
     
    def update(self):
        # Player-controlled movement of Jon Snow with limitations that is controlled based on the screen dimensions. 
        if self.key_handler[UP] == True and self.y > GROUND - self.lradius:
            self.vy = -1 * self.speed
        elif self.key_handler[DOWN] == True and self.lradius + self.y < HEIGHT:
            self.vy = self.speed
        elif self.key_handler[RIGHT] == True and self.x + self.sradius < WIDTH:
            self.vx = self.speed
        elif self.key_handler[LEFT] == True and self.x - self.sradius > 0:
            self.vx = -1 * self.speed
        else:
            self.vy = 0
            self.vx = 0
            
        # To display the standing animation when Jon is not walking nor shooting.
        if self.vx == 0 and self.vy == 0 and self.img != self.shootingAnimation:
            self.frame = 0

        # Increment Jon's position by the vertical and horizontal speeds as long as the movement will not move Jon out of the screen.
        if GROUND - self.lradius < self.y + self.vy < HEIGHT - self.lradius:
             self.y += self.vy
        if self.sradius < self.x + self.vx < WIDTH - self.sradius:
            self.x += self.vx
        
        # Slow down walking animation.
        if frameCount% 3 == 0 and (self.vy != 0 or self.vx != 0):
            # Play footstep marching sound when changing the frames of the walking animation if the player has not muted sounds. 
            if playSound: # Play marching sound is sounds are on.
                self.footstepsSound.rewind() 
                self.footstepsSound.play()
            self.frame = (self.frame + 1) % self.num_frames
        
        # Call the shoot method to check if a projectile is released and to remove a projectile from the quiver and place it in the bow in prepararation for shooting.
        self.shoot()
        # If the bow list is not empty, we call the diplay method of every arrow in the bow list, which in turn propels the arrows based on the shooting position.
        # Check if there was any collision between any walker in the game.enemies list and remove the arrow, then remove the walker after the smoke animation is played.
        if self.bow != []:
            for arrow in self.bow: # Display arrows that are shot.
                arrow.display()
                for e in game.enemies: 
                    if arrow.collide(e) and arrow in self.bow and e.img != e.smokeAnimation: # Jon cannot strike a walker whose "dying" (if the walker's animation is the smoke sprite).
                        self.bow.remove(arrow)
                        e.disappear() # Changes animation to smoke; plays a death screech if sounds are on.
                        game.score += 10 * game.currentLevel
                        break
            # Remove the arrow from the bow if the arrow has travelled outside the screen.
                if arrow.x > WIDTH or arrow.x < 0:
                    if arrow in self.bow:
                        self.bow.remove(arrow)        
            
            
        # Check if Jon collided with any "alive", walking walker in the game, at which point Jon's dead attribute is set to True.
        for e in game.enemies:
            if self.collide(e) and e.img!=  e.smokeAnimation:
                self.dead = True 
                if self.lives > 0: # Resurrect Jon from the dead if he has lives.
                    self.lives -= 1
                    self.dead = False
                    self.x, self.y = WIDTH//2, GROUND # Reset Jon's position to the middle of the screen.
                    break
                
                
        # If the space bar is pressed, display the shooting animation until all shooting frames have been displayed, at which point, the animation is set back to the walking 
        # animation.
        if self.img == self.shootingAnimation and self.frameShooting > 0:
            if self.dir == RIGHT:  # Display animation with changes in character position every frame.
                image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
            elif self.dir == LEFT:
                image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w , 0 , self.frame * self.img_w, self.img_h)
            self.frameShooting -= 1
        # Reset image to the waliking animation after the shooting animation is over (self.frameShooting == 0); reset the frameShooting attribute back to its original value for 
        # the next time it is to be played.
        else:
            self.img = self.walkingAnimation
            self.frameShooting = 10


    # Determine a collision. 
    def collide(self, target):
        # Subtracted 15 pixels to offset the extra no fill pixels the animations have so that collisions look more natural.
        if math.sqrt((target.x - self.x)**2 + (target.y - self.y)**2) <= (self.sradius + target.sradius) - 15: 
            return True
        # Since Jon and the walkers are ellipses, we need a condition that detects their collision when they vertically overlap.
        elif target.x - target.sradius < self.x < target.x + target.sradius:
            if abs(self.y - target.y) <= (self.lradius + target.lradius):
                return True
        
        
    # This method checks if the space bar has been pressed.
    def shoot(self):
        if self.projectile_released:
            self.img = self.shootingAnimation # Change the animation from walking to shooting. 
            
        # If Jon has arrows, an arrow is taken from his quiver and put into the bow, and the number of total arrows he has is decremented by 1. Jon can only shoot when his bow list is empty to avoid
        # having Jon lose all his arrows with one space bar press.
        if self.quiver != []  and self.bow == [] and self.projectile_released:
            arrow = self.quiver.pop()
            arrow.x =  self.x
            arrow.y = self.y
            arrow.dir = self.dir
            self.bow.append(arrow)
            self.total_arrows -= 1
           
           
# Create a WhiteWalker class that inherits from the gameCharacter class.
class WhiteWalker(gameCharacter):
    def __init__(self, x, y, sradius, lradius, speed, img, img_w, img_h, num_frames, dir):
        gameCharacter.__init__(self, x, y, sradius, lradius, speed, img, img_w, img_h, num_frames, dir)
        self.smokeAnimation = ANIMATION["Smoke Animation"]
        self.smokeAnimFrames = 12
        self.deathScreech =  SOUNDS["Death Screech"]
        # This attribute will partially determine whether a bonus item will be instantiated after a walker is killed. 
        self.hasBonus = random.choice([True, False, False]) # This makes it less likely that there are bonus items.
        
        
    def update(self, target):
        if self.img ==  self.smokeAnimation: # If the walker is "dying",
            frames = self.smokeAnimFrames - 1 # Create a local variable to be used in the condition of removing the walker from the game.
            if frameCount % 3 == 0:
                self.frame = (self.frame + 1) % self.num_frames # Display the animations.
                self.speed = 0 # Stop the walker from advancing.
                if self.frame == frames: # If the smoke animation has been displayed, remove the walker from the list holding the enemies in the game object.
                    game.enemies.remove(self)
                    # If a walker was initialized with a bonus that Jon will be capable of colliding with (it is within his range of movement), a BonusItem is instantiated.
                    if self.hasBonus and self.sradius < self.x < WIDTH - self.sradius and self.sradius + GROUND < self.y < HEIGHT - self.sradius: 
                        b = BonusItem(self.x, self.y, 20)
                        game.bonusItems.append(b)
        else:          
            # Have the white walkers follow Jon.
            if self.x > target.x:
                self.x -= self.speed
                if self.x != target.x and self.x - self.speed > target.x: # This condition prevents a fast change in direction (will look like the walker is confused) caused by position overshooting.
                    self.dir = LEFT # Change the direction of the walker based on Jon's location so that the walker is always facing Jon.
            elif self.x < target.x:
                self.x += self.speed
                if self.x != target.x and self.x + self.speed < target.x:  # This condition prevents a fast change in direction (will look like the walker is confused) caused by position overshooting.
                    self.dir = RIGHT # Change the direction of the walker based on Jon's location so that the walker is always facing Jon.

            if self.y < target.y:
                self.y += self.speed
            elif self.y > target.y:
                self.y -= self.speed

            if frameCount % 5 == 0:
                self.frame = (self.frame + 1) % self.num_frames

    
    def display(self, target):  # Display animation with changes in character position every frame.
        self.update(target)
       # Flips the image horizontally (mirrors the image across a vertical line to change the animation depending on the direction the character is taking.
        if self.dir == RIGHT: 
           image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
           image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w , 0 , self.frame * self.img_w, self.img_h)
     
     
    # This method changes the display image of the walker to a smoke sprite and plays a death screech sound if sounds are on. Called when Jon Projectile kills a walker.
    def disappear(self):
          self.img = self.smokeAnimation
          self.frame = 0
          if playSound:
            self.deathScreech.rewind()
            self.deathScreech.play()


# Create a NightKing class that also inherits from the gameCharacter class.
class NightKing(gameCharacter):
    def __init__(self, x, y, sradius, lradius, speed, img, img_w, img_h, num_frames, dir):
        gameCharacter.__init__(self, x, y, sradius, lradius, speed, img, img_w, img_h, num_frames, dir)
        self.health_units = 15
        # NK's StatsBar object will be a measure of his health.
        self.health_bar = StatsBar(120, self.health_units, 1130, 50, GRAPHICS["Night King Icon"], 980, 20, GRAPHICS["Heart Icon"], 1080, 40, color(173, 38, 9))
        self.deathScreech =  SOUNDS["Death Screech"]
        self.shooting_probability = 0.4
        self.time_gap = 4000
        self.start_time = millis()
        self.bullets = []
        self.dead = False
        self.walkingAnimation = self.img
        self.shootingAnimation = ANIMATION["Night King Shooting"]
        self.frameShooting = 8
    
    
    # Have NK follow Jon as well.
    def update(self, target):
        if self.x > target.x:
            self.x -= self.speed
            if self.x != target.x and self.x - self.speed > target.x:
                self.dir = LEFT
        elif self.x < target.x:
            self.x += self.speed
            if self.x != target.x and self.x + self.speed < target.x:
                self.dir = RIGHT

        if self.y < target.y:
            self.y += self.speed
        elif self.y > target.y:
            self.y -= self.speed


        self.shoot() # Appends a Spear object to NK's bullet list if conditions are met.
        if self.bullets != []:
            for bullet in self.bullets:
                bullet.display()
                if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT: # Remove the Spear object if it travelled beyond the screen.
                    self.bullets.remove(bullet)
                if bullet.collide(game.jon): # If Spear object collides with Jon,
                    self.bullets.remove(bullet) # Remove Spear from display.
                    game.jon.dead = True # Set Jon object's dead attribute to True.
                    if game.jon.lives > 0: # If Jon has lives, decrement his lives attribute and resurrect him in the middle of the screen on the GROUND.
                        game.jon.lives -= 1
                        game.jon.x, game.jon.y = WIDTH//2, GROUND 
                        game.jon.dead = False # Ensure the game is still not lost by reseting Jon's dead attribute back to False.
                    break


        for a in game.jon.bow: 
            if a.collide(self) and self.health_units > 0: # Decrement NK's health if Jon strikes him.
                self.health_units -= 1
                # Increment the score by 20. The score incrementation here is fixed regardless of the game.currentLevel, since the difficulty of this level is the same whether the game had only 3 levels or 10.
                game.score += 20 
                game.jon.bow.remove(a) # Remove jon's arrow from the bow (and from display) if it strikes NK.
        
        
        if self.collide(game.jon): # The collision between NK (not his Spear) and Jon is similar to that between a walker and Jon.
            game.jon.dead = True
            if game.jon.lives > 0:
                game.jon.lives -= 1
                game.jon.dead = False
                game.jon.x, game.jon.y = WIDTH//2, GROUND
            
            
        if self.health_units == 0: # NK dies when his health is 0.
            self.dead = True # This attribute will be used to declare a game win.
            if playSound:
                self.deathScreech.rewind()
                self.deathScreech.play()
            
            
        # Display shooting animation when the img is the shooting img and if the frames have not been displayed in their entirety
        if self.img == self.shootingAnimation and self.frameShooting > 0:
            if self.dir == RIGHT:  # Display animation with changes in character position every frame.
                image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
            elif self.dir == LEFT:
                image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w , 0 , self.frame * self.img_w, self.img_h)
            self.frameShooting -= 1 # decrement self.frameShooting with every frame displayed.
            
        else:
            self.img = self.walkingAnimation # Once all the frames have been displayed, reset img and frameShooting to their default values.
            self.frameShooting = 10
            
            
    def collide(self, target):
        # Subtracted 30 pixels to offset the extra no fill pixels the animations have so that collisions look more natural.
        if math.sqrt((target.x - self.x)**2 + (target.y - self.y)**2) <= (self.sradius + target.sradius) - 30: 
            return True
    
    
    def shoot(self): 
        self.fire_chance = random.random() # Randomly generate a real number between 0 and 1. This adds randomness to NK's shooting.
        # NK will shoot only if the chance is less than or equal to the probability and if at least 4 seconds have passed since the last Spear shot and if his bullets list is empty.
        if self.fire_chance <= self.shooting_probability and millis() - self.start_time > self.time_gap and self.bullets == []:
            self.bullets.append(Spear(self.x, self.y, 150, 24, ANIMATION["Spear"], self.dir)) # Append the Spear to his list of bullets.
            self.speed += 0.05 # Increment his speed with every spear shot so that it gets more difficult to evade him.
            self.img = self.shootingAnimation # Change animation to shooting animation.
            self.start_time = millis() # Re-clock the start time so that the next 4 seconds are second when NK will not be shooting.

    
    def display(self, target):
        self.update(target) # Call the update method so that changes are displayed.
       # Flips the image horizontally (mirrors the image across a vertical line to change the animation depending on the direction the character is taking).
        if self.dir == RIGHT: 
           image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
           image(self.img, self.x - self.img_w //2, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w , 0 , self.frame * self.img_w, self.img_h)
        if frameCount % 5 == 0:
            self.frame = (self.frame + 1) % self.num_frames
  

# Create a Projectile class from which Jon's arrows are to be instantiated
class Projectile():
    def __init__(self, x, y, w, h, img, dir):
        self.dir = dir
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.shot = False
        self.vx = 10
        self.angle = 0


    # Jon's arrows, unlike NK's spear, can only move in a vertical fashion.
    def move(self):
        # Direction of the arrow will depend on Jon's direction
        if self.dir == RIGHT:  
            self.x += self.vx # Add vertical velocity to position if projectile is supposed to go right.
        if self.dir == LEFT:
            self.x += (self.vx * -1) # Subtract vertical velocity from position if projectile is supposed to go left.
           
           
    def display(self):
        self.move() # Call the .move() method so that changes to location are displayed on the screen.
        # Flips the image horizontally (mirrors the image across a vertical line to change the animation depending on the direction the projectile is taking.
        if self.dir == RIGHT:
            image(self.img, self.x, self.y, self.w, self.h)
        elif self.dir == LEFT:
            image(self.img, self.x - self.w, self.y,  self.w, self.h,self.w, 0, 0, self.h)
    
    
    # This method will be used to detect a collision between Jon's arrows and the walkers.
    def collide(self, target):
        if target.x - target.sradius <= self.x <= target.x + target.sradius and  target.y - target.lradius  <= self.y <= target.y + target.lradius:
            return True


# Create a Spear class that inherits from the Projectile class for the Spear objects NK will use to attempt to kill Jon.
class Spear(Projectile):
    def __init__(self, x, y, w, h, img, dir):
        Projectile.__init__(self, x, y, w, h, img, dir)
        self.speed = 10
        self.targetX = game.jon.x
        self.targetY = game.jon.y
        # Use trigonometry to determine the direction of the spear
        # Use exception handling in case NK and Jon are in the same position (If they are, we will get a ZeroDivisionError when trying to find the angle).
        try:
            self.angle = math.atan((self.targetY-self.y)/(self.targetX-self.x))
        
            if self.x > self.targetX and self.y > self.targetY:
                self.angle = self.angle + math.pi
            elif self.x < self.targetX and self.y > self.targetY:
                self.angle = self.angle
            elif self.x > self.targetX and self.y < self.targetY:
                self.angle = self.angle + math.pi
            elif self.x < self.targetX and self.y < self.targetY:
                self.angle = self.angle + 2 * math.pi
        # We know that arctan(x) is undefined when cos(x). That happens when the angle is either half pi or 3 pi over 2.
        except ZeroDivisionError: 
            if self.y > self.targetY:
                self.angle = (math.pi/2)
            elif self.y < self.targetY:
                self.angle = (3 * math.pi)/2 
        
    # Get the velocity vector (vx, vy) by using trignometric relationships and normalizing it by mutliplying cos(self.angle) or sin(self.angle) by the speed.
    def move(self):
        vx, vy = math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed
        if self.angle == (math.pi/2):
            vx, vy = 0, -1 * self.speed
        elif self.angle == (3*math.pi/2):
            vx, vy = 0, 1 * self.speed
        self.x += vx
        self.y += vy

    # Use image manipulation to rotate the image about its upper left corner by the angle formed between the Spear object and the target:
    def display(self):
            self.move()
            pushMatrix() 
            translate(self.x, self.y) # Change the origin from (0,0) to the upper left corner of the object.
            rotate(self.angle) # Rotate the image about the new origin.
            image(self.img, 0, 0, self.w, self.h) # Display the image.
            translate(0,0) # Restore to default setting.
            rotate(0)
            popMatrix()
        
        
# Create a StatsBar class that tracks player performance.
class StatsBar():
    def __init__(self, bar_length, max_amount, bar_x, bar_y, icon1, icon1_x, icon1_y, icon2, icon2_x, icon2_y, bar_color):
        self.max_amount = max_amount
        self.bar_length = bar_length 
        self.unit = bar_length / self.max_amount
        # self.current_amount = current_amount
        self.bar_x = bar_x
        self.bar_y = bar_y
        self.icon1 = icon1
        self.icon2 = icon2
        self.icon1_x = icon1_x
        self.icon1_y = icon1_y
        self.icon2_x = icon2_x
        self.icon2_y = icon2_y
        self.bar_color = bar_color
        
        
    # Have the display method take a current amount arguement that will be used to modify the length of the bar
    def display(self, current_amount):
        self.current_amount = current_amount
        noStroke()
        fill(self.bar_color)
        rect(self.bar_x, self.bar_y, self.bar_length - ((self.bar_length/self.max_amount) * (self.max_amount - self.current_amount)), 10)
        stroke(0, 0, 0)
        strokeWeight(1)
        noFill()
        rect(self.bar_x, self.bar_y, self.bar_length, 10) 
        image(self.icon1, self.icon1_x, self.icon1_y, 70, 70) 
        image(self.icon2, self.icon2_x, self.icon2_y, 50, 50)
        
        
# Create a BonusItem class whose objects will be instantited if Jon kills a walker with True as their hasBonus attribute and if the walker is within the necessary frame.
class BonusItem():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.images = {"arrow": loadImage(path + "/images/ArrowBonus.png"), "life": loadImage(path + "/images/RedWomanIcon.png")}
        self.ding = SOUNDS["Bonus Item"]
        self.randomNum = random.choice([1,1,1,2,2,2,3,3]) # This makes it less likely to get an item that is worth 3 things (3 lives or 30 points)
        # This makes it less likely to get life as compared to arrows or life
        self.type = random.choice([("arrow", self.randomNum),("arrow", self.randomNum),("life", 1), ("points", self.randomNum * 10), ("points", self.randomNum * 10), ("points", self.randomNum * 10)]) 
        
        
    def display(self):
        # Display the item as a circle with a specific color that indicates its type and an image if applicable.
        noStroke()
        if self.type[0] == "arrow":
            fill(253,253,150)
            ellipse(self.x + self.radius, self.y, 2 * self.radius, 2 * self.radius)
            image(self.images["arrow"], self.x, self.y)
        elif self.type[0] == "life":
            fill(255, 0, 0)
            ellipse(self.x + self.radius, self.y, 2 * self.radius, 2 * self.radius)
            imageMode(CENTER)
            image(self.images["life"], self.x + self.radius, self.y, 150, 150)
            imageMode(CORNER)
        elif self.type[0] == "points":
            fill(0, 128, 255)
            ellipse(self.x + self.radius, self.y, 2 * self.radius, 2 * self.radius)
        fill(0)
        textSize(10)
        textAlign(CENTER)
        text("+"+ str(self.type[1]), self.x + self.radius, self.y)
        textAlign(LEFT)
        # This condition outlines what happens if Jon collides with an item.
        if self.collide(game.jon):
            if playSound:
                self.ding.rewind()
                self.ding.play()
            game.bonusItems.remove(self) # Remove the item from the list in the game object that stores all bonus items in the game.
            if self.type[0] == "arrow": # If the type is arrow and Jon needs arrows and the item's quantity when added to Jon's quiver does not exceed the maximum quantity Jon can have at any moment,
                if self.type[1] + len(game.jon.quiver) <= game.jon.arrow_bar.max_amount:
                    for i in range(self.type[1]): # Instantiate a new Projectile object and append it to Jon's quiver.
                        game.jon.quiver.append(Projectile(game.jon.x, game.jon.y, 80, 15, ANIMATION["Arrow"], game.jon.dir))
                elif (game.jon.arrow_bar.max_amount - len(game.jon.quiver)) < self.type[1]: # If the quantity of the arrows needs only a fraction of the quantity,
                    i = game.jon.arrow_bar.max_amount - len(game.jon.quiver) # Only that number of arrows that Jon needs will be appended to his quiver.
                    for i in range(i):
                        game.jon.quiver.append(Projectile(game.jon.x, game.jon.y, 80, 15, ANIMATION["Arrow"], game.jon.dir))

            elif self.type[0] == "life": # If Jon claims an extra life, he gets to be "resurrected"; his lives attribute is incremented by 1.
                game.jon.lives += self.type[1]
            elif self.type[0] == "points":
                game.score += self.type[1] # If Jon claims extra points, the score attribute of the game is incremented by that number.

    
    def collide(self, object): # This method detects a collision between the item and another object.
        if math.sqrt((self.x - object.x)**2 + (self.y - object.y)**2) <= (object.sradius + self.radius):
            return True
            

class Game():
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.jon = JonSnow(WIDTH//2, GROUND, 32, 64, 5, ANIMATION["Jon Walking"], 64, 128, 10, RIGHT)
        self.jon_icon = GRAPHICS["Jon Snow Icon"]
        self.enemy_icon = GRAPHICS["White Walker Icon"]
        self.arrow_icon = GRAPHICS["Arrows Icon"]
        self.heart_icon = GRAPHICS["Heart Icon"]
        self.gameSpeed = 0.5 # Speed of the walkers
        self.num_enemies = 15 # Number of walkers instantiated at the beginning of the game.
        self.enemies = []
        self.scene = SCENES["Game Scene"]
        self.army_health = StatsBar(120, self.num_enemies, 1130, 50, GRAPHICS["White Walker Icon"], 980, 20, GRAPHICS["Heart Icon"], 1080, 40, color(104, 215, 247))
        self.crosshair = loadImage(path +"/images/crosshair.png")
        self.backgroundMusic = SOUNDS["BG Music"]
        self.buttonClick = SOUNDS["Click"]
        self.win_sound = SOUNDS["Win"]
        self.bonusItems = []
        self.barWidth = 120
        # These attributes determine which screen to be displayed.
        self.displayIntro = True
        self.displayHighScores = False
        self.displayInstructions = False
        self.gameOn = False
        self.currentLevel = 1
        self.introImage = SCENES["Intro Scene"]
        self.instructionsImage = SCENES["Instructions Scene"]
        self.leaderboardImage = SCENES["Leaderboard Scene"]
        if playMusic: # Game object will play a sound upon instantiation only if global variable playMusic is True.
            self.backgroundMusic.rewind()
            self.backgroundMusic.loop()
        self.musicIcon =  GRAPHICS["Music Icon"]
        self.soundIcon = GRAPHICS["Sound Icon"]
        self.nightKing = NightKing(random.randint(0,WIDTH), (3/2)*HEIGHT, 82.5, 110, 0.5, ANIMATION["Night King Walking"], 165, 220, 5, LEFT) # NK instantiated at a random x location.
        # Since there are both losing and winning conditions, we initialize them as boolean attributes with every new Game object.
        self.won = False
        self.lost = False
        self.score = 0
    
    
    # What the display method, which is called from the draw function every frame, depends on certain game conditions.
    def display(self):
        # Check loss.
        self.check_loss()
        # If the game is lost or won, a certain text is displayed accordingly.
        if self.lost or self.won: 
            image(self.scene,0, 0)
            if self.lost and len(self.enemies) > 1 and len(self.jon.quiver) == 0 and len(self.jon.bow) == 0 and len(self.bonusItems) == 0:
                fill(255,0,0)
                textSize(20)
                textAlign(CENTER)
                text("You ran out of arrows!", WIDTH//2, HEIGHT//2 - 40)
                textAlign(LEFT)
            fill(0, 0, 0)
            textSize(20)
            textAlign(CENTER)
            if self.lost:
                text("Game over. The army of the dead wins.", WIDTH//2, HEIGHT//2)
                fill(255,0,0)
            elif self.won:
                text("Good Job! You are the true protector of the Seven Kingdoms!", WIDTH//2, HEIGHT//2)
                fill(255,0,0)
            text("Input name then enter: " + typing,  WIDTH//2 - 40, HEIGHT//2 + 40)
            text("Or press anywhere on the screen to continue", WIDTH//2, HEIGHT//2 + 80)
            textAlign(LEFT)
            return
            
        if self.displayIntro: # Display intro scene if the game is instantiated for the first time or if a back button is clicked.
            self.introScene()
        
        if self.displayInstructions:  # Display intstructions scene if the "INSTRUCTIONS" button is clicked.
            self.instructionsScreen()
            
        if self.displayHighScores: # Display leaderboard scene if the "HIGH SCORES" button is clicked.
            self.highScoresScreen()
                            
        if self.gameOn and self.currentLevel < LEVELS: # If gameOn (not Paused) and the level is not the last, call the level() method.
            self.level()
        if self.gameOn and self.currentLevel == LEVELS: # If gameOn (not Paused) and the level is not the last, call the lastLevel() method, that starts the battle with NK.
            self.lastLevel()
            
        if not self.displayIntro: # Display game features during game time.
            self.displayScreenFeatures() 
        
    def introScene(self):
        image(self.introImage, 0, 0) # Display intro scene.
        textSize(30)
        stroke(65,65,65)
        strokeWeight(2)
        # Buttons change colors depending on sound pereference.
        if not playMusic:
            fill(255,10,0)
        else:
            fill(0, 250 , 200)
        rect(100, 650, 50, 50)
        image(self.musicIcon, 103,655)
        if not playSound:
            fill(255,10,0)
        else:
            fill(0, 250 , 200)
        rect(160, 650, 50, 50)
        image(self.soundIcon, 165,660)
        # Display intro buttons.
        if 100 <= mouseX <= 300 and 550 <= mouseY <= 600: 
            fill(0, 255, 0)
        else:
            fill(255,192,203)
        rect(100, 550, 200, 50)
        fill(29,41,81)
        text("HIGH SCORES", 103 , 590)
 
        if 950 <= mouseX <= 1150 and 550 <= mouseY <= 600:
            fill(0, 255, 0)
        else:
            fill(255,192,203)
        textSize(25)
        rect(950, 550, 200, 50)
        fill(29,41,81)
        text("INSTRUCTIONS", 960 , 590)
        
        if 530 <= mouseX <= 730 and 650 <= mouseY <= 700:
            fill(0, 255, 0)
        else:
            fill(255,192,203)
        textSize(30)
        rect(530, 650, 200, 50)
        fill(29,41,81)
        text("NEW GAME", 550 , 685)
    
    
    def level(self): # This is the method that controls the levels without NK.
        if self.enemies == []: # If the enemies list is empty (either at the beginning of the game or when Jon completes a level), 
            # Spawn whites. Note: the gameSpeed and num_enemies will be incremented with each level, so that there's an increase in difficulty.
            # Second note: enemies are instantiated off screen so they may take some time to appear.
            self.enemies = self.spawnWhites(self.gameSpeed, self.num_enemies) 
        image(self.scene, 0, 0) # Display background.
        # Display game information (level, lives, and score).
        fill(255,0,0)
        textSize(15)
        text("Level " + str(self.currentLevel), WIDTH - len("Level " + str(self.currentLevel)) * 15 , 30)
        text("Lives: " + str(self.jon.lives), WIDTH - len("Lives: " + str(self.jon.lives)) * 25, 30)
        text("Score: " + str(self.score), WIDTH//2, 30)
        
        if self.bonusItems != []: # Display bonus items if there are any.
            for item in self.bonusItems:
                item.display()
                    
        self.jon.display() # Display Jon.
        self.jon.arrow_bar.display(len(self.jon.quiver)) # Update the current amount of his StatsBar so that it conveys accurate information.
            
        for e in self.enemies:
            e.display(self.jon) # Display walkers.
        self.army_health.display(len(self.enemies)) # Update the current amount of the army StatsBar so that it conveys accurate information.
 
        if self.enemies == []: # If Jon kills all enemies.
            self.jon.x, self.jon.y = WIDTH//2, GROUND # Jon's location is reset to the default position, in preparation for the subsequent level.
            self.jon.total_arrows = 20  # Jon's quiver is given an extra 20 arrows every level.
            self.jon.quiver = [Projectile(self.jon.x, self.jon.y, 80, 15, ANIMATION["Arrow"], self.jon.dir) for i in range(self.jon.total_arrows)]
            self.currentLevel += 1 # current level is updated.
            self.gameSpeed += 0.35 # Speed of the walkers increases every level.
            self.num_enemies += 7
            self.army_health.max_amount = self.num_enemies # Max amount for the army's StatsBar is also updated so that it conveys accurate information.
            self.jon.arrow_bar.max_amount = len(self.jon.quiver) # Max amount for Jon's StatsBar is also updated so that it conveys accurate information.
            delay(500)
            
            
    def lastLevel(self): # This is the method that controls the last level.
        image(self.scene,0, 0)
        fill(255,0,0)
        textSize(15)
        text("Level " + str(self.currentLevel), WIDTH - len("Level " + str(self.currentLevel)) * 15, 30) # Display game information.
        text("Lives: " + str(self.jon.lives), WIDTH - len("Lives: " + str(self.jon.lives)) * 25, 30)
        text("Score: " + str(self.score), WIDTH//2, 30)
        if self.bonusItems != []: # Display bonus items
            for item in self.bonusItems:
                item.display()
        self.jon.display() # Display Jon.
        self.jon.arrow_bar.display(self.jon.total_arrows) # Display Jon's StatsBar object.
        self.nightKing.display(self.jon) # Display NK
        self.nightKing.health_bar.display(self.nightKing.health_units) # Display NK's StatsBar object.
        if self.nightKing.dead == True:  # If NK is dead, then the game is won.
            self.won = True
            if playSound:
                self.win_sound.rewind()
                self.win_sound.play()
            
            
    # This method displays the instructions page and the back buttons.
    def instructionsScreen(self): 
        image(self.instructionsImage, 0, 0)
        if 50 <= mouseX <= 110 and 50 <= mouseY <= 80: # Change the color of the back button if the player's mouse lands on it.
             fill(0, 255, 0)
        else:   
            fill(255,192,203)
        stroke(255,0,0)
        strokeWeight(0.5)
        rect(50,50,60,30)
        fill(0,0,0)
        textSize(20)
        textAlign(CENTER)
        text("BACK", 80, 70)
        textAlign(LEFT)
        
        
    def getHighScores(self):
        f = open("highscores.txt", "a") # In case it is our first time playing the game; this creates the file in our directory.
        f.close()
        self.score_dict = {} # Create an empty dictionary that will be used to store player names as keys, and their scores as values.
        self.highscore_file = open("highscores.txt", "r")
        for line in self.highscore_file:
            data = line.strip().split(',') # split each stripped line into a list.
            if len(data) == 2:
                if data[0] not in self.score_dict:  # If player not in dictionary, add player and their score.
                    self.score_dict[data[0]] = int(data[1])
                elif data[0] in self.score_dict: # If player in dictionary, only add player and their score if they outperformed their previous score.
                    if int(data[1]) > self.score_dict[data[0]]:
                        self.score_dict[data[0]] = int(data[1])
                        
        self.highscore_file.close() # Close the file.
        self.sorted_keys = [] # Create an empty list that will be used hold player names in the sorting process.
        self.key_list = list(self.score_dict.keys()) # Create a list of the keys in the dictionary.
        self.value_list = list(self.score_dict.values()) # Create a list of the values in the dictionary.
        self.sorted_values = sorted(self.value_list, reverse = True) # Sort the scores (values) list from greatest to least
        for x in self.sorted_values: # Iterate through the sorted values list.
            n = self.value_list.index(x) # Get x's position in the unsorted list.
            self.sorted_keys.append(self.key_list[n]) # Append the corresponding player name to the sorted keys list.
            self.value_list.remove(x) # Remove the score and the player from both values and keys lists so that players who have received the same value (score) are accounted for.
            self.key_list.remove(self.key_list[n])
    
        # Display the top 10 scores.
        for count, score in enumerate(self.sorted_values):
            if count < 11:
                text(self.sorted_keys[count] + ": " + str(score), WIDTH//2, 150 + 50 *count)
        
        
    # This method displays the leaderboard screen and the high score.
    def highScoresScreen(self):
        image(self.leaderboardImage, 0, 0)
        if 50 <= mouseX <= 110 and 50 <= mouseY <= 80:
             fill(0, 255, 0)
        else:   
            fill(255,192,203)
        stroke(255,0,0)
        strokeWeight(0.5)
        rect(50,50,60,30)
        fill(0,0,0)
        textSize(20)
        textAlign(CENTER)
        text("BACK", 80, 70)
        textSize(40)
        fill(0,0,144)
        self.getHighScores()
        textAlign(LEFT)
        
        
    # This method is used to display the QUIT button.
    def quitButton(self):
        if 50 <= mouseX <= 90 and 50 <= mouseY <= 90:  # "QUIT" in red if mouse is over the button 
            fill(150,0,0)
        else:
            fill(0,150,0)
        textSize(20)
        textAlign(CENTER)
        text("QUIT", 70, 70)
        textAlign(LEFT)
        
        
    # This method is used to display the PAUSE button.
    def pauseButton(self):
        if 120 <= mouseX <= 180 and 50 <= mouseY <= 90 or not self.gameOn:
            fill(150,0,0) # "PAUSE" in red if mouse is over the button or when game is paused.
        else:
            fill(0,150,0) # "PAUSE" in green if mouse is over the button or when the game is not paused.
        textSize(20)
        textAlign(CENTER)
        text("PAUSE", 150 , 70)
        textAlign(LEFT)
        
    
    # This method displays screen features such as the QUIT, PAUSE, sound, and music buttons.
    def displayScreenFeatures(self):
        noFill() # During game time, the sound and music buttons do not change colors based on clicking;  their functionality is represented by the clicking sound.
        rect(100, 650, 50, 50)
        image(self.musicIcon, 103,655)
        rect(160, 650, 50, 50)
        image(self.soundIcon, 165,660)
        self.quitButton()
        self.pauseButton()


    # This method checks whether a game is lost, by checking if jon died (touched by a walker/the NK or hit by the NK's spear), or if Jon
    # ran out of arrows and there are no bonus items from which he could potentially get arrows and there are no arrows in his bow currently being released.
    # The game should also not be lost if jon released his last arrow when there is one only walker in the game.
    def check_loss(self):
        if self.jon.dead:
            self.lost = True
        elif len(self.enemies) > 1 and len(self.jon.quiver) == 0 and len(self.jon.bow) == 0 and len(self.bonusItems) == 0:  
            self.lost = True
        elif len(self.enemies) == 1 and len(self.jon.bow) != 0 and len(self.jon.quiver) == 0: # In the case there is only one walker.
            self.lost = False


   # This method returns a list of tuples of randomly selected white walker locations in this form: (x,y). It takes an armySize parameter to determine
   # how many locations it must churn up.
    def getEnemyLocations(self, armySize):
        enemyLocations = []
        for i in range(armySize):
            y = random.randint(GROUND, HEIGHT*2)
            LeftX = random.randint((-1 * WIDTH)//2, -80)
            RightX = random.randint(WIDTH + 80, WIDTH + WIDTH//2)
            if y > HEIGHT:
                x = random.randint(0, WIDTH)
            else:
                x = random.choice([LeftX, RightX])
                
            if (x,y) not in enemyLocations:
                enemyLocations.append((x,y))
        return enemyLocations
    
    
    # This method uses calls the getEnemyLocations() class method to spawn walkers from those locations.
    def spawnWhites(self, speed, armySize):
        whites = []
        locations = self.getEnemyLocations(armySize)
        for loc in locations:
            whites.append(WhiteWalker(loc[0],loc[1], 38, 69, speed, ANIMATION["White Walker Walking"], 76, 138, 12, RIGHT))
        return whites
    
    
# Instantiate a game object.
game = Game(WIDTH, HEIGHT, GROUND)


# Define the setup window size of the game.
def setup():
    size(WIDTH, HEIGHT)
    
    
# Call the display method of the game class to display game.    
def draw():
    game.display()


# Change the relevant boolean value to True of the handler dictionary attribute of Jon to have him move based on the key the player pressed.
def keyPressed():
    if keyCode == UP:
        game.jon.key_handler[UP] = True
    if keyCode == DOWN:
        game.jon.key_handler[DOWN] = True
    if keyCode == RIGHT:
        game.jon.key_handler[RIGHT] = True
        game.jon.dir = RIGHT
    if keyCode == 32:
        game.jon.projectile_released = True
        if playSound and game.gameOn and not game.won and not game.lost:
            game.jon.shootingSound.rewind()
            game.jon.shootingSound.play() 
    if keyCode == LEFT:
        game.jon.key_handler[LEFT] = True
        game.jon.dir = LEFT


def keyReleased():
    global game
    global typing
    # Stop Jon's movement as soon as the player releases the relevant key.
    if keyCode == UP:
        game.jon.key_handler[UP] = False
    if keyCode == DOWN:
        game.jon.key_handler[DOWN] = False
    if keyCode == 32:
        game.jon.projectile_released = False
    if keyCode == RIGHT:
        game.jon.key_handler[RIGHT] = False
    if keyCode == LEFT:
        game.jon.key_handler[LEFT] = False
    # 
    if game.lost or game.won:
        # If the enter key is released, write the player information, name and score, to the 
        # file "highscore.txt" and instantiate a new game object to take the player back to the main menu.
        try:
            if key == "\n":
                if typing != "" and len(typing) <= 25: # Append and start a new game only when the user's input is not an empty string or not too long.
                    f = open("highscores.txt", "a")
                    f.write(typing + "," + str(game.score) + "\n" )
                    f.close()
                    typing = ""
                    game.backgroundMusic.pause()
                    game = Game(WIDTH, HEIGHT, GROUND)
            # Modify the global variable typing that is being displayed when the game is lost or won based on user input.
            elif str(key).isalpha():
                typing += str(key)
            # If the space bar is released when the game is lost or won, a space will be added to the variable typing
            elif keyCode == 32:
                typing += " "
            # If the backspace key is released, the typing variable will be sliced to exclude the last variable, so as to mimic dynamic deletion.
            elif keyCode == 8:
                typing = typing[:-1]
        except:
            typing += ""
    
    
def mouseClicked():
    global game
    global playMusic
    global playSound
    global LEVELS
    # If game is lost or won or the player pressed the quit button at any point during the game, then we create instantiate a new game object.
    # if game.lost or game.won or (game.gameOn and 50 <= mouseX <= 90 and 50 <= mouseY <= 90) or (not game.gameOn and 50 <= mouseX <= 90 and 50 <= mouseY <= 90):
    if game.lost or game.won or (not game.displayIntro and 50 <= mouseX <= 90 and 50 <= mouseY <= 90):  
        typing = "" 
        game.buttonClick.rewind()
        game.buttonClick.play()
        game.backgroundMusic.pause()
        game = Game(WIDTH, HEIGHT, GROUND)
        
    # If we are in the intro display scene of the game;
    if game.displayIntro:
        # If player presses the "new game" button, then the game starts by setting the attribute gameOn of the game object to True and 
        # displayIntro attribute to False. This controls what is being displayed by the display method of the game class.
        if 530 <= mouseX <= 730 and 650 <= mouseY <= 700:
            game.displayIntro = False
            game.gameOn = True
            game.buttonClick.rewind()
            game.buttonClick.play()
        # If player presses the "High Scores" button, then the leaderboard page is displayed.  
        elif 100 <= mouseX <= 300 and 550 <= mouseY <= 600:
            game.displayHighScores = True
            game.buttonClick.rewind()
            game.buttonClick.play()
        # If player presses the "High Scores" button, then the leaderboard page is displayed.
        elif 950 <= mouseX <= 1150 and 550 <= mouseY <= 600:
            game.buttonClick.rewind()
            game.buttonClick.play()
            game.displayInstructions = True
          
    # If the "back" button is clicked, player is taken to the main intro screen.
    if game.displayHighScores or game.displayInstructions:
        if 50 <= mouseX <= 110 and 50 <= mouseY <= 80:  
            game.buttonClick.rewind()
            game.buttonClick.play()      
            game.displayIntro = True
            game.displayHighScores = False
            game.displayInstructions = False

    # If player clicks on the pause button, the game attribute gameOn is set to False. If player
    # clicks it again while game is not lost and not on, the game is resumed.
    if game.gameOn:
        if 120 <= mouseX <= 180 and 50 <= mouseY <= 90:
            game.buttonClick.rewind()
            game.buttonClick.play()
            game.gameOn = False
    elif not game.lost and not game.gameOn:
        if 120 <= mouseX <= 180 and 50 <= mouseY <= 90:
            game.buttonClick.rewind()
            game.buttonClick.play()
            game.gameOn = True
     
    # If player clicks on the Music button when the background music is on, it is turned it off. If music were off, it is turned on.
    if 100 <= mouseX <= 150 and 650 <= mouseY <= 700 and (not game.lost or (not game.lost and not game.gameOn)):
        game.buttonClick.rewind()
        game.buttonClick.play()
        if playMusic:
            game.backgroundMusic.pause()
            playMusic = False
        else:
            playMusic = True
            game.backgroundMusic.play()
            game.backgroundMusic.loop()
        
    # If player clicks on the Sound button when the background music is on, all  sounds except the clicking sounds will not be played. If playSound were False, it will changed 
    # to True so that sounds could be once again played.
    if 160 <= mouseX <= 210 and 650 <= mouseY <= 700 and (not game.lost or (not game.lost and not game.gameOn)):
        game.buttonClick.rewind()
        game.buttonClick.play()
        if playSound:
            playSound = False
        else:
            playSound = True
