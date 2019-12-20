import pygame


class OnBoard(pygame.sprite.Sprite):
    def __init__(self, raw_image, position):
        super(OnBoard, self).__init__()
        self.__position = position
        self.image = raw_image
        self.image = pygame.transform.scale(self.image,
                                            (15, 15))  # Image and Rect required for the draw function on sprites
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

    # Getters and Setters
    def setCenter(self, position):
        self.rect.center = position

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    # Update Image, this is an abstract method, needs to be implemented in the subclass with whatever size required
    def updateImage(self, raw_image):  # Abstract Method
        raise NotImplementedError("Subclass must implement this")

    # Modify the size of the image
    def modifySize(self, raw_image, height, width):
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (width, height))