from circleshape import *
from constants import *
from explosion import*
import random

class Asteroid(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, radius, file_path):
        super().__init__(x, y, radius, file_path)
        self.rotation = 0
        self.angle = 0
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.circle(screen, "white", self.position, self.radius, 2) #draws debug circle

    def update(self, dt):
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        elif self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        elif self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        
        self.position += self.velocity * dt
        self.rect.center = (self.position.x, self.position.y)
       
        
        self.angle = (self.angle + 2) % 360  # Adjust rotation speed
        self.image = self.rotated_images[self.angle // 1]
        self.rect = self.image.get_rect(center=self.rect.center)


    def split(self, asteroidfield):       
        
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            explosion = Explosion(self.position.x, self.position.y, self.radius * 3)
            return
        else:
            random_angle = random.uniform(20.0, 50.0)
            direction1 = self.velocity.rotate(random_angle) * 1.2
            direction2 = self.velocity.rotate(-random_angle) * 1.2
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroidfield.spawn(new_radius, self.position, direction1) 
            asteroidfield.spawn(new_radius, self.position, direction2)
        
            explosion = Explosion(self.position.x, self.position.y, self.radius * 3)

            


            


    