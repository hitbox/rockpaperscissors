from ..display import Display

def fitrect():
    "Demo fitting one rect inside another"
    display = Display((300, 200), scale=4)
    #
    clock = Clock()
    rect1 = pygame.Rect(40,10,150,130)
    rect2 = pygame.Rect(40,10,145,145)
    rect3 = fitrect(rect1, rect2)
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
        display.clear()
        #display.surface.blit(image, (0,0))
        pygame.draw.rect(display.surface, (200,10,10), rect1, 1)
        pygame.draw.rect(display.surface, (10,200,10), rect2, 1)
        pygame.draw.rect(display.surface, (10,10,200), rect3, 1)
        display.update()
