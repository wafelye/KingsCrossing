from game_window import Board
from const import *


class Play:
    def __init__(self):
        self.board_width = 10
        self.board_height = 10
        self.size = board_width * 70, board_height * 70
        self.screen = pygame.display.set_mode(size)

        self.play_window = pygame.Surface((board_width * 50, board_height * 50))  # панель с доской
        self.play_window.fill(PLAY_WINDOW_BG)

        pygame.display.set_caption('Реверси')

        self.board = Board(self.board_width, board_height)
        self.board.set_view(0, 0, 50)

    def go(self):
        pygame.init()







        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(SCREEN_BG, (0, 0))
            screen.blit(play_window, (100, 100))
            board.run()
            board.render()
            pygame.display.flip()
        pygame.quit()
