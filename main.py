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



def game_state():
    global PAUSE
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            PAUSE = not PAUSE
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
            sys.exit()

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
 
    score_font = pygame.font.Font(None, 36)
    pause_font = pygame.font.Font(None, 128)

    
    score = 0

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
        game_state()

        global PLAYER_ALIVE
        
        screen.fill("black")
        score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
        pause_text = pause_font.render('PAUSED', True, (255, 255, 255))
        death_text = pause_font.render('GAME OVER', True, (255, 255, 255))
        lives_text = pause_font.render(f'Lives remaining: {PLAYER_LIVES}', True, (255, 255, 255))
        respawn_text = score_font.render('PRESS SPACE TO RESPAWN', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH, 10))

        if PAUSE:
            screen.blit(pause_text,(SCREEN_WIDTH/2 - pause_text.get_width()/2, SCREEN_HEIGHT/2 - pause_text.get_height()/2))
        elif not PLAYER_ALIVE:
            if PLAYER_LIVES > 0:
                screen.blit(lives_text,(SCREEN_WIDTH/2 - lives_text.get_width()/2, SCREEN_HEIGHT/2 - lives_text.get_height()/2))
                screen.blit(respawn_text,(SCREEN_WIDTH/2 - respawn_text.get_width()/2, SCREEN_HEIGHT/2 - respawn_text.get_height()/2 + lives_text.get_height()))
            else:
                screen.blit(death_text,(SCREEN_WIDTH/2 - death_text.get_width()/2, SCREEN_HEIGHT/2 - death_text.get_height()/2))
        else:
            updatables.update(dt)

            for asteroid in asteroids:
                if player.colliding_with(asteroid):
                    print("Game Over!")
                    PLAYER_ALIVE = False
                    #return
            
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.colliding_with(shot):
                        asteroid.split(asteroidfield)
                        shot.kill()
                        score += SCORE_INCREMENT
            
            for drawable in drawables:
                drawable.draw(screen)

        

        pygame.display.flip()
        clock.tick(60)
        dt = clock.tick(60)/1000
        
       



if __name__ == "__main__":
    main()