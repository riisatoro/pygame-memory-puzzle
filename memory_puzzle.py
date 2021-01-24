import pygame, sys
from dataclasses import dataclass
import memory_puzzle_settings as settings

from random import shuffle


@dataclass
class Tile:
    shape: str
    color: tuple
    revealed: bool = False


class Core:
    @staticmethod
    def create_new_board() -> list:
        tiles = [
            Tile(shape, color)
            for shape in settings.ALL_SHAPES
            for color in settings.ALL_COLORS
        ]
        shuffle(tiles)
        tiles_required = (settings.BOARD_WIDTH * settings.BOARD_HEIGHT) // 2
        tiles = tiles[:tiles_required] * 2
        shuffle(tiles)

        board = []
        for y in range(settings.BOARD_HEIGHT):
            row = []
            for x in range(settings.BOARD_WIDTH):
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
        for x_axes in range(settings.BOARD_WIDTH):
            for y_axes in range(settings.BOARD_HEIGHT):
                left, top = Core.get_title_coords_on_display(x_axes, y_axes)
                print(left, top)
                if board[y_axes][x_axes].revealed:
                    shape, color = (
                        board[y_axes][x_axes].shape,
                        board[y_axes][x_axes].color,
                    )
                    Drawable.draw_icon(surf, shape, color, (x_axes, y_axes))
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
        left, top = Core.get_title_coords_on_display(coords[0], coords[1])

        if shape == settings.DONUT:
            pygame.draw.circle(surf, color, (left + half, top + half), half - 5)
            pygame.draw.circle(
                surf, settings.BGCOLOR, (left + half, top + half), quarter - 5
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
                    (left + settings.BOXSIZE - 1, top + half),
                    (left + half, top + settings.BOXSIZE - 1),
                    (left, top + half),
                ),
            )

        elif settings.LINES:
            for i in range(0, settings.BOX_SIZEIZE, 4):
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
    def draw_tile_covers(surf, tiles):
        for tile in tiles:
            left, top = Core.get_title_coords_on_display()
            pygame.draw.rect(
                surf,
                settings.BG_COLOR,
                (left, top, settings.BOX_SIZE, settings.BOX_SIZE),
            )
            shape, color = tile.shape, tile.color
            Drawable.draw_icon(surf, shape, color, (left, top))


class Animation:
    @staticmethod
    def start_game(surf, board):
        tiles = [
            (x, y)
            for x in range(settings.BOARD_WIDTH)
            for y in range(settings.BOARD_HEIGHT)
        ]
        shuffle(tiles)
        grouped_tiles = Core.split_into_group(8, tiles)
        Drawable.draw_board(surf, board)
        for group in grouped_tiles:
            Animation.reveal_tiles(surf, board, group)
            Animation.hide_tiles(surf, board, group)

    @staticmethod
    def reveal_tiles(surf, board, tiles):
        for coverage in range(
            settings.BOX_SIZE, (-settings.REVEAL_SPEED) - 1, -settings.REVEAL_SPEED
        ):
            Drawable.draw_tile_covers(surf, tiles, coverage)

    @staticmethod
    def hide_tiles(board, group):
        pass


class Main:
    @staticmethod
    def run():
        pygame.init()

        clock = pygame.time.Clock()
        window = pygame.display.set_mode(settings.RESOLUTION)
        window.fill(settings.BG_COLOR)

        mouse_x, mouse_y = 0, 0
        pygame.display.set_caption(settings.TITLE)

        board = Core.create_new_board()
        Drawable.draw_board(window, board)

        first_selection = None

        # Animation.start_game(DISPLAY_SURF, board)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(settings.FPS)

        import ipdb

        ipdb.set_trace()


if __name__ == "__main__":
    Main.run()
