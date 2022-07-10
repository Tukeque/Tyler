import pygame
from app import Sprite, Tyler

class Dummy(Tyler):
    NAME = "Dummy"

    def start(self) -> None:
        gorilla_index = self.add_texture("gorilla.jpg")

        self.sprites["gorilla"] = Sprite(gorilla_index, 4, 4, 10, self)

    def loop(self, delta) -> None:
        self.sprites["gorilla"].x += 1 * delta
        pass

dummy: Dummy = Dummy(800, 800, 20, 20)
dummy.run()