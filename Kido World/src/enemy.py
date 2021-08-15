import pygame
import random
# model
class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        '''
		initializes object's state
		arg: self: instance of class; name: name of object; x: x-position of object; y: y-position of object
		return: none
	'''
        # initialize all the Sprite functionality
        pygame.sprite.Sprite.__init__(self)
        
        # create surface object image
        self.load_images()
        self.image = self.right_frame
        
        # get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # set other attributes
        self.name = name
        self.speed = 2
        self.direction = "r"

    def load_images(self):
        '''
		loads images for animation
		arg: self: instance of class
		return: none
	'''
        self.left_frame = pygame.transform.smoothscale(pygame.image.load("assets/enemy_L.png").convert_alpha(), (50,50))
        self.right_frame = pygame.transform.smoothscale(pygame.image.load("assets/enemy_R.png").convert_alpha(), (50,50))
    
    def update(self):
        '''
		updates enemies
		arg: self: instance of class
		return: none
	'''
        # changes direction of bullet
        if self.rect.x > 450:
            self.direction = "l"
        elif self.rect.x < 20:
            self.direction = "r"

        # bullet moves left to right and updates the image of it
        if self.direction == "r":
            self.rect.x += self.speed
            self.image = self.right_frame
        elif self.direction == "l":
            self.rect.x -= self.speed
            self.image = self.left_frame