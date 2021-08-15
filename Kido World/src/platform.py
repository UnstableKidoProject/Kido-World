import pygame
import random
#model
class Platform(pygame.sprite.Sprite):
    def __init__(self, name, x, y, img_file):
        '''
		initializes object's state
		arg: self: instance of class; name: name of object; x: x-position of object; y: y-position of object; img_file: image file to represent object
		return: none
	'''
        #initialize all the Sprite functionality
        pygame.sprite.Sprite.__init__(self)
        #create surface object image
        self.image = pygame.image.load(img_file).convert_alpha()
        #get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #set other attributes
        self.name = name

    def movingRight(self):
        '''
		makes platform moves right
		arg: self: instance of class
		return: none
	'''
        self.rect.x += 1
        # platforms wraps around screen
        if self.rect.centerx == 500:
            self.rect.centerx = 0

    def movingLeft(self):
        '''
		makes platform moves left
		arg: self: instance of class
		return: none
	'''
        # platforms moves left
        self.rect.x -= 1
        # platforms wraps around screen
        if self.rect.centerx == 0:
            self.rect.centerx = 500
