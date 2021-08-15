import pygame
import random
#model
class Menu(pygame.sprite.Sprite):
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
        self.rect.centerx = x
        self.rect.centery = y
        
        #set other attributes
        self.name = name