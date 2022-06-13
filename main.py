import pygame
from sprite import Player, Door, Tile, Bullet
import random

pygame.init()
screen = pygame.display.set_mode((2000, 1000))
pygame.display.set_caption("Castle Race")

game_active = False
released = False

red = 0
green = 0
blue = 0

color1 = (0,0,0)
color2 = (0,0,0)

frame_rate = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 50)

player = pygame.sprite.GroupSingle()
player.add(Player())

door = pygame.sprite.GroupSingle()
door.add(Door())

bullet = pygame.sprite.Group()

bullet_count = 5
tiles = pygame.sprite.Group()

color_chosen = False
choice = 0

level = 1
bullet_pos_x = -100

image = ""
image_rect = ""

background = ""
background_rect = ""

castle = ""
castle_rect = ""

castle2 = ""
castle_rect2 = ""



def title_screen():
    global font, score

    title_text = font.render('Welcome To Day 5!', False, 'white')
    title_rect = title_text.get_rect(midtop=(1000, 200))
    screen.blit(title_text, title_rect)

    if score > 0:
        score_label = font.render(f"Your Score: {score}", False, 'white')
        score_rect = score_label.get_rect(center=(1000, 360))
        screen.blit(score_label, score_rect)

    instructions_label = font.render('Press the space bar to Start', False, 'gray')
    instructions_rect = instructions_label.get_rect(center=(1000, 500))
    screen.blit(instructions_label, instructions_rect)

def display_score():

    global score, font

    text = 'Score: ' + str(score)

    score_surface = font.render(text, False, 'white')
    font.set_bold(score_surface)
    score_rectangle = score_surface.get_rect(center=(1000, 50))
    screen.blit(score_surface, score_rectangle)


def reset():
    global score, released, level, bullet, bullet_count, bullet_pos_x, tiles, player

    create_background()

    level = 1
    score = 0
    bullet_count = 5
    bullet_pos_x = 0
    player.sprite.rect = player.sprite.image.get_rect(topleft=(500, 880))

    bullet.empty()
    tiles.empty()
    generate_bullets()
    generate_tiles()
    released = False

def generate_tiles():
    num = level * 5 + 10
    increment = random.randint(300,400)

    if level < 6:
        increment = random.randint(300, int(14000/num))

    stack_amount = 0
    stack_verticle = False
    previous_x = 900
    previous_y = 0
    overlapping = True
    bullet_count = 5

    for i in range(0,num):
        tile = Tile(i)


        if stack_amount == 0:
            if level > 2:
                stack_amount = random.randint(1,5)

                if stack_verticle:
                    stack_verticle = 0
                else:
                    stack_verticle = random.randint(0, 1)

            else:
                stack_amount = 1
                stack_verticle = False

            previous_x += increment
            if previous_x > 13000:
                previous_x = 11000

            if stack_verticle:
                previous_y = random.randint(50, 200)
            else:
                previous_y = random.randint(50,500)

        if stack_verticle:
            previous_y += 65
            tile.set_coordinates(previous_x, previous_y)
        else:
            previous_x += 65
            tile.set_coordinates(previous_x, previous_y)


        if stack_verticle:
            if stack_amount > 1:
                tile.value = 1

        tiles.add(tile)
        stack_amount -= 1


    while overlapping:

        num = 0

        for tile1 in tiles:
            for tile2 in tiles:
                if tile1.pos != tile2.pos:
                    if abs(tile1.rect.y - tile2.rect.y) < 65:
                        if abs(tile1.rect.x - tile2.rect.x) < 65:
                            if tile1.rect.y > tile2.rect.y:
                                tile1.rect.y += 65
                            else:
                                tile2.rect.y += 65

                            if tile1.rect.x > tile2.rect.x:
                                tile1.rect.x += 65
                            else: tile2.rect.x += 65


                            num = 1

            if num == 0:
                overlapping = False

def generate_bullets():
    global bullet, bullet_count, bullet_pos_x
    for i in range(0, bullet_count):
        bullet_pos_x += 25
        bullet.add(Bullet(bullet_pos_x, i+1))

def create_background():
    global image, image_rect, background, background_rect, castle, castle_rect, castle2, castle_rect2, color1, color2, door, level
    if level == 1:
        color1 = generate_color()
        color2 = generate_color()

    else:
        castle = castle2.copy()
        color2 = generate_color()

    image = pygame.image.load("images/ground.jpg")
    image_rect = image.get_rect(topleft=(0, 400))

    background = pygame.image.load("images/ground.jpg")

    background = pygame.transform.scale(background, (14000, 100))
    background_rect = background.get_rect(topleft=(0, 950))

    if level == 1:
        castle = pygame.image.load("images/castle.jpg")
        castle.fill(color1, special_flags=pygame.BLEND_RGB_ADD)
        castle = pygame.transform.rotozoom(castle, 0, 2)

        castle2 = castle.copy()
    else:
        castle2 = pygame.image.load("images/castle.jpg")
        castle2 = pygame.transform.rotozoom(castle2, 0, 2)


    castle2.fill(color2, special_flags=pygame.BLEND_RGB_ADD)

    castle_rect = castle.get_rect(bottomleft=(-30, 970))
    castle_rect2 = castle.get_rect(bottomleft=(13018, 970))

    door.sprite.rect = door.sprite.image.get_rect(center = (13525,900))


def generate_color():
    l = []
    for i in range(1,4):
        l.append(random.randint(0,150))

    if min(l) > 50:
        num = random.randint(0,2)
        l[num] = random.randint(0,40)
    return (l[0],l[1],l[2], 50)

def change_background_color():
    global red, green, blue, color_chosen, choice

    if not color_chosen:
        choice = random.randint(1, 3)

    if choice == 1:
        if red < 255:
            red += 1
        else:
            color_chosen = False
    if choice == 2:
        if green < 255:
            green += 1
        else:
            color_chosen = False
    if choice == 3:
        if blue < 255:
            blue += 1
        else:
            color_chosen = False


    if 180 < min(red,green,blue):
        l = [1,2,3]
        num = random.randint(1,3)
        l.remove(num)

        if 1 in l:
            red = 50
        if 2 in l:
            green = 50
        if 3 in l:
            blue = 50

def blit():
    screen.blit(background, background_rect)
    screen.blit(castle, castle_rect)
    screen.blit(castle2,castle_rect2)

def add_x(x):
    global background_rect, castle_rect, tiles, door
    background_rect.x += x
    castle_rect.x += x
    castle_rect2.x += x
    door.sprite.rect.x += x

    for tile in tiles:
        tile.rect.x += x

def move():
    global player, x, castle_rect, castle_rect2

    for p in player:
        if not p.on_the_ground:
            if p.rect.y >= 880:
                p.on_the_ground = True
                p.gravity = 0
                p.rect.y = 880
            else:
                p.gravity += .1
                p.rect.y += p.gravity

        keys = pygame.key.get_pressed()
        p.moving = False

        if keys[pygame.K_LEFT]:
            p.right = False
            p.moving = True
            if p.rect.x > 100:
                p.rect.x -= 10
            else:
                if castle_rect.x < -30:
                    add_x(10)

        if keys[pygame.K_RIGHT]:
            p.right = True
            p.moving = True
            if not castle_rect2.x < 1100:
                add_x(-10)
                if not p.rect.x > 1800:
                    p.rect.x += 1
            elif p.rect.x < 1960:
                p.rect.x += 10

        if keys[pygame.K_UP]:
            if p.on_the_ground and p.released:
                p.rect.y -= 200
                p.gravity = 0
                p.on_the_ground = False
                p.released = False
        else:
            p.released = True

def next_level():
    global door, player, tiles, castle, castle2, level, bullet, bullet_count, bullet_pos_x, released, score
    if pygame.sprite.spritecollide(player.sprite, door, False):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet_pos_x = 0
            released = False
            score += level * 500
            level += 1
            bullet_count = 5 + int(level/5)
            tiles.empty()
            bullet.empty()
            player.sprite.rect = player.sprite.image.get_rect(topleft = (200,880))

            create_background()
            generate_tiles()
            generate_bullets()

def shoot():
    global player, door, bullet, bullet_count, released, tiles, level, score

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if released:
            if not pygame.sprite.spritecollide(player.sprite, door, False):
                if bullet_count > 0:
                    for b in bullet:
                        if b.value == bullet_count:
                            b.shoot(player.sprite.rect.x,player.sprite.rect.y, player.sprite.right)
                            bullet_count -= 1
                released = False
    else: released = True

    for b in bullet:
        if b.moving:
            if pygame.sprite.spritecollide(b, tiles, True):
                score += 100 + level * 5
                b.kill()






create_background()
generate_tiles()
generate_bullets()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    reset()
                    game_active = True

    if game_active:
        change_background_color()
        screen.fill((red,green,blue, 50))
        blit()

        player.draw(screen)
        player.update()

        tiles.draw(screen)
        tiles.update(player.sprite.rect)

        door.draw(screen)
        display_score()

        bullet.draw(screen)
        bullet.update()

        next_level()

        move()

        shoot()

        game_active = not pygame.sprite.spritecollide(player.sprite,tiles, False)



    else:
        screen.fill((0, 0, 0))
        title_screen()


    pygame.display.update()

    frame_rate.tick(60)



