import pygame
import random
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = self.generate_frames()
        self.rect = self.image.get_rect(topleft = (500,880))

        self.on_the_ground = True
        self.released = False
        self.gravity = 0
        self.time = 0
        self.right = True
        self.moving = False


    def generate_frames(self):
        walk1 = pygame.image.load("images/player/walk1.jpg").convert_alpha()
        walk1 = pygame.transform.rotozoom(walk1, 0, 1.5)

        walk2 = pygame.image.load("images/player/walk2.jpg").convert_alpha()
        walk2 = pygame.transform.rotozoom(walk2, 0, 1.5)

        walk3 = pygame.image.load("images/player/walk3.jpg").convert_alpha()
        walk3 = pygame.transform.rotozoom(walk3, 0, 1.5)

        walk4 = pygame.image.load("images/player/walk4.jpg").convert_alpha()
        walk4 = pygame.transform.rotozoom(walk4, 0, 1.5)

        self.image = walk1

        return [walk3, walk1, walk2, walk4]



    def animation(self):
        if self.moving:
            self.time += .2
            if self.time > len(self.frames):
                self.time = 0
            self.image = self.frames[int(self.time)]
        else:
            self.image = self.frames[3]

        if not self.on_the_ground:
            self.image = self.frames[2]


        if not self.right:
         self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.animation()


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.generate_image()
        self.started = False
        self.go_to_origin = False
        self.x = random.randint(5,15)
        self.y = random.randint(5,10)
        self.origin_y = 0

        self.value = 0

    def generate_image(self):
        num = random.randint(1,11)
        images = {
            1: pygame.image.load("images/tiles/blue.jpg").convert_alpha(),
            2: pygame.image.load("images/tiles/darkgray.jpg").convert_alpha(),
            3: pygame.image.load("images/tiles/gray.jpg").convert_alpha(),
            4: pygame.image.load("images/tiles/green.jpg").convert_alpha(),
            5: pygame.image.load("images/tiles/lightblue.jpg").convert_alpha(),
            6: pygame.image.load("images/tiles/orange.jpg").convert_alpha(),
            7: pygame.image.load("images/tiles/pink.jpg").convert_alpha(),
            8: pygame.image.load("images/tiles/purple.jpg").convert_alpha(),
            9: pygame.image.load("images/tiles/red.jpg").convert_alpha(),
            10: pygame.image.load("images/tiles/red2.jpg").convert_alpha(),
            11: pygame.image.load("images/tiles/white.jpg").convert_alpha(),
        }
        self.image = images[num]
        self.rect = self.image.get_rect(center = (0,0))

    def set_coordinates(self, x, y):
        self.rect.x = x
        self.origin_y = y
        self.rect.y = y

    def move(self, rect):
        if self.go_to_origin:
            if self.origin_y >= self.rect.y:
                self.y *= -1
                self.x *= -1
                self.started = False
                self.go_to_origin = False
            else:
                self.rect.y += self.y
                self.rect.x += self.x
        else:
            if not self.started:
                if self.value == 1:
                    if rect.x < self.rect.x:
                        self.x *= -1
                    self.y = abs(self.x)
                else:
                    self.x = 0


                self.started = True

            else:
                if self.rect.y >= 889:
                    self.x *= -1
                    self.y *= -1
                    self.started = False
                    self.go_to_origin = True
                else:
                    self.rect.x += self.x
                    self.rect.y += self.y

    def update(self, rect):
        self.move(rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

class Door(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Door.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,120))
        self.rect = self.image.get_rect(center = (13525,900))
        self.image.fill((0,0,0,0))

class Bullet(pygame.sprite.Sprite):
    def generate_color(self):
        l = []
        for i in range(1, 4):
            l.append(random.randint(0, 150))

        if min(l) > 50:
            num = random.randint(0, 2)
            l[num] = random.randint(0, 40)
        return (l[0], l[1], l[2], 50)

    def __init__(self, x, value):
        super().__init__()
        self.value = value
        self.moving = False
        self.speed = 10

        self.image = pygame.image.load("images/bullet.jpg").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .07)


        self.color = self.generate_color()
        self.image.fill(self.color, special_flags=pygame.BLEND_RGB_ADD)
        self.rect = self.image.get_rect(center = (x,50))

    def move(self):
        if self.moving:
            self.rect.x += self.speed

        if self.speed > 0:
            if self.rect.x > 14000:
                self.kill()
        else:
            if self.rect.x < -1000:
                self.kill()
    def shoot(self, x, y, right):
        self.image = pygame.transform.rotozoom(self.image, 0, .4)

        if right:
            self.image = pygame.transform.rotate(self.image, -90)
        else:
            self.speed *= -1
            self.image = pygame.transform.rotate(self.image, 90)


        self.rect.x = x + 40
        self.rect.y = y + 55


        self.moving = True

    def update(self):
        self.move()



