import pygame
from app import Tyler, Scene, Sprite

class Dummy(Tyler):
    NAME = "Dummy"
    DEFAULT_SCENE_NAME = "title_screen"
    TEXTURE_DATA = [
        ("default.png", 1, 1),
        ("transparent.png", 1, 1),
        ("press_any_key.png", 1, 1),
        ("burger.jpg", 1, 1),
        ("capuchin.png", 2, 1.5),
        ("gorilla.png", 1, 1)
    ]

class TitleScreen(Scene):
    tyler: Tyler # only for vs to help with autocompletion

    def start(self) -> None:
        self.tyler.CLEAR_COLOR = (0xff, 0xff, 0xff)

        self.tyler.fill(self.tyler.backgrounds[0], self.tyler.texture("default.png"))
        self.tyler.get_tile(self.tyler.backgrounds[0], 1, 1).texture_index = self.tyler.texture("press_any_key.png")

    def draw(self) -> None:
        self.tyler.draw(0, 0, 0)

    def event(self, event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                self.tyler.load_scene("main")

class Main(Scene):
    tyler: Tyler

    def start(self) -> None:
        self.tyler.CLEAR_COLOR = (0, 0, 0)

        self.tyler.fill(self.tyler.backgrounds[0], self.tyler.texture("burger.jpg"))
        for i in range(self.tyler.tile_w):
            self.tyler.get_tile(self.tyler.foreground, i, self.tyler.tile_h - 1).texture_index = self.tyler.texture("default.png")

        self.tyler.sprites["gorilla"] = Sprite(self.tyler.texture("gorilla.png"), 1, 1, 10, self.tyler, 0, 0, -1)
        self.tyler.sprites["capuchin"] = Sprite(self.tyler.texture("capuchin.png"), 1, 3, 10, self.tyler)
        self.tyler.sprites["gorilla"].DO_ROTATION = True

    def draw(self) -> None:
        self.tyler.draw(0, 0, 0)

    def loop(self, delta) -> None:
        self.tyler.sprites["capuchin"].x += .5 * delta
        self.tyler.sprites["gorilla"].r += 90 * delta

dummy: Dummy = Dummy(800, 800, 8, 8, {
    "title_screen": TitleScreen(),
    "main": Main()
})
dummy.run()