import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.images = []
        for num in range (1, 6):
            img = pygame.image.load(f"./Image_Files/Explosion/exp{num}.png")
            img = pygame.transform.scale(img, (radius, radius))
            self.images.append(img)
        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        explosion_speed = 3 #number of frames sprite is displayed
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


