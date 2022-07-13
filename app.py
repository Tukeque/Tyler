from copy import copy
from typing import final
import pygame, traceback

class Sprite:
    def __init__(self, texture_index: int, x: int, y: int, z: int, tyler):
        self.x, self.y = x, y
        self.z = z

        self.tyler = tyler
        self.texture_index = texture_index

    def draw(self, screen: pygame.Surface) -> None:
        surface = self.tyler.textures[self.texture_index]
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
    FPS = 30
    NAME = "Tyler Application"
    OUTSIDE = None
    DEFAULT_TEXTURE_NAME = "default.png"
    OUTSIDE_TEXTURE_NAME = "default.png"
    TRANSPARENT_TEXTURE_NAME = "transparent.png"
    DEFAULT_SCENE_NAME = "main"

    TEXTURE_DATA = [
        ("default.png", 1, 1),
        ("transparent.png", 1, 1)
    ]

    @final
    def int_to_xy(self, x: int) -> tuple[int, int]:
        return (x % self.tile_h, x // self.tile_h)

    @final
    def xy_to_int(self, x: int, y: int) -> int:
        return y * self.tile_h + x

    @final
    def get_tile(self, tiles: list[Sprite], x: int, y: int) -> Sprite:
        try:
            if x < 0 or x >= self.tile_w or y < 0 or y >= self.tile_w:
                raise IndexError

            return tiles[self.xy_to_int(x, y)]
        except IndexError:
            return self.OUTSIDE

    @final
    def set_tile(self, tiles: list[Sprite], x: int, y: int, sprite: Sprite) -> None:
        tiles[self.xy_to_int(x, y)] = sprite

    @final
    def gen_tiles(self, tiles: list[Sprite], texture_index: int) -> None:
        for i in range(self.length):
            tiles[i] = Sprite(texture_index, self.int_to_xy(i)[0], self.int_to_xy(i)[1], -1, self)

    @final
    def get_sort_value(self, sprite: Sprite) -> int:
        return sprite.z

    @final
    def regenerate(self, draw_tiles, tiles, old_tiles) -> None:
        if tiles != old_tiles: # regenerate
            for i in range(len(tiles)):
                draw_tiles[i] = copy(tiles[i])

            draw_tiles.sort(key=self.get_sort_value)

    @final
    def texture(self, texture_name: str) -> int:
        for i, texture in enumerate(self.TEXTURE_DATA):
            if texture[0] == texture_name:
                return i
        raise Exception(f"Cannot find texture {texture_name}")

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
        self.length = tile_w * tile_h

        self.texture_width = width // tile_w
        self.texture_height = height // tile_h
        self.do_run = True
        self.fps_check = 5

        self.sprites: dict[str, Sprite] = {}
        self.textures = [pygame.transform.scale(pygame.image.load(texture[0]), (self.texture_width * texture[1], self.texture_height * texture[2])) for texture in self.TEXTURE_DATA]

        self.background: list[Sprite] = [None for _ in range(self.length)]
        self.foreground: list[Sprite] = [None for _ in range(self.length)]
        self.draw_background: list[Sprite] = [None for _ in range(self.length)]
        self.draw_foreground: list[Sprite] = [None for _ in range(self.length)]
        self.old_background: list[Sprite] = [] # don't touch
        self.old_foreground: list[Sprite] = [] # don't touch
        
        self.gen_tiles(self.background, self.texture(self.DEFAULT_TEXTURE_NAME))
        self.gen_tiles(self.foreground, self.texture(self.TRANSPARENT_TEXTURE_NAME))
        self.OUTSIDE = Sprite(self.texture(self.OUTSIDE_TEXTURE_NAME), -1, -1, -9999, self)

        pygame.display.set_caption(self.NAME)
        self.clock = pygame.time.Clock() # For syncing the FPS

        self.scenes = scenes
        for scene_name in self.scenes:
            self.scenes[scene_name].tyler = self
        self.load_scene(self.DEFAULT_SCENE_NAME)

    @final
    def update(self) -> None:
        if self.FPS != 0:
            delta = self.clock.tick(self.FPS) / 1000 # will make the loop run at the same speed all the time
        else:
            delta = self.clock.tick() / 1000 # no FPS limit

        self.fps_check += 1 * delta
        if self.fps_check >= 2:
            print(f"FPS: {round(1/delta, 1)}")
            self.fps_check = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.do_run = False

            self.scene.event(event)

        self.screen.fill((0x00, 0x00, 0x00))
        self.scene.loop(delta)

        # background & foreground order
        self.regenerate(self.draw_background, self.background, self.old_background)
        self.regenerate(self.draw_foreground, self.foreground, self.old_foreground)

        self.old_background = [copy(x) for x in self.background]
        self.old_foreground = [copy(x) for x in self.foreground]

        # sprite order
        sorted_sprites: list[Sprite] = []
        for key in self.sprites: sorted_sprites.append(copy(self.sprites[key]))
        sorted_sprites.sort(key=self.get_sort_value)

        # draw everything
        for sprite in self.draw_background: sprite.draw(self.screen)
        for sprite in self.draw_foreground: sprite.draw(self.screen)
        for sprite in sorted_sprites: sprite.draw(self.screen)

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