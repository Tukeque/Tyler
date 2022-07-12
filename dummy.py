import pygame
from app import Tyler, Scene, Sprite

class Dummy(Tyler):
    NAME = "Dummy"
    DEFAULT_SCENE_NAME = "title_screen"
    TEXTURE_NAMES = [
        "default.png",
        "gorilla.jpg",
        "press_any_key.png",
        "burger.jpg"
    ]

class TitleScreen(Scene):
    tyler: Tyler # only for vs to help with autocompletion

    def start(self) -> None:
        self.tyler.get_tile(1, 1).texture_index = self.tyler.texture("press_any_key.png")

    def event(self, event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                self.tyler.load_scene("main")

class Main(Scene):
    tyler: Tyler

    def start(self) -> None:
        self.tyler.gen_tiles(self.tyler.texture("burger.jpg"))
        self.tyler.sprites["gorilla"] = Sprite(self.tyler.texture("gorilla.jpg"), 1, 1, 10, self.tyler)

    def loop(self, delta) -> None:
        self.tyler.sprites["gorilla"].x += 1 * delta

dummy: Dummy = Dummy(800, 800, 8, 8, {
    "title_screen": TitleScreen(),
    "main": Main()
})
dummy.run()