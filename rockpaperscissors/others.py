def scale(container, value):
    type_ = type(container)
    return type_(v*value for v in container)

class Loop:
    """
    Update current state in loop and manage switching states.
    """

    def __init__(self):
        self.running = False
        self.state = None
        self.nextstate = None

    def run(self, state):
        self.state = state
        self.running = True
        while self.running:
            self.state.update()
            if self.nextstate:
                self.state = self.nextstate
                self.nextstate = None

    def stop(self):
        self.running = False

    def switch(self, state):
        self.nextstate = state


class Assets:

    def __init__(self, root):
        self.root = Path(root)
        self.current = self.root

    def iterdir(self):
        return self.current.iterdir()


class Sprite:

    def __init__(self, image, rect=None):
        self.image = image
        if rect is None:
            rect = self.image.get_rect()
        self.rect = rect


class AssetSprite:

    def __init__(self, path, font, name=None):
        self.path = path
        self.font = font
        self.image = None
        self.rect = None
        self.update(name)

    def update(self, name=None):
        icon = preview(self.path, self.font.size(' '))
        if name is None:
            name = self.path.name
        name = self.font.render(name, False, (200,200,200))
        if icon:
            image = joinimages(name, icon)
        else:
            image = name
        self.image = image
        self.rect = self.image.get_rect()


class AssetsViewer:

    def __init__(self, assets, font):
        self.assets = assets
        self.font = font
        self.sprites = None

    def update(self):
        parent = AssetSprite(self.assets.current.parent, self.font, name='..')
        self.sprites = [parent]
        for path in self.assets.iterdir():
            sprite = AssetSprite(path, self.font)
            self.sprites.append(sprite)
        if self.sprites:
            maxwidth = max(sprite.rect.width for sprite in self.sprites)
            for sprite1, sprite2 in pairwise(self.sprites):
                sprite1.rect.width = maxwidth
                sprite2.rect.width = maxwidth
                sprite2.rect.top = sprite1.rect.bottom
