from .external import pygame

def joinimages(*images, dir='horizontal'):
    if not dir.startswith('h'):
        raise NotImplementedError
    rects = [image.get_rect() for image in images]
    for rect1, rect2 in pairwise(rects):
        rect2.left = rect1.right
    width = rects[-1].right - rects[0].left
    height = max(rect.height for rect in rects)
    result = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    for rect, image in zip(rects, images):
        result.blit(image, rect)
    return result

def preview(path, size):
    try:
        image = pygame.image.load(path)
    except pygame.error:
        image = None
    else:
        rect = fitrect(image.get_rect(), image.get_rect(size=size))
        image = pygame.transform.scale(image, rect.size)
    return image
