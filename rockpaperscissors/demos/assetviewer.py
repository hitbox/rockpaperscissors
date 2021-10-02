from .external import pygame

KENNYDIR = Path('/home/hitbox/Documents/Kenney Game Assets/Kenney Game Assets 3 version 28')
KENNYSPRITES = KENNYDIR / '2D assets'
KENNYFONT = KENNYDIR / 'Other/Fonts/Kenney Pixel.ttf'

def assetsviewer():
    pygame.font.init()
    display = Display((800, 800), scale=1)
    #
    font = pygame.font.Font(KENNYFONT, 20)
    assets = Assets(KENNYSPRITES)
    assetsviewer = AssetsViewer(assets, font)
    _newroot = None
    assetsviewer.update()
    highlight = None
    imageview = None
    clock = Clock()

    size = (15,15)
    button_scale_up = Sprite(draw.triangle(size, (200,200,200), 'midtop'))
    button_scale_up.rect.topright = display.rect.topright

    sep = font.size(' ')

    button_scale_down = Sprite(draw.triangle(size, (200,200,200), 'midbottom'))
    button_scale_down.rect.centerx = button_scale_up.rect.centerx
    button_scale_down.rect.top = button_scale_up.rect.bottom + sep[1]

    image_scale = 1

    def update_highlight():
        nonlocal highlight
        if assetsviewer.sprites:
            pos = tuple(x // display.scale for x in event.pos)
            for sprite in assetsviewer.sprites:
                if sprite.rect.collidepoint(pos):
                    highlight = sprite
                    break
            else:
                highlight = None

    running = True
    while running:
        elapsed = clock.tick()
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.MOUSEMOTION:
                update_highlight()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if highlight:
                    if highlight.path.is_dir():
                        _newroot = highlight.path
                    elif highlight.path.is_file():
                        try:
                            imageview = pygame.image.load(highlight.path)
                        except pygame.error:
                            pass
                pos = tuple(x // display.scale for x in event.pos)
                if button_scale_up.rect.collidepoint(pos):
                    image_scale += 1
                elif button_scale_down.rect.collidepoint(pos):
                    if image_scale > 1:
                        image_scale -= 1
        # draw
        display.clear()
        image = font.render(f'scale: {image_scale}', False, (200,200,200))
        display.surface.blit(image, image.get_rect(topright=button_scale_up.rect.bottomright))
        display.surface.blit(button_scale_up.image, button_scale_up.rect)
        display.surface.blit(button_scale_down.image, button_scale_down.rect)
        for sprite in assetsviewer.sprites:
            display.surface.blit(sprite.image, sprite.rect)
        if highlight:
            rect = highlight.rect.inflate(8,4)
            pygame.draw.rect(display.surface, (200,10,10), rect, 1)
        if imageview:
            image = pygame.transform.scale(imageview, tuple(x*image_scale for x in imageview.get_size()))
            r1 = image.get_rect()
            rect = fitrect(r1, display.rect)
            rect.midright = display.rect.midright
            display.surface.blit(image, rect)
        display.update()
        #
        if _newroot:
            assets = Assets(_newroot)
            assetsviewer = AssetsViewer(assets, font)
            assetsviewer.update()
            _newroot = None
            update_highlight()
