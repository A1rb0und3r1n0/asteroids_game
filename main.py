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
from explosion import *



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
    explosions = pygame.sprite.Group()
    Player.containers = (updatables, drawables)
    Asteroid.containers = (asteroids, updatables, drawables)
    AsteroidField.containers = (updatables)
    Shot.containers = (shots, updatables, drawables)
    Explosion.containers = (updatables, drawables, explosions)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroidfield = AsteroidField()

    while True:
        game_state()

        global PLAYER_ALIVE
        global PLAYER_LIVES

        keys = pygame.key.get_pressed() 
        Backdrop = pygame.image.load("./Image_Files/Backdrop/Space.jpg")
        Backdrop = pygame.transform.scale(Backdrop, (SCREEN_WIDTH, SCREEN_HEIGHT))
        score_text_ui = score_font.render(f'Score: {score}', True, (255, 255, 255))
        pause_text = pause_font.render('PAUSED', True, (255, 255, 255))
        death_text = pause_font.render('GAME OVER', True, (255, 255, 255))
        lives_text = pause_font.render(f'Lives remaining: {PLAYER_LIVES}', True, (255, 255, 255))
        lives_text_ui = score_font.render(f'Lives remaining: {PLAYER_LIVES}', True, (255, 255, 255))
        respawn_text = score_font.render('PRESS SPACE TO RESPAWN', True, (255, 255, 255))

        
        screen.blit(Backdrop, Backdrop.get_rect())


        if PAUSE:
            screen.blit(pause_text,(SCREEN_WIDTH/2 - pause_text.get_width()/2, SCREEN_HEIGHT/2 - pause_text.get_height()/2))     
        elif not PLAYER_ALIVE:
            if PLAYER_LIVES > 0:
                screen.blit(lives_text,(SCREEN_WIDTH/2 - lives_text.get_width()/2, SCREEN_HEIGHT/2 - lives_text.get_height()/2))
                screen.blit(respawn_text,(SCREEN_WIDTH/2 - respawn_text.get_width()/2, SCREEN_HEIGHT/2 - respawn_text.get_height()/2 + lives_text.get_height()))
                if keys[pygame.K_SPACE]:
                    screen.fill("black")
                    PLAYER_LIVES -= 1
                    PLAYER_ALIVE = True
                    player.respawn()
                    updatables.update(dt)
            else:
                screen.blit(death_text,(SCREEN_WIDTH/2 - death_text.get_width()/2, SCREEN_HEIGHT/2 - death_text.get_height()/2))
        else:
            updatables.update(dt)

            for asteroid in asteroids:
                if player.colliding_with(asteroid):
                    PLAYER_ALIVE = False

            for asteroid in asteroids:
                exclude = asteroid
                for asteroid2 in asteroids:
                    if asteroid2 == exclude:
                        pass
                    elif asteroid.colliding_with(asteroid2):
                        asteroid.resolve_collision(asteroid2)
                        #asteroid.split(asteroidfield)
                        #asteroid2.split(asteroidfield)  

            '''
            for asteroid in asteroids:
                exclude = asteroid
                for asteroid2 in asteroids:
                    if asteroid2 == exclude:
                        pass
                    elif asteroid.colliding_with(asteroid2) and asteroid.invulnerable == False and asteroid2.invulnerable == False:
                        #asteroid.split(asteroidfield)
                        #asteroid2.split(asteroidfield)  
            '''

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.colliding_with(shot):
                        asteroid.split(asteroidfield)
                        shot.kill()
                        score += SCORE_INCREMENT
            
            for drawable in drawables:
                drawable.draw(screen)

        
        screen.blit(score_text_ui, (10, 10))
        screen.blit(lives_text_ui, (SCREEN_WIDTH - (lives_text_ui.get_width() + 10), 10))

        pygame.display.flip()
        clock.tick(60)
        dt = clock.tick(60)/1000


if __name__ == "__main__":
    main()