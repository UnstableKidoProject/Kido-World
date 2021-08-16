import pygame
import random
# model
class Powerup(pygame.sprite.Sprite):
    def __init__(self, name, x, y, image):
        '''
		initializes object's state
		arg: self: instance of class; name: name of object; x: x-position of object; y: y-position of object; image: image to represent object
		return: none
	'''
        # initialize all the Sprite functionality
        pygame.sprite.Sprite.__init__(self)

        # create surface object image
        self.image = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(), (30,30))
        
        # get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # set other attributes
        self.name = name
        self.duration = 1000
          
    
    def reposition(self):
        '''
		repostitions the invinciblilty star after using it (Moves it up the map after collision instead of deleting and readding sprite)
		arg: self: instance of class
		return: none
	'''
        self.rect.y -= random.randrange(4000, 5000)
        self.rect.x = random.randrange(20, 450)

    



