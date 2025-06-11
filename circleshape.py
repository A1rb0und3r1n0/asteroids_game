import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, image_path = None):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (radius * 2.2, radius * 2.2))
            self.rect = self.image.get_rect(center=(x, y))
            self.rotated_images = [pygame.transform.rotate(self.image, angle) for angle in range(0, 360, 1)]

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def colliding_with(self, other):
        return self.radius + other.radius > self.position.distance_to(other.position)