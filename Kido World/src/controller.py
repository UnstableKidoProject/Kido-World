import sys
import pygame
import random
from src import kido
from src import platform
from src import menu
from src import enemy
from src import powerup

class Controller:
    def __init__(self):
        '''
		initializes object's state
		arg: self: instance of class
		return: none
	'''
        pygame.init()

        ''' Setting up screen '''
        self.width = 500
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background_image = pygame.image.load('assets/star.png')
        pygame.display.set_caption("Kido Jump!")
        self.clock = pygame.time.Clock()
        pygame.font.init()

        ''' Loading score and highscore '''
        self.score = 0
        self.load_data()
        
        ''' Loading the sprites we need ''' 
        self.kido = kido.Kido(self, "Baxter", 100, 450)
        self.scoreboard = platform.Platform("Platform", 10, 10, "assets/scoreboard.png")
        self.platforms = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.powerup = pygame.sprite.Group()
        self.boost = pygame.sprite.Group()
        self.rightPlatforms = pygame.sprite.Group()
        self.leftPlatforms = pygame.sprite.Group()
        self.boostPlatforms = pygame.sprite.Group()
        self.breakPlatforms = pygame.sprite.Group()
       
        # loads enemies in random positions
        for i in range(1):
            y = random.randrange(-200, -180)
            self.enemy.add(enemy.Enemy("Bullet", 60, y))           
        
        # loads platforms in random positions
        # (broken into two sections so that RNG won't make it impossible to progress if spawns are bad)
        for i in range(3):
            x = random.randrange(100, 500)
            y = random.randrange(0, 250)
            self.platforms.add(platform.Platform("Platform", x, y, "assets/large_platform.png"))
            x = random.randrange(100, 400)
            y = random.randrange(250, 400)
            self.platforms.add(platform.Platform("Platform", x, y, "assets/large_platform.png"))

        # loads powerups in random positions
        self.powerup.add(powerup.Powerup("Invincibility", random.randrange(20, 450), random.randrange(-2000, -500), "assets/powerup.png"))
        self.boost.add(powerup.Powerup("Boost", random.randrange(20, 450), random.randrange(-2000, -500), "assets/boost.png"))
            
        # starting platform
        firstPlatform = platform.Platform("Platform", 0, 470, "assets/starting_plat.png")
        self.platforms.add(firstPlatform)

        # grouping all sprites
        self.all_sprites = pygame.sprite.Group(
            (self.kido, self.scoreboard) + tuple(self.platforms) + tuple(self.enemy) + tuple(self.powerup) + tuple(self.boost))

        ''' Game State '''
        self.STATE = "MENU"


        
    def load_data(self):
        '''
		loads highscore data
		arg: self: instance of class
		return: none
	'''
        with open("src/highscore.json", 'r') as f:
            try: 
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def mainLoop(self):
        '''
		updates the game state
		arg: self: instance of class
		return: none
	'''
        while True:
            if(self.STATE == "MENU"):
                self.mainmenu()
            elif(self.STATE == "GAME"):
                self.gameLoop()
            elif(self.STATE == "GAMEOVER"):
                self.gameOver()

    def gameLoop(self):
        '''
		runs the game
		arg: self: instance of class
		return: none
	'''
        while self.STATE == "GAME":

            ''' Sets FPS '''
            self.clock.tick(60)

            ''' Sets events '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            ''' Updates sprites '''
            self.update()

            ''' Drawing screen '''
            # background
            self.screen.blit(self.background_image, (0, 0))
                
            # draws all sprites
            self.all_sprites.draw(self.screen)
               
            # draws scoreboard
            font = pygame.font.SysFont(None, 20, False)
            scoreboard = font.render('Score: ' + str(self.score), False, (255, 255, 255))
            self.screen.blit(scoreboard, (15, 15))
                
            # flips screen
            pygame.display.flip()

    def update(self):
        '''
		updates sprites
		arg: self: instance of class
		return: none
	'''
        ''' Player auto jump '''
        self.kido.jump()

        ''' Updating all sprites '''
        self.all_sprites.update()

        ''' Checks if player hits platform '''
        if self.kido.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.kido, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.kido.pos.x < lowest.rect.right + 10 and \
                    self.kido.pos.x > lowest.rect.left -10:
                        self.kido.pos.y = lowest.rect.top
                        self.kido.vel.y = 0
                        self.kido.jumping = False

        ''' Checks if player reaches 1/4 of screen '''
        if self.kido.rect.top <= self.height / 4:
            self.kido.pos.y += max(abs(self.kido.vel.y), 2)
                
            # scrolls platforms
            for plat in self.platforms:
                plat.rect.y += max(abs(self.kido.vel.y), 2)
                if plat.rect.top >= self.height:
                    plat.kill()
                    self.score += 10
                
            # scrolls enemies
            for enemy in self.enemy:
                enemy.rect.y += max(abs(self.kido.vel.y), 2)
                if enemy.rect.y > 600:
                    enemy.rect.y -= random.randrange(1600, 2000)
                
            # scrolls powerups
            for powerup in self.powerup:
                powerup.rect.y += max(abs(self.kido.vel.y), 2)
                if powerup.rect.y > 600:
                    powerup.rect.y -= random.randrange(4000, 5000)
                    powerup.rect.x = random.randrange(20, 450)
            for boost in self.boost:
                boost.rect.y += max(abs(self.kido.vel.y), 2)
                if boost.rect.y > 600:
                    boost.rect.y -= random.randrange(4000, 5000)
                    boost.rect.x = random.randrange(20, 450)

        ''' Adds new platforms '''
        while len(self.platforms) < 6:
            regPlat = ["assets/small_platform.png",
                     "assets/medium_platform.png",
                     "assets/large_platform.png"]
            specialPlat = ["assets/special.png",
                         "assets/special2.png",
                         "assets/special3.png",
                        "assets/special4.png"]
            platform_size = random.choice(regPlat)
            platform_type = random.choice(specialPlat)
                
            # adds special platforms
            if random.randrange(0,100) < 20:
                newPlatform = platform.Platform("Platform", random.randrange(0, 350), random.randrange(-15, 50),  platform_type)
                # platform moving right
                if platform_type == "assets/special.png":
                    self.rightPlatforms.add(newPlatform)
                    
                # platform moving left
                elif platform_type == "assets/special2.png":
                    self.leftPlatforms.add(newPlatform)
                    
                # platform that gives boost
                elif platform_type == "assets/special3.png":
                    self.boostPlatforms.add(newPlatform)
                    
                # platform that break
                elif platform_type == "assets/special4.png":
                    self.breakPlatforms.add(newPlatform)
                self.platforms.add(newPlatform)
                self.all_sprites.add(newPlatform)
            
            # adds regular platforms
            else:
                newPlatform = platform.Platform("Platform", random.randrange(0, 350), random.randrange(-15, 50),  platform_size)
                self.platforms.add(newPlatform)
                self.all_sprites.add(newPlatform)
        
        ''' Updates moving platforms '''
        for plat in self.rightPlatforms:
            plat.movingRight()
        for plat in self.leftPlatforms:
            plat.movingLeft()
    
        ''' Check for collisions with powerup'''
        # check for player with powerup
        if pygame.sprite.spritecollide(self.kido, self.powerup, False):
            for powerup in self.powerup:
                if powerup.name == "Invincibility":
                    powerup.reposition()
                    self.kido.invincibility = True
                    self.kido.poweruptimer = powerup.duration
        
                    # boost powerup
        if pygame.sprite.spritecollide(self.kido, self.boost, False):
            for boost in self.boost:
                if boost.name == "Boost":
                    boost.reposition()
                    self.kido.boost()

        
        # powerup duration
        self.kido.poweruptimer -=1
        if self.kido.poweruptimer == 0:
            self.kido.invincibility = False

        ''' Check for collisions with enemies'''
        if self.kido.invincibility == False:
            if pygame.sprite.spritecollide(self.kido, self.enemy, False):
                self.STATE = "GAMEOVER"
        if self.kido.invincibility == True:
            if pygame.sprite.spritecollide(self.kido, self.enemy, False):
                print("You're Invincible!")
    
        ''' Player dies'''
        if self.kido.rect.bottom > self.height + 10:
            self.STATE = "GAMEOVER"


    def mainmenu(self):
        '''
		load main menu
		arg: self: instance of class
		return: none
	'''
        # loads buttons
        self.playButton = menu.Menu("Play", 250, 300, "assets/play_button.png")
        self.quitButton = menu.Menu("Quit", 250, 400, "assets/quit_button.png")
        self.title = menu.Menu("Title", 250, 100, "assets/title.png")
        self.menu_sprites = pygame.sprite.Group(self.playButton, self.quitButton, self.title)
        

        # menu logic for clicking buttons
        while self.STATE == "MENU":
            
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if self.playButton.rect.collidepoint(pos):
                            self.STATE = "GAME"
                        if self.quitButton.rect.collidepoint(pos):
                            pygame.quit()
                            sys.exit()
            
            self.menu_sprites.update()
            
            # color background
            self.screen.blit(self.background_image, (0, 0))
                
            # draw sprites
            self.menu_sprites.draw(self.screen)
            pygame.display.flip()
            
            
    
    def gameOver(self):
        '''
		load game over menu
		arg: self: instance of class
		return: none
	'''
        ''' Drawing End Screen '''
        # load image sprites
        self.quitButton = menu.Menu("Quit", 250, 300, "assets/quit_button.png")
        self.scoreContainer = menu.Menu("Score", 250, 200, "assets/scorecard.png")
        self.gameOverContainer = menu.Menu("Score", 250, 100, "assets/scorecard.png")
        self.menu_sprites = pygame.sprite.Group(self.quitButton, self.scoreContainer,self.gameOverContainer)
        
        # color background
        self.screen.blit(self.background_image, (0, 0))
            
        # load sprites
        self.menu_sprites.draw(self.screen)
        font = pygame.font.SysFont(None, 50, False)
        smallfont = pygame.font.SysFont(None, 34, False)
            
        # writing score
        gameover = font.render("Game over!", False, (255, 255, 255))
        score = smallfont.render("Score: " + str(self.score), False, (255, 255, 255))
            
        # writing highscore
        highscore = smallfont.render("Highscore: " + str(self.highscore), False, (255, 255, 255))
        newhighscore = smallfont.render("New HS: " + str(self.score), False, (255, 255, 255))
        self.endcard = platform.Platform("Endcard", 10, 10, "assets/scoreboard.png")
        self.screen.blit(gameover, (self.width / 3, self.height / 6))
        self.screen.blit(score, (self.width / 3, self.height / 3))
            
        # checks if new highscore
        if self.score > self.highscore:
            self.highscore = self.score
            with open ("src/highscore.json", 'w')  as f:
                f.write(str(self.score))
            self.screen.blit(newhighscore, (self.width / 3, self.height / 2.5))
        else:
            self.screen.blit(highscore, (self.width / 3, self.height / 2.5))
        
        pygame.display.flip()

        # quit button logic
        while self.STATE == "GAMEOVER":
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.quitButton.rect.collidepoint(pos):
                        pygame.quit()
                        sys.exit()
