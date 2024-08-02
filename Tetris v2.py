import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GRAY = (169, 169, 169)  # Gray for preview

# Shape colors
SHAPE_COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

# Tetris shapes (use indices to reference colors)
tetris_shapes = [
    [[1, 1, 1, 1]],

    [[2, 2, 0],
     [0, 2, 2]],

    [[0, 3, 3],
     [3, 3, 0]],

    [[4, 4, 4],
     [0, 0, 4]],

    [[5, 5, 5],
     [5, 0, 0]],

    [[0, 6, 0],
     [6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# Game dimensions
block_size = 30
play_width = 10
play_height = 20
display_width = play_width * block_size
display_height = play_height * block_size

# Initialize game window
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tetris')

# Font
font = pygame.font.SysFont(None, 40)

# Piece class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[tetris_shapes.index(shape)]
        self.rotation = 0

    @property
    def rotated_shape(self):
        return self.rotate(self.shape, self.rotation)

    def rotate(self, shape, rotation):
        rotated_shape = shape
        for _ in range(rotation):
            rotated_shape = [list(row) for row in zip(*rotated_shape[::-1])]
        return rotated_shape

# Create new piece
def new_piece():
    shape = random.choice(tetris_shapes)
    piece = Piece(4, 0, shape)
    return piece

# Draw block
def draw_block(x, y, color):
    pygame.draw.rect(game_display, color, [x * block_size, y * block_size, block_size, block_size])

# Check if the position is valid
def is_valid_position(piece):
    for y in range(len(piece.rotated_shape)):
        for x in range(len(piece.rotated_shape[y])):
            if piece.rotated_shape[y][x] != 0:
                if (piece.x + x < 0 or piece.x + x >= play_width or
                    piece.y + y >= play_height or
                    (piece.y + y >= 0 and (grid[piece.y + y][piece.x + x] != 0 and grid[piece.y + y][piece.x + x] != -1))):
                    return False
    return True

# Lock piece in the grid
def lock_piece(piece):
    for y in range(len(piece.rotated_shape)):
        for x in range(len(piece.rotated_shape[y])):
            if piece.rotated_shape[y][x] != 0:
                if 0 <= piece.y + y < play_height and 0 <= piece.x + x < play_width:
                    grid[piece.y + y][piece.x + x] = piece.rotated_shape[y][x]

# Clear full rows
def clear_rows():
    global score
    full_rows = 0
    for y in range(play_height):
        if all(grid[y]):
            full_rows += 1
            for row in range(y, 0, -1):
                grid[row] = grid[row - 1].copy()
            grid[0] = [0] * play_width
    score += full_rows * 10

# Draw the game state
def draw_game():
    game_display.fill(BLACK)
    for y in range(play_height):
        for x in range(play_width):
            if grid[y][x] != 0:
                draw_block(x, y, SHAPE_COLORS[grid[y][x] - 1])
    draw_piece(current_piece)
    draw_preview(current_piece)
    draw_grid()
    draw_score()

# Draw piece
def draw_piece(piece):
    for y in range(len(piece.rotated_shape)):
        for x in range(len(piece.rotated_shape[y])):
            if piece.rotated_shape[y][x] != 0:
                draw_block(piece.x + x, piece.y + y, piece.color)

# Draw preview of the piece
def draw_preview(piece):
    # Create a copy of the piece and simulate it falling to the bottom
    temp_piece = Piece(piece.x, piece.y, piece.shape)
    temp_piece.rotation = piece.rotation  # Start with the same rotation
    while is_valid_position(temp_piece):
        temp_piece.y += 1
    temp_piece.y -= 1

    # Draw the preview piece in gray
    for y in range(len(temp_piece.rotated_shape)):
        for x in range(len(temp_piece.rotated_shape[y])):
            if temp_piece.rotated_shape[y][x] != 0:
                draw_block(temp_piece.x + x, temp_piece.y + y, GRAY)

# Draw grid
def draw_grid():
    for y in range(play_height):
        pygame.draw.line(game_display, WHITE, (0, y * block_size), (display_width, y * block_size))
    for x in range(play_width):
        pygame.draw.line(game_display, WHITE, (x * block_size, 0), (x * block_size, display_height))

# Draw score
def draw_score():
    score_text = font.render(f'Score: {score}', True, WHITE)
    game_display.blit(score_text, (10, 10))

# Hard drop
def hard_drop(piece):
    while is_valid_position(piece):
        piece.y += 1
    piece.y -= 1
    lock_piece(piece)
    clear_rows()

# Handle downward movement
def move_down(piece):
    piece.y += 1
    if not is_valid_position(piece):
        piece.y -= 1
        lock_piece(piece)
        clear_rows()
        return False
    return True

# Rotate piece
def rotate_piece(piece):
    original_rotation = piece.rotation
    piece.rotation = (piece.rotation + 1) % 4
    rotated_shape = piece.rotate(piece.shape, piece.rotation)
    if not is_valid_position(piece):
        piece.rotation = original_rotation
        return

    # Try to adjust position
    for offset in range(1, 4):  # Try different offsets
        piece.x -= offset
        if is_valid_position(piece):
            return
        piece.x += 2 * offset
        if is_valid_position(piece):
            return
        piece.x -= offset

    # If no valid position is found, revert to original rotation
    piece.rotation = original_rotation

# Main game loop
def game_loop():
    global grid, current_piece, next_piece, score
    grid = [[0] * play_width for _ in range(play_height)]
    current_piece = new_piece()
    next_piece = new_piece()
    score = 0
    clock = pygame.time.Clock()
    game_exit = False
    game_over = False
    fall_time = 0
    fall_speed = 0.5  # Adjust fall speed as necessary
    move_sideways_time = 0
    move_sideways_speed = 0.1
    hard_drop_triggered = False
    rotation_just_pressed = False

    while not game_exit:
        if game_over:
            game_display.fill(BLACK)
            game_over_text = font.render('Game Over!', True, WHITE)
            score_text = font.render(f'Score: {score}', True, WHITE)
            game_over_x = (display_width - game_over_text.get_width()) // 2
            score_x = (display_width - score_text.get_width()) // 2
            game_display.blit(game_over_text, (game_over_x, display_height // 2 - 50))
            game_display.blit(score_text, (score_x, display_height // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        keys = pygame.key.get_pressed()
        move_sideways_time += clock.get_rawtime()

        # Handle sideways movement
        if keys[pygame.K_LEFT] and move_sideways_time / 1000 >= move_sideways_speed:
            current_piece.x -= 1
            if not is_valid_position(current_piece):
                current_piece.x += 1
            move_sideways_time = 0

        if keys[pygame.K_RIGHT] and move_sideways_time / 1000 >= move_sideways_speed:
            current_piece.x += 1
            if not is_valid_position(current_piece):
                current_piece.x -= 1
            move_sideways_time = 0

        # Handle downward movement
        if keys[pygame.K_DOWN] and move_sideways_time / 1000 >= move_sideways_speed:
            if not move_down(current_piece):
                current_piece = next_piece
                next_piece = new_piece()
                if not is_valid_position(current_piece):
                    game_over = True
            move_sideways_time = 0

        # Handle rotation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not rotation_just_pressed:
                        rotate_piece(current_piece)
                        rotation_just_pressed = True
                elif event.key == pygame.K_SPACE:
                    if not hard_drop_triggered:
                        hard_drop(current_piece)
                        current_piece = next_piece
                        next_piece = new_piece()
                        if not is_valid_position(current_piece):
                            game_over = True
                        hard_drop_triggered = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rotation_just_pressed = False
                elif event.key == pygame.K_SPACE:
                    hard_drop_triggered = False

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            if not move_down(current_piece):
                current_piece = next_piece
                next_piece = new_piece()
                if not is_valid_position(current_piece):
                    game_over = True
                hard_drop_triggered = False  # Allow hard drop for the new piece
            fall_time = 0

        draw_game()
        pygame.display.update()

    pygame.quit()
    quit()

# Start the game
game_loop()
