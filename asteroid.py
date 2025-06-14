from circleshape import *
from constants import *
from explosion import*
import random
import numpy as np


class Asteroid(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, radius, file_path):
        super().__init__(x, y, radius, file_path)
        self.rotation = 0
        self.angle = 0
        self.mass = radius ** 2

        self.invulnerable = True
        self.invul_timer = 0
        
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.circle(screen, "white", self.position, self.radius, 2) #draws debug circle

    def update(self, dt):

        if self.invulnerable:
            self.invul_timer += dt  # dt ist bereits in Sekunden
            if self.invul_timer >= 5:
                self.invulnerable = False

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

    #GPT CODE
    def resolve_collision(self, other):
        normal = self.position - other.position
        distance_squared = normal.length_squared()

        if distance_squared == 0:
            # Prevent division by zero
            normal = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            distance_squared = 1.0  # arbitrary non-zero

        relative_velocity = self.velocity - other.velocity
        dot_product = relative_velocity.dot(normal)

        if dot_product >= 0:
            return  # already moving apart — no need to resolve

        impulse = (2 * dot_product) / ((self.mass + other.mass) * distance_squared)

        self.velocity -= impulse * other.mass * normal
        other.velocity += impulse * self.mass * normal



    '''
    def resolve_collision(self, other):
        normal = self.position - other.position
        #normalized_normal = normal / np.linalg.norm(normal)

        velocity_difference_1 = self.velocity - other.velocity
        #velocity_difference_2 = other.velocity - self.velocity
        dot1 = velocity_difference_1.dot(normal)
        dot2 = -velocity_difference_1.dot(-normal)

        self.velocity = self.velocity - (2 * other.mass / (self.mass + other.mass)) * (dot1 / (normal.length() ** 2)) * normal
        other.velocity = other.velocity - (2 * self.mass / (self.mass + other.mass)) * (dot2 / (normal.length() ** 2)) * (-normal)
    '''