def guimain():
    pygame.display.init()
    #
    buffer = pygame.Surface((800, 800))
    rect = buffer.get_rect()
    area = rect.inflate(-20, -20)
    screen = pygame.display.set_mode(scale(rect.size, 1))
    clock = Clock()
    #
    promptrect = area.inflate(-20, -area.height / 2)
    promptrect.center = area.center
    width = int(promptrect.width // len(Gestures) * .8)
    size = (width, width)

    icons = (gesture.draw(size, (200,200,200)) for gesture in Gestures)
    icons = {image: image.get_rect(left=promptrect.left, top=promptrect.top)
             for image in icons}
    layout_flow(icons.values(), promptrect.width, betweenx=30)

    highlight = None
    #
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
        #
        pos = pygame.mouse.get_pos()
        for rect in icons.values():
            if rect.collidepoint(pos):
                highlight = rect
                break
        else:
            highlight = None
        #
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (200,10,10), promptrect, 1)
        for icon, rect in icons.items():
            screen.blit(icon, rect)
            if highlight is rect:
                color = (200,200,10)
            else:
                color = (200,10,10)
            pygame.draw.rect(screen, color, rect, 1)
        pygame.display.flip()
