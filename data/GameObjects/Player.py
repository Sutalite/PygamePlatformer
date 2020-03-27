import pygame
from pygame.locals import *

from ..utils.utils import clamp
from ..utils.SpriteLoader import load_animation

class Player(pygame.sprite.Sprite):
    def __init__(self, left_key, right_key, jump_key, player_id, rect):
        super().__init__()
        self.rect = rect
        self.size = self.rect.w
        self.grounded = True
        self.mvt = [0,0]
        self.speed = 0.5
        self.gravity = 0.0035
        self.jump_force = self.size / 55

        self.left_key  = left_key
        self.right_key = right_key
        self.jump_key  = jump_key

        self.player_id = player_id
        self.image = pygame.Surface((self.size,self.size), SRCALPHA)

        self.prev_colliders = []

        self.animations = {
                "walking" : load_animation('walker1.png', (64,64), (self.size, self.size), 16, 33)
                # "idle": load_animation(f'player_{self.player_id}_idle.png', (self.size, self.size)),
                # "walking": load_animation(f'player_{self.player_id}_walking.png', (self.size, self.size), 9, 27),
                # "standing": load_animation(f'player_{self.player_id}_standing.png', (self.size, self.size))
        }

        #Looking direction :
        # 0 : left
        # 1 : right
        self.looking_direction = 1

        self.animation_lenght = 1000 #duration of the animation in ms
        self.animation_time = 0 #time since the start of the animation in ms
        self.update_animation(0)


    def move(self, dt):
        self.rect.x += self.mvt[0] * dt
        self.rect.y += self.mvt[1] * dt
        self.rect.x = clamp(self.rect.x, 0, 1920 - self.size)

    def update_animation(self, dt):
        self.image.fill((0,0,0,0))
        self.animation_time = (self.animation_time + dt) % self.animation_lenght
        animation_frame = self.animation_time * len(self.animations['walking']) // self.animation_lenght
        frame_to_blit = self.animations['walking'][animation_frame]
        if self.looking_direction == 0:
            flipped_image = pygame.transform.flip(frame_to_blit, True, False)
            self.image.blit(flipped_image, (0,0))
        if self.looking_direction == 1:
            self.image.blit(frame_to_blit, (0,0))

    def c_update(self, colliders, keys, dt):
        self.update_animation(dt)
        if keys:
            self.move(dt)
            self.mvt[0] = (keys[self.right_key] - keys[self.left_key]) * self.speed
            if self.mvt[0] > 0: self.looking_direction = 1
            if self.mvt[0] < 0: self.looking_direction = 0
        collisions = self.rect.collidelistall(colliders)
        dx = 0
        dy = 0

        for col in self.prev_colliders.copy():
            if not col in collisions: #si le joueur n'a plus de collision avec un objet qu'il touchait avant
                colliders[col].on_collision_exit(self)
                self.prev_colliders.remove(col)


        if len(collisions) > 2:
            for i in collisions:
                col = colliders[i]
                if col == self: #don't collide with itself
                    continue
                if not i in self.prev_colliders:
                    self.prev_colliders.append(i)
                    col.on_collision(self)
                #If the collider is traversable don't check collisions
                if not col.has_collision(self.player_id):
                    continue

                rect = col.rect
                #Collision en dessous du joueur
                if self.collision_bottom(rect):
                    dy -= (self.rect.bottom - rect.top) #Correction pour éviter que le joueur traverse le sol
                    self.grounded = True
                    self.mvt[1] = 0
                elif self.collision_top(rect) and rect.w > self.rect.w:
                    dy -= (self.rect.top - rect.bottom) #Correction pour éviter que le joueur traverse le plafond
                    self.grounded = False
                    self.mvt[1] = 0
                elif self.collision_right(rect):
                    self.mvt[0] = 0
                    #check if only the topright corner is colliding in order to avoid teleporting
                    #the player when there is no need to
                    tr = rect.collidepoint(self.rect.topright)
                    mr = rect.collidepoint(self.rect.midright)
                    if tr and not mr:
                        continue
                    dx -= (self.rect.right - rect.left)
                elif self.collision_left(rect) and not self.collision_top(rect):
                    self.mvt[0] = 0
                    #check if only the topleft corner is colliding in order to avoid teleporting
                    #the player when there is no need to
                    tl = rect.collidepoint(self.rect.topleft)
                    ml = rect.collidepoint(self.rect.midleft)
                    if tl and not ml:
                        continue
                    dx -= (self.rect.left - rect.right)
        else:
            self.grounded = False

        self.rect.x += dx
        self.rect.y += dy

        if not self.grounded:
            self.mvt[1] += self.gravity * dt

        if keys and keys[self.jump_key] and self.grounded:
            self.mvt[1] -= self.jump_force
            self.grounded = False

    def collision_bottom(self, col):
        bl = col.collidepoint(self.rect.bottomleft)
        bm = col.collidepoint(self.rect.midbottom)
        br = col.collidepoint(self.rect.bottomright)
        ml = col.collidepoint(self.rect.midleft)
        mr = col.collidepoint(self.rect.midright)
        return (bl or br or bm) and not ml and not mr

    def collision_top(self, col):
        tl = col.collidepoint(self.rect.topleft)
        tm = col.collidepoint(self.rect.midtop)
        tr = col.collidepoint(self.rect.topright)
        ml = col.collidepoint(self.rect.midleft)
        mr = col.collidepoint(self.rect.midright)
        return (tl or tr or tm) and not ml and not mr


    def collision_left(self, col):
        t = col.collidepoint(self.rect.topleft)
        m = col.collidepoint(self.rect.midleft)
        b = col.collidepoint(self.rect.bottomleft)
        bm = col.collidepoint(self.rect.midbottom)
        br = col.collidepoint(self.rect.bottomright)
        return (t or m or b) and not bm and not br

    def collision_right(self, col):
        t = col.collidepoint(self.rect.topright)
        m = col.collidepoint(self.rect.midright)
        b = col.collidepoint(self.rect.bottomright)
        bm = col.collidepoint(self.rect.midbottom)
        bl = col.collidepoint(self.rect.bottomleft)
        return (t or m or b) and not bm and not bl

    def has_collision(self, player_id):
        return True

    def on_collision(self, collider):
        return

    def on_collision_exit(self, collider):
        return

    def set_position(self, position):
        self.rect = pygame.Rect(*position, self.size, self.size)