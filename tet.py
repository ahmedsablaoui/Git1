import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
COLOR_LIST = [CYAN, MAGENTA, YELLOW, ORANGE, RED, GREEN, BLUE]

# Points awarded for clearing lines
LINE_CLEAR_POINTS = 100

# Shapes of Tetriminos
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Helper functions
def check_collision(board, shape, offset):
    """Check if the shape collides with the board or the edges."""
    x_offset, y_offset = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board_x = x + x_offset
                board_y = y + y_offset
                if (board_x < 0 or board_x >= BOARD_WIDTH or
                    board_y >= BOARD_HEIGHT or
                    board[board_y][board_x]):
                    return True
    return False

def clear_lines(board):
    """Clear completed lines from the board and return the number of lines cleared."""
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    new_board = [[0] * BOARD_WIDTH for _ in range(lines_cleared)] + new_board
    return new_board, lines_cleared

def rotate(shape):
    """Rotate the shape."""
    return [list(row) for row in zip(*shape[::-1])]

def draw_board(board):
    """Draw the game board."""
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell,
                                 pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.flip()

def draw_shape(shape, offset):
    """Draw the current shape."""
    x_offset, y_offset = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell,
                                 pygame.Rect((x + x_offset) * BLOCK_SIZE, (y + y_offset) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_score(score):
    """Draw the score on the screen."""
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over():
    """Draw the game over message."""
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 36))

def is_game_over(board, shape):
    """Check if the game is over."""
    x_offset = BOARD_WIDTH // 2 - len(shape[0]) // 2
    y_offset = 0
    return check_collision(board, shape, (x_offset, y_offset))

def main():
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0  # Initialize the score
    shape = random.choice(SHAPES)
    shape_color = random.choice(COLOR_LIST)
    shape = [[shape_color if cell else 0 for cell in row] for row in shape]
    shape_offset = [BOARD_WIDTH // 2 - len(shape[0]) // 2, 0]
    running = True
    game_over = False

    while running:
        if not game_over:
            screen.fill(BLACK)
            fall_time += clock.get_rawtime()
            clock.tick()
            if fall_time > 500:
                shape_offset[1] += 1
                if check_collision(board, shape, shape_offset):
                    shape_offset[1] -= 1
                    for y, row in enumerate(shape):
                        for x, cell in enumerate(row):
                            if cell:
                                board[y + shape_offset[1]][x + shape_offset[0]] = cell
                    board, lines_cleared = clear_lines(board)
                    score += lines_cleared * LINE_CLEAR_POINTS  # Update the score
                    shape = random.choice(SHAPES)
                    shape_color = random.choice(COLOR_LIST)
                    shape = [[shape_color if cell else 0 for cell in row] for row in shape]
                    shape_offset = [BOARD_WIDTH // 2 - len(shape[0]) // 2, 0]
                    if is_game_over(board, shape):
                        game_over = True
                fall_time = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        shape_offset[0] -= 1
                        if check_collision(board, shape, shape_offset):
                            shape_offset[0] += 1
                    if event.key == pygame.K_RIGHT:
                        shape_offset[0] += 1
                        if check_collision(board, shape, shape_offset):
                            shape_offset[0] -= 1
                    if event.key == pygame.K_DOWN:
                        shape_offset[1] += 1
                        if check_collision(board, shape, shape_offset):
                            shape_offset[1] -= 1
                    if event.key == pygame.K_UP:
                        rotated_shape = rotate(shape)
                        if not check_collision(board, rotated_shape, shape_offset):
                            shape = rotated_shape
            
            draw_board(board)
            draw_shape(shape, shape_offset)
            draw_score(score)  # Draw the score
            pygame.display.flip()
        else:
            draw_game_over()
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting

    pygame.quit()

if __name__ == "__main__":
    main()
