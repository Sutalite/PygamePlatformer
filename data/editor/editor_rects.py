import pygame

class DragRect(pygame.sprite.Sprite):
    def __init__(self, x,y,w,h, color):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = color
        self.image = pygame.Surface((w,h))

    def draw(self,camera,surface):
        camera.draw_rect(surface, self.color, self.rect)

def get_corner_point(rect, point):
    pr = pygame.Rect(rect)
    sub_rects = [
            pygame.Rect(pr.x, pr.y, pr.w / 2, pr.h / 2),
            pygame.Rect(pr.x + pr.w / 2, pr.y, pr.w / 2, pr.h / 2),
            pygame.Rect(pr.x, pr.y + pr.h / 2, pr.w / 2, pr.h / 2),
            pygame.Rect(pr.x + pr.w / 2, pr.y + pr.h / 2, pr.w / 2, pr.h / 2)
            ]
    for i, sr in enumerate(sub_rects):
        if sr.collidepoint(point):
            return i

def resize_rect(rect, corner, dx,dy, zoom):
    AREA_LIMIT = 2000
    new_rect = None
    if corner == 0:
        new_rect = (rect[0] + dx * (1 / zoom),
                    rect[1] + dy * (1 / zoom),
                    rect[2] - dx * (1 / zoom),
                    rect[3] - dy * (1 / zoom))

    elif corner == 1:
        new_rect = (rect[0],
                    rect[1] + dy * (1 / zoom),
                    rect[2] + dx * (1 / zoom),
                    rect[3] - dy * (1 / zoom))

    elif corner == 2:
        new_rect = (rect[0] + dx * (1 / zoom),
                    rect[1],
                    rect[2] - dx * (1 / zoom),
                    rect[3] + dy * (1 / zoom))

    elif corner == 3:
        new_rect = (rect[0],
                    rect[1],
                    rect[2] + dx * (1 / zoom),
                    rect[3] + dy * (1 / zoom))
    area = new_rect[2] * new_rect[3]
    if area < AREA_LIMIT:
        return rect
    return pygame.Rect(new_rect)

def inside_rect(rects, mouse_position, camera):
    for i,r in enumerate(rects.sprites()):
        if r.selectable == False: continue
        if pygame.Rect(r.rect).collidepoint(camera.screen_to_world(mouse_position)):
            return i
    return -1

def create_rect(rect_start, mouse_end, obj):
    size = ((mouse_end[0] - rect_start[0]), (mouse_end[1] - rect_start[1]))
    r = obj(*rect_start, *size, color=(255,0,0))

    if abs(r.rect[2]) < 16 or abs(r.rect[3]) < 16:
        print ("The rect is too smol")
        return None

    rr = r.rect
    #bottom left
    if rr[2] > 0 and rr[3] < 0:
        rr = (rr[0], rr[1] + rr[3], rr[2], abs(rr[3]))
    #bottom right
    if rr[2] < 0 and rr[3] < 0:
        rr = (rr[0] + rr[2], rr[1] + rr[3], abs(rr[2]), abs(rr[3]))
    #top right
    if rr[2] < 0 and rr[3] > 0:
        rr = (rr[0] + rr[2], rr[1], abs(rr[2]), rr[3])

    r.rect = rr
    return r