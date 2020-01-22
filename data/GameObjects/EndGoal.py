import pygame
from data.editor import *

class EndGoal(pygame.sprite.Sprite):
    def __init__(self, x,y, w,h, color = (150,100,200)):
        super().__init__()
        size = (150,30)
        self.org_rect = pygame.Rect(x,y,*size)
        self.rect = self.org_rect.copy()
        self.color = color
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.players_on = []
        self.collide = False
        self.selectable = True
        self.level_manager = None

    def update(self, cam = None):
        if cam:
            self.rect = pygame.Rect(*(cam.get_offset(self.org_rect)))
            self.image = pygame.Surface((self.rect.w,self.rect.h))
            self.image.fill(self.color)

    def has_collision(self, player_id):
        return self.collide

    def get_properties(self):
        return []

    def outline(self, surface, camera):
        border = (self.rect[0],self.rect[1],self.rect[2],self.rect[3])
        color = invert_color(self.color)
        camera.draw_rect(surface, color, border, 5)

    def move(self, mp, drag_start, constraint):
        if constraint == "vertical":
            self.org_rect.x = self.before_drag[0] + mp[0] - drag_start[0]
        elif constraint == "horizontal":
            self.org_rect.y = self.before_drag[1] + mp[1] - drag_start[1]
        else:
            self.org_rect.x = self.before_drag[0] + mp[0] - drag_start[0]
            self.org_rect.y = self.before_drag[1] + mp[1] - drag_start[1]

    def on_collision(self, collider):
        if not collider in self.players_on:
            self.players_on.append(collider)
        if len(self.players_on) == 2:
            self.level_manager.end_game()

    def on_collision_exit(self, collider):
        self.players_on.remove(collider)

    def as_string(self):
        rect_int = [ int(self.org_rect.x), int(self.org_rect.y), int(self.org_rect.w), int(self.org_rect.h) ]
        return 'Goal, {},{},{},{}\n'.format(*rect_int)
