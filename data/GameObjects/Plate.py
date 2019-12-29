import pygame
from ..editor import *

class Plate(pygame.sprite.Sprite):
    def __init__(self, x,y,w,h, color = (255,0,0), linked_to_id = -1):
        super().__init__()
        self.org_rect = pygame.Rect(int(x),int(y),int(w),int(h))
        self.rect = pygame.Rect(x,y,w,30)
        self.color = color
        self.collide = False
        self.linked_to_id = linked_to_id
        self.linked_to = None
        self.players_on = []
        self.image = pygame.Surface((w,h))
        self.image.fill(self.color)

    def update(self, cam = None):
        if cam:
            self.rect = pygame.Rect(*(cam.get_offset(self.org_rect)))
            self.image = pygame.Surface((self.rect.w,self.rect.h))
            self.image.fill(self.color)

    def outline(self, surface, camera):
        border = (self.rect[0] - 5,self.rect[1] - 5,self.rect[2] + 10,self.rect[3] + 10)
        color = invert_color(self.color)
        camera.draw_rect(surface,color,border)

    def move(self, dx,dy,zoom,ratio):
        self.org_rect = pygame.Rect(self.org_rect[0] + dx * (1 / zoom) * ratio[0],
                                    self.org_rect[1] + dy * (1 / zoom) * ratio[1],
                                    self.org_rect[2], self.org_rect[3])

    def has_collision(self, player_id):
        return self.collide

    def get_properties(self):
        return ["Linker"]

    def on_collision(self, collider):
        if not self.players_on: #s'il n'y a aucun joueur sur la plaque
            self.linked_to.switch_status()
        if not collider in self.players_on:
            self.players_on.append(collider)

    def on_collision_exit(self, collider):
        print('exit')
        self.players_on.remove(collider)
        if not self.players_on:
            self.linked_to.switch_status()

    def as_string(self):
        rect_int = [ int(self.org_rect.x), int(self.org_rect.y), int(self.org_rect.w), int(self.org_rect.h) ]
        return 'Plate, {},{},{},{}, {}\n'.format(*rect_int, self.linked_to_id)
