import pygame
from app import Tyler, Scene, Sprite

class Dummy(Tyler):
    NAME = "Dummy"
    DEFAULT_SCENE_NAME = "title_screen"
    TEXTURE_NAMES = [
        "default.png",
        "transparent.png",
        "gorilla.jpg",
        "press_any_key.png",
        "burger.jpg",
        "capuchin.png"
    ]

class TitleScreen(Scene):
    tyler: Tyler # only for vs to help with autocompletion

    def start(self) -> None:
        self.tyler.get_tile(self.tyler.background, 1, 1).texture_index = self.tyler.texture("press_any_key.png")

    def event(self, event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                self.tyler.load_scene("main")

class Main(Scene):
    tyler: Tyler

    def start(self) -> None:
        self.tyler.gen_tiles(self.tyler.background, self.tyler.texture("burger.jpg"))

        self.tyler.sprites["gorilla"] = Sprite(self.tyler.texture("gorilla.jpg"), 1, 1, 10, self.tyler)
        self.tyler.sprites["capuchin"] = Sprite(self.tyler.texture("capuchin.png"), 1, 3, 10, self.tyler)

    def loop(self, delta) -> None:
        self.tyler.sprites["gorilla"].x += 1 * delta
        self.tyler.sprites["capuchin"].x += .5 * delta

dummy: Dummy = Dummy(800, 800, 8, 8, {
    "title_screen": TitleScreen(),
    "main": Main()
})
dummy.run()