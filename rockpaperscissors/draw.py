from .external import pygame

def rock(size, linecolor):
    image = pygame.Surface(size, flags=pygame.SRCALPHA)
    rect = image.get_rect()
    radius = min(rect.size) * .5
    points = []
    var = min(rect.size) // 16
    var = cycle([var,-var])
    for angle in range(0, 360, 30):
        angle = math.radians(angle)
        r = radius + next(var)
        x = rect.centerx + math.cos(angle) * r
        y = rect.centery + math.sin(angle) * r
        points.append((x,y))
    pygame.draw.polygon(image, linecolor, points)
    return image

def paper(size, color):
    image = pygame.Surface(size, flags=pygame.SRCALPHA)
    rect = image.get_rect()
    points = [
        rect.topleft,
        (rect.width * 0.8, rect.top),
        (rect.width, rect.height * 0.2),
        rect.bottomright,
        rect.bottomleft,
    ]
    pygame.draw.polygon(image, color, points)
    return image

def scissors(size, linecolor):
    image = pygame.Surface(size, flags=pygame.SRCALPHA)
    rect = image.get_rect()
    area = rect.copy()
    points = [
        (area.width * .35, area.centery * 1.1),
        (area.width * .20, area.top),
        area.center,
        (area.width - (area.width * .20), area.top),
        (area.width - (area.width * .35), area.centery * 1.1),
    ]
    pygame.draw.polygon(image, linecolor, points, 1)
    #
    center = (area.width * .2, area.height * .8)
    radius = min(size) // 6
    width = min(size) // 16
    pygame.draw.circle(image, linecolor, center, radius, width)
    center = (area.width * .8, area.height * .8)
    pygame.draw.circle(image, linecolor, center, radius, width)
    return image


def triangle(size, color, attr, width=1):
    othermap = {
        'midtop': ['bottomright', 'bottomleft'],
        'midright': ['bottomleft', 'topleft'],
        'midbottom': ['topleft', 'topright'],
        'midleft': ['topright', 'bottomright'],
    }
    rect = pygame.Rect((0,0), size)
    points = [getattr(rect, attr)]
    for otherattr in othermap[attr]:
        other = list(getattr(rect, otherattr))
        if 'right' in otherattr:
            other[0] -= 1
        if 'bottom' in otherattr:
            other[1] -= 1
        points.append(other)
    result = pygame.Surface(size, flags=pygame.SRCALPHA)
    pygame.draw.polygon(result, color, points, width)
    return result


