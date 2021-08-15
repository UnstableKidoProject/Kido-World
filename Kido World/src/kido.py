import pygame
import random
#model
class Kido(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y):
        '''
		initializes object's state
		arg: self: instance of class; game: allows reference to game loop; name: name of object; x: x-position of object; y: y-position of object
		return: none
	'''
        # initialize all the Sprite functionality
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        # create surface object image
        self.load_images()
        self.image = self.stand_frame
        
        # get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # set other attributes
        self.name = name
        self.player_acc = 0.5
        self.player_friction = -0.12
        self.player_grav = .9
        self.player_jump = 21
        self.width = 500
        self.height = 500
        self.vec = pygame.math.Vector2
        self.pos = self.vec(40, self.height - 100)
        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)
        self.left = False
        self.right = False
        self.jumping = False
        self.invincibility = False
        self.poweruptimer = 0

    
    def load_images(self):
        '''
		loads images for animation
		arg: self: instance of class
		return: none
	'''
        self.left_frame = pygame.image.load("assets/kido_left.png").convert_alpha()
        self.right_frame = pygame.image.load("assets/kido_right.png").convert_alpha()
        self.stand_frame = pygame.image.load("assets/kido.png").convert_alpha()
        self.invincibility_left_frame = pygame.image.load("assets/flexi_kido_left.png").convert_alpha()
        self.invincibility_right_frame = pygame.image.load("assets/flexi_kido_right.png").convert_alpha()
        self.invincibility_stand_frame = pygame.image.load("assets/flexi_kido.png").convert_alpha()

    def jump(self):
        '''
		allows player to jump
		arg: self: instance of class
		return: none
	'''
        # jumps if standing on a platform
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        boosthits = pygame.sprite.spritecollide(self, self.game.boostPlatforms, False)
        breakhits = pygame.sprite.spritecollide(self, self.game.breakPlatforms, False)

        # checks if player hits platform that gives boost
        if boosthits and not self.jumping:
            self.jumping = True
            self.vel.y = -50
            self.invincibility = True
            self.poweruptimer = 80
            self.poweruptimer -=1
            if self.poweruptimer == 0:
                self.invincibility = False

        # checks if player hits platform that breaks
        elif breakhits and not self.jumping:
            self.jumping = True
            breakhits[0].kill()

        # checks if player hits other platforms
        elif hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.player_jump
        
        # checks if player hits boost powerup
    def boost(self):
        self.jumping = True
        self.vel.y = -50
        self.invincibility = True
        self.poweruptimer = 80
        self.poweruptimer -=1
        if self.poweruptimer == 0:
            self.invincibility = False


    def update(self):
        '''
		updates player
		arg: self: instance of class
		return: none
	'''
        self.acc = self.vec(0, self.player_grav)
        self.animate()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -self.player_acc
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT]:
            self.acc.x = self.player_acc
            self.right = True
            self.left = False
        else:
            self.left = False
            self.right = False

        # apply friction
        self.acc.x += self.vel.x * self.player_friction
        
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # wrap around the sides of the screen
        if self.pos.x > self.width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.width
        self.rect.midbottom = self.pos

    def animate(self):
        '''
		animates player
		arg: self: instance of class
		return: none
	'''
        # animates when not invincible
        if self.invincibility == False:
            if self.right:
                self.image = self.right_frame
            elif self.left == True:    
                self.image = self.left_frame
            else:
                self.image = self.stand_frame
        
        # animates when invincible
        elif self.invincibility == True:
            if self.right:
                self.image = self.invincibility_right_frame
            elif self.left == True:    
                self.image = self.invincibility_left_frame
            else:
                self.image = self.invincibility_stand_frame