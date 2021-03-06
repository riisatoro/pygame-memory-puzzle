import pygame, sys
from pygame.locals import *
from dataclasses import dataclass
from collections import namedtuple
import memory_puzzle_settings as settings

from random import shuffle

Indexes = namedtuple("Indexes", ["x", "y"])
Coords = namedtuple("Coords", ["x", "y"])


@dataclass
class Tile:
    shape: str
    color: tuple
    revealed: bool = False

    def __eq__(self, other):
        return self.shape == other.shape and self.color == other.color


class Core:
    @staticmethod
    def create_new_board() -> list:
        tiles = [
            Tile(shape, color)
            for shape in settings.ALL_SHAPES
            for color in settings.ALL_COLORS
        ]
        shuffle(tiles)
        tiles_required = (settings.TILES_ON_WIDTH * settings.TILES_ON_HEIGHT) // 2
        tiles_required += (settings.TILES_ON_WIDTH * settings.TILES_ON_HEIGHT) % 2
        
        tiles = tiles[:tiles_required] * 2
        shuffle(tiles)
        #import ipdb; ipdb.set_trace()
        board = []
        for y in range(settings.TILES_ON_HEIGHT):
            row = []
            for x in range(settings.TILES_ON_WIDTH):
                row.append(tiles.pop())
            board.append(row)
        return board

    @staticmethod
    def split_into_group(size, tiles):
        return [tiles[i : i + size] for i in range(0, len(tiles), size)]

    @staticmethod
    def get_title_coords_on_display(x_axes, y_axes):
        x = x_axes * (settings.BOX_SIZE + settings.GAP_SIZE) + settings.X_MARGIN
        y = y_axes * (settings.BOX_SIZE + settings.GAP_SIZE) + settings.Y_MARGIN
        return x, y


class Drawable:
    @staticmethod
    def draw_board(surf, board):
        for x_axes in range(settings.TILES_ON_WIDTH):
            for y_axes in range(settings.TILES_ON_HEIGHT):
                left, top = Core.get_title_coords_on_display(x_axes, y_axes)
                if board[y_axes][x_axes].revealed:
                    shape, color = (
                        board[y_axes][x_axes].shape,
                        board[y_axes][x_axes].color,
                    )
                    Drawable.draw_icon(surf, shape, color, Coords(x_axes, y_axes))
                else:
                    pygame.draw.rect(
                        surf,
                        settings.BOX_COLOR,
                        (left, top, settings.BOX_SIZE, settings.BOX_SIZE),
                    )

    @staticmethod
    def draw_icon(surf, shape, color, coords):
        quarter = int(settings.BOX_SIZE * 0.25)
        half = int(settings.BOX_SIZE * 0.5)
        left, top = Core.get_title_coords_on_display(coords.x, coords.y)

        if shape == settings.DONUT:
            pygame.draw.circle(surf, color, (left + half, top + half), half - 5)
            pygame.draw.circle(
                surf, settings.BG_COLOR, (left + half, top + half), quarter - 5
            )

        elif shape == settings.SQUARE:
            pygame.draw.rect(
                surf,
                color,
                (
                    left + quarter,
                    top + quarter,
                    settings.BOX_SIZE - half,
                    settings.BOX_SIZE - half,
                ),
            )

        elif shape == settings.DIAMOND:
            pygame.draw.polygon(
                surf,
                color,
                (
                    (left + half, top),
                    (left + settings.BOX_SIZE - 1, top + half),
                    (left + half, top + settings.BOX_SIZE - 1),
                    (left, top + half),
                ),
            )

        elif settings.LINES:
            for i in range(0, settings.BOX_SIZE, 4):
                pygame.draw.line(surf, color, (left, top + i), (left + i, top))
                pygame.draw.line(
                    surf,
                    color,
                    (left + i, top + settings.BOX_SIZE - 1),
                    (left + settings.BOX_SIZE - 1, top + i),
                )
        elif settings.OVAL:
            pygame.draw.ellipse(
                surf, color, (left, top + quarter, settings.BOX_SIZE, half)
            )

    @staticmethod
    def draw_open_tiles(surf, tile, indexes):
        left, top = Core.get_title_coords_on_display(indexes.x, indexes.y)
        pygame.draw.rect(
            surf,
            settings.BOARD_COLOR,
            (left, top, settings.BOX_SIZE, settings.BOX_SIZE),
        )
        shape, color = tile.shape, tile.color
        Drawable.draw_icon(surf, shape, color, indexes)

    @staticmethod
    def draw_closed_tiles(surf, tile, indexes):
        left, top = Core.get_title_coords_on_display(indexes.x, indexes.y)
        pygame.draw.rect(
            surf,
            settings.BOX_COLOR,
            (left, top, settings.BOX_SIZE, settings.BOX_SIZE),
        )

    @staticmethod
    def board_revealed(board):
        for row in board:
            for tile in row:
                if not tile.revealed:
                    return False
        return True

class Animation:
    @staticmethod
    def start_game(surf, board):
        Animation.reveal_tiles(surf, board, tiles=None)
        pygame.display.update()
        pygame.time.wait(10000)
        Animation.hide_tiles(surf, board, tiles=None)

    @staticmethod
    def reveal_tiles(surf, board, tiles=None):
        if tiles is None:
            for y, row in enumerate(board):
                for x, tile in enumerate(row):
                    Drawable.draw_open_tiles(surf, tile, Indexes(x, y))
        else:
            pass

    @staticmethod
    def hide_tiles(surf, board, tiles=None):
        if tiles is None:
            for y, row in enumerate(board):
                for x, tile in enumerate(row):
                    Drawable.draw_closed_tiles(surf, tile, Indexes(x, y))
        else:
            pass


class Main:
    @staticmethod
    def run():
        pygame.init()
        pygame.display.set_caption(settings.TITLE)

        window = pygame.display.set_mode(settings.RESOLUTION)
        window.fill(settings.BOARD_COLOR)

        clock = pygame.time.Clock()


        board = Core.create_new_board()
        Drawable.draw_board(window, board)

        first_tile = None

        Animation.start_game(window, board)

        mouse_x, mouse_y = 0, 0
        mouse_clicked = False
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYUP and event.key == K_ESCAPE
                ):
                    run = False
                elif event.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    mouse_clicked = True
            if Core.board_revealed(board):
                pass

            if mouse_clicked:
                indexes = Indexes(
                    (mouse_x - settings.GAP_SIZE) // (settings.BOX_SIZE + settings.GAP_SIZE),
                    (mouse_y - settings.GAP_SIZE) // (settings.BOX_SIZE + settings.GAP_SIZE),
                )
                if indexes.x not in range(settings.TILES_ON_WIDTH) or indexes.y not in range(settings.TILES_ON_HEIGHT):
                    mouse_clicked = False
                    continue

                if first_tile is None:
                    first_tile = indexes
                    Drawable.draw_open_tiles(
                        window, board[indexes.y][indexes.x], indexes
                    )
                else:
                    if first_tile == indexes:
                        mouse_clicked = False
                        continue

                    Drawable.draw_open_tiles(
                        window, board[indexes.y][indexes.x], indexes
                    )
                    pygame.display.update()
                    pygame.time.wait(2000)
                    if board[indexes.y][indexes.x] == board[first_tile.y][first_tile.x]:
                        board[indexes.y][indexes.x].revealed = True
                        board[first_tile.y][first_tile.x].revealed = True
                    Drawable.draw_board(window, board)
                    first_tile = None

            mouse_clicked = False
            pygame.display.update()
            clock.tick(settings.FPS)


if __name__ == "__main__":
    Main.run()
