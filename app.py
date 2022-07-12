from copy import copy
from typing import final
from PIL import Image
import pygame, traceback

class Sprite:
    def __init__(self, texture_index: int, x: int, y: int, z: int, tyler):
        self.x, self.y = x, y
        self.z = z

        self.tyler = tyler
        self.texture_index = texture_index

    def draw(self, screen) -> None:
        surface = self.tyler.surfaces[self.texture_index]
        screen.blit(surface, (
            self.x * self.tyler.texture_width,
            self.tyler.height - (self.y + 1) * self.tyler.texture_height
        ))

class Scene:
    def loop(self, delta) -> None:
        pass

    def start(self) -> None:
        pass

    def quit(self) -> None:
        pass

    def event(self, event) -> None:
        pass

    def draw(self) -> None:
        pass

class Tyler:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    FPS = 30
    NAME = "Tyler Application"
    OUTSIDE = None
    DEFAULT_TEXTURE_NAME = "default.png"
    OUTSIDE_TEXTURE_NAME = "default.png"
    DEFAULT_SCENE_NAME = "main"

    TEXTURE_NAMES = [
        "default.png"
    ]

    @final
    def int_to_xy(self, x: int) -> tuple[int, int]:
        return (x % self.tile_h, x // self.tile_h)

    @final
    def xy_to_int(self, x: int, y: int) -> int:
        return y * self.tile_h + x

    @final
    def get_tile(self, x: int, y: int) -> Sprite:
        try:
            if x < 0 or x >= self.tile_w or y < 0 or y >= self.tile_w:
                raise IndexError

            return self.tiles[self.xy_to_int(x, y)]
        except IndexError:
            return self.OUTSIDE

    @final
    def set_tile(self, x: int, y: int, sprite: Sprite) -> None:
        self.tiles[self.xy_to_int(x, y)] = sprite

    @final
    def gen_tiles(self, texture_index: int) -> None:
        self.tiles = [Sprite(texture_index, self.int_to_xy(x)[0], self.int_to_xy(x)[1], -1, self) for x in range(self.tile_w * self.tile_h)]

    @final
    def texture(self, texture_name: str) -> int:
        return self.TEXTURE_NAMES.index(texture_name)

    @final
    def load_scene(self, name: str) -> None:
        self.scene = self.scenes[name]

        self.scene.start()

    @final
    def __init__(self, width: int, height: int, tile_w: int, tile_h: int, scenes: dict[str, Scene]):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

        self.width = width
        self.height = height
        self.tile_w = tile_w
        self.tile_h = tile_h

        self.texture_width = width // tile_w
        self.texture_height = height // tile_h
        self.do_run = True
        self.fps_check = 5

        self.tiles_draw = []
        self.sprites: dict[str, Sprite] = {}
        self.textures = [Image.open(name).resize((self.texture_width, self.texture_height)) for name in self.TEXTURE_NAMES]
        self.surfaces = [pygame.image.fromstring(texture.tobytes(), texture.size, texture.mode).convert() for texture in self.textures]
        self.old_tiles = [] # don't touch

        self.gen_tiles(self.texture(self.DEFAULT_TEXTURE_NAME))
        self.OUTSIDE = Sprite(self.texture(self.OUTSIDE_TEXTURE_NAME), -1, -1, -9999, self)

        pygame.display.set_caption(self.NAME)
        self.clock = pygame.time.Clock() # For syncing the FPS

        self.scenes = scenes
        for scene_name in self.scenes:
            self.scenes[scene_name].tyler = self
        self.load_scene(self.DEFAULT_SCENE_NAME)

    @final
    def update(self) -> None:
        delta = self.clock.tick(self.FPS) / 1000 # will make the loop run at the same speed all the time
        self.fps_check += 1 * delta
        if self.fps_check >= 2:
            print(f"FPS: {round(1/delta, 1)}")
            self.fps_check = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.do_run = False

            self.scene.event(event)

        self.screen.fill(self.BLACK)
        self.scene.loop(delta)

        def get_sort_value(sprite: Sprite) -> int:
                return sprite.z

        # draw sprites
        if self.tiles != self.old_tiles: # regenerate
            self.tiles_draw = self.tiles

            # sort
            self.tiles_draw.sort(key=get_sort_value)

        sorted_sprites: list[Sprite] = []
        for key in self.sprites: sorted_sprites.append(copy(self.sprites[key]))
        sorted_sprites.sort(key=get_sort_value)

        for sprite in self.tiles_draw: sprite.draw(self.screen)
        for sprite in sorted_sprites: sprite.draw(self.screen)

        self.old_tiles = [copy(x) for x in self.tiles]

        self.scene.draw()
        pygame.display.flip()

    @final
    def run(self) -> None:
        try:
            while self.do_run:
                self.update()
        except Exception as e:
            print(traceback.format_exc())
        
        self.scene.quit()
        pygame.quit()
        print("Goodbye!")