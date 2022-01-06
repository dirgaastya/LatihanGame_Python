# Import library
from typing import cast
import pygame as pg
from pygame import mouse
from pygame.locals import *
from random import randint
import math
# Membuat screen
pg.init()
width, height = 640,480
screen = pg.display.set_mode((width,height))

# Key Mapping
keys = {
    "top" : False,
    "bottom" : False,
    "left" : False,
    "right" : False,
}

running = True
playerPos = [100,100] #Posisi awal pemain

exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN =1

score = 0
arrows=[]

enemy_timer = 100
enemies = [[width,100]]

health_point = 194
countdown_timer = 90000 #90 detik

# Load Asset
player = pg.image.load("resources/images/dude.png")
grass = pg.image.load("resources/images/grass.png")
castle = pg.image.load("resources/images/castle.png")
arrow = pg.image.load("resources/images/bullet.png")
enemy_img = pg.image.load("resources/images/badguy.png")
healthBar = pg.image.load("resources/images/healthbar.png")
health = pg.image.load("resources/images/health.png")
gameOver = pg.image.load("resources/images/gameover.png")
youWin = pg.image.load("resources/images/youwin.png")

# Load audio
pg.mixer.init()
hit_sound = pg.mixer.Sound("resources/audio/explode.wav")
enemyHit = pg.mixer.Sound("resources/audio/enemy.wav")
shoot = pg.mixer.Sound("resources/audio/shoot.wav")
hit_sound.set_volume(0.05)
enemyHit.set_volume(0.05)
shoot.set_volume(0.05)
# Bgm
pg.mixer.music.load("resources/audio/moonlight.wav")
pg.mixer.music.play(-1, 0.0)
pg.mixer.music.set_volume(0.25)

# Game Loop
while(running):
    # Clear Screen
    screen.fill(0)

    # draw game obj
    
    # draw grass
    for x in range(int(width/grass.get_width()+1)):
        for y in range(int(height/grass.get_width()+1)):
            screen.blit(grass, (x*100, y*100))
    
    #draw castle
    screen.blit(castle, (0,30)) 
    screen.blit(castle, (0,135)) 
    screen.blit(castle, (0,240)) 
    screen.blit(castle, (0,345)) 

    # player position
    mouse_position = pg.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (playerPos[1]+32), mouse_position[0] - (playerPos[0]+26))
    player_rotation = pg.transform.rotate(player, 360 - angle * 57.29)
    new_playerPos = (playerPos[0] - player_rotation.get_rect().width / 2, (playerPos[1] - player_rotation.get_rect().height / 2))
    screen.blit(player_rotation, new_playerPos)
    
    #draw arrow
    for bullet in arrows:
        arrow_index=0
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1]+= velx
        bullet[2]+= vely

        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            arrows.pop(arrow_index)
        arrow_index +=1
        # draw the arrow
        for projectile in arrows:
            new_arrow = pg.transform.rotate(arrow, 360 - projectile[0]*57.29)
            screen.blit(new_arrow, (projectile[1],projectile[2]))
    
    # Draw enemy
    enemy_timer -= 1
    if enemy_timer == 0:
        # buat musuh
        enemies.append([width,randint(50, height -32)])
        #reset enemy timer to random time
        enemy_timer = randint(1,100)
    
    index = 0
    for enemy in enemies:
        # musu h bergerak
        enemy[0] -= 5
        # hapus musuh
        if enemy[0] < -64:
            enemies.pop(index)
        # 6.2.1 collision between enemies and castle 
        enemy_rect = pg.Rect(enemy_img.get_rect())
        enemy_rect.top = enemy[1] # ambil titik y 
        enemy_rect.left = enemy[0] # ambil titik x
        # benturan musuh dengan markas kelinci
        if enemy_rect.left < 64:
            enemies.pop(index)
            health_point -= randint(5,20)
            hit_sound.play()
            print("Oh tidak, kita diserang!!")
        
        # 6.2.2 Check for collisions between enemies and arrows
        index_arrow = 0
        for bullet in arrows:
            bullet_rect = pg.Rect(arrow.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            # benturan anak panah dengan musuh
            if enemy_rect.colliderect(bullet_rect):
                score += 1
                enemies.pop(index)
                arrows.pop(index_arrow)
                enemyHit.play()
                print("Boom! mati kau!")
                print("Score: {}".format(score))
            index_arrow += 1
        index += 1
    
    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    #Draw HB
    screen.blit(healthBar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))
    
    # Draw Clock
    font = pg.font.Font(None, 24)
    minutes = int((countdown_timer-pg.time.get_ticks())/60000)
    seconds = int((countdown_timer-pg.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635,5]
    screen.blit(clock, textRect)
    # update the screen
    pg.display.flip()

    # Event Loop
    for event in pg.event.get():
        # event saat tombol exi diklik
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        # Fire
        if event.type == pg.MOUSEBUTTONDOWN:
            arrows.append([angle, new_playerPos[0]+32, new_playerPos[1]+32])
            shoot.play()
        #check keydowm / key up
        if event.type == pg.KEYDOWN:
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_a:
                keys["left"] = True
            elif event.key == K_s:
                keys["bottom"] = True
            elif event.key == K_d:
                keys["right"] = True
        if event.type == pg.KEYUP:
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_a:
                keys["left"] = False
            elif event.key == K_s:
                keys["bottom"] = False
            elif event.key == K_d:
                keys["right"] = False
    #end event loop

    # Move player
    if keys["top"]:
        playerPos[1] -= 5 # - y
    elif keys["bottom"]:
        playerPos[1] += 5 # +y
    elif keys["left"]:
        playerPos[0] -= 5 # -x
    elif keys["right"]:
        playerPos[0] += 5 # + y
    
    time_getTicks = pg.time.get_ticks()

    if  time_getTicks > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER

if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameOver, (0,0))
else:
    screen.blit(youWin, (0,0))

text = font.render("Score: {}".format(score), True, (255,255,255))
textRect = text.get_rect()
textRect.centerx=screen.get_rect().centerx
textRect.centery=screen.get_rect().centery + 24
screen.blit(text, textRect)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
    pg.display.flip()