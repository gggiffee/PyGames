import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359))
pygame.display.set_caption('Python GAME')
icon = pygame.image.load('prikol.jpg')
pygame.display.set_icon(icon)

bg= pygame.image.load('f.png').convert_alpha()

walk_left = [
    pygame.image.load('player_left1.png').convert_alpha(),
    pygame.image.load('player_left2.png').convert_alpha(),
    pygame.image.load('player_left3.png').convert_alpha(),
    pygame.image.load('player_left4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('player_rith1.png').convert_alpha(),
    pygame.image.load('player_rith2.png').convert_alpha(),
    pygame.image.load('player_rith3.png').convert_alpha(),
    pygame.image.load('player_rith4.png').convert_alpha(),
]

ghost = pygame.image.load('a.png').convert_alpha()
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y =250

is_jump = False
jump_count = 8

bg_saund = pygame.mixer.Sound('sauntrec.mp3')

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

label = pygame.font.Font('Micro5-Regular.ttf',110)
lose_lable = label.render('You Loser', True, (193,196,199))
restart_lable = label.render('Restart', True, (115,132,148))
restart_lable_rect = restart_lable.get_rect(topleft=(180, 200))
bullets_left = 5
bullet = pygame.image.load('bulleet.png').convert_alpha()
bullets = []

gameplay = True

runnung = True
while runnung:

    screen.blit(bg, (0,0))
    screen.blit(bg,(bg_x + 618,0))
    
    if gameplay: 

        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))

        if ghost_list_in_game:
            for(i, el)in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x,player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x,player_y))


        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
                if jump_count >= -8:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 8


        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count +=1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0
        
        if bullets:
            # Выпускает патрон
            for (i, el) in enumerate( bullets):
                screen.blit(bullet, (el.x,el.y))
                el.x += 4

                if el.x > 630:
                    bullets.pop(i)
                # Удаляет монстра при столкновении с патроном
                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87,88,89))
        screen.blit(lose_lable,(180,100))
        screen.blit(restart_lable,restart_lable_rect)

        mouse = pygame.mouse.get_pos()
        if restart_lable_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5


    pygame.display.update( )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnung = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_w and bullets_left>0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1

    clock.tick(15)
