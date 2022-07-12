import pygame
from app import Sprite, Tyler

class Dummy(Tyler):
    NAME = "Dummy"
    TEXTURE_NAMES = [
        "default.png",
        "gorilla.jpg"
    ]

    def start(self) -> None:
        self.sprites["gorilla"] = Sprite(self.texture("gorilla.jpg"), 1, 1, 10, self)

    def loop(self, delta) -> None:
        self.sprites["gorilla"].x += 1 * delta

dummy: Dummy = Dummy(800, 800, 8, 8)
dummy.run()