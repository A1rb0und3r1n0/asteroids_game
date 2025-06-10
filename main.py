# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
import os


from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    score = 0
    score_increment = 1

    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatables, drawables)
    Asteroid.containers = (asteroids, updatables, drawables)
    AsteroidField.containers = (updatables)
    Shot.containers = (shots, updatables, drawables)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroidfield = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")

        font = pygame.font.Font(None, 36)

        updatables.update(dt)

        for asteroid in asteroids:
            if player.colliding_with(asteroid):
                print("Game Over!")
                return
            
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.colliding_with(shot):
                    asteroid.split(asteroidfield)
                    shot.kill()
                    score += score_increment
            
        for drawable in drawables:
            drawable.draw(screen)

        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        dt = clock.tick(60)/1000
       



if __name__ == "__main__":
    main()