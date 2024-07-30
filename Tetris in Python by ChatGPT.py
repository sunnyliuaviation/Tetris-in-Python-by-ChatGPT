import pygame
import random

# 初始化Pygame
pygame.init()

# 定義顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# 定義方塊的顏色對應表
SHAPE_COLORS = {
    1: CYAN,
    2: BLUE,
    3: ORANGE,
    4: YELLOW,
    5: GREEN,
    6: PURPLE,
    7: RED
}

# 定義方塊結構
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# 遊戲視窗尺寸和方塊大小
block_size = 30
play_width = 10
play_height = 20
display_width = play_width * block_size
display_height = play_height * block_size

# 初始化遊戲視窗
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('俄羅斯方塊')

# 設定字體
font = pygame.font.SysFont(None, 40)

# 定義方塊類別
class Piece:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0

    @property
    def rotated_shape(self):
        return self.rotate(self.shape, self.rotation)

    def rotate(self, shape, rotation):
        rotated_shape = shape
        for _ in range(rotation):
            rotated_shape = [list(row) for row in zip(*rotated_shape[::-1])]
        return rotated_shape

# 創建新方塊
def new_piece():
    shape = random.choice(tetris_shapes)
    color = SHAPE_COLORS[tetris_shapes.index(shape) + 1]
    piece = Piece(4, 0, shape, color)
    return piece

# 繪製方塊
def draw_block(x, y, color):
    pygame.draw.rect(game_display, color, [x * block_size, y * block_size, block_size, block_size])

# 檢查方塊位置是否有效
def is_valid_position(piece):
    for y in range(len(piece.rotated_shape)):
        for x in range(len(piece.rotated_shape[y])):
            if piece.rotated_shape[y][x] != 0:
                if (piece.x + x < 0 or piece.x + x >= play_width or
                    piece.y + y >= play_height or
                    grid[piece.y + y][piece.x + x] != 0):
                    return False
    return True

# 將方塊固定在遊戲畫面
def lock_piece(piece):
    for y in range(len(piece.rotated_shape)):
        for x in range(len(piece.rotated_shape[y])):
            if piece.rotated_shape[y][x] != 0:
                grid[piece.y + y][piece.x + x] = piece.rotated_shape[y][x]

# 消除滿行並計分
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

# 繪製遊戲畫面
def draw_game():
    game_display.fill(BLACK)
    for y in range(play_height):
        for x in range(play_width):
            if grid[y][x] != 0:
                draw_block(x, y, SHAPE_COLORS[grid[y][x]])
    draw_piece(current_piece)
    draw_next_piece(next_piece)
    draw_grid()
    draw_score()

# 繪製方塊
def draw_piece(piece):
    for y in range(len(piece.rotated_shape)):
        for x in range(len(piece.rotated_shape[y])):
            if piece.rotated_shape[y][x] != 0:
                draw_block(piece.x + x, piece.y + y, piece.color)

# 繪製下一個方塊
def draw_next_piece(piece):
    for y in range(len(piece.rotated_shape)):
        for x in range(len(piece.rotated_shape[y])):
            if piece.rotated_shape[y][x] != 0:
                draw_block(play_width + 2 + x, 2 + y, piece.color)

# 繪製遊戲網格
def draw_grid():
    for y in range(play_height):
        pygame.draw.line(game_display, BLACK, (0, y * block_size), (display_width, y * block_size))  
    for x in range(play_width):
        pygame.draw.line(game_display, BLACK, (x * block_size, 0), (x * block_size, display_height))  

# 繪製分數
def draw_score():
    score_text = font.render(f'Score: {score}', True, WHITE)
    game_display.blit(score_text, (10, 10))

# 主遊戲迴圈
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
    fall_speed = 0.8
    move_sideways_time = 0
    move_sideways_speed = 0.1

    while not game_exit:
        if game_over:
            game_display.fill(BLACK)
            game_over_text = font.render(' Game Over !', True, WHITE)
            game_display.blit(game_over_text, (display_width // 2 - 100, display_height // 2 - 50))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        keys = pygame.key.get_pressed()
        move_sideways_time += clock.get_rawtime()

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

        if keys[pygame.K_DOWN] and move_sideways_time / 1000 >= move_sideways_speed:
            current_piece.y += 1
            if not is_valid_position(current_piece):
                current_piece.y -= 1
            move_sideways_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % 4
                    if not is_valid_position(current_piece):
                        current_piece.rotation = (current_piece.rotation - 1) % 4

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            current_piece.y += 1
            fall_time = 0
            if not is_valid_position(current_piece):
                current_piece.y -= 1
                lock_piece(current_piece)
                clear_rows()
                current_piece = next_piece
                next_piece = new_piece()
                if not is_valid_position(current_piece):
                    game_over = True

        draw_game()
        pygame.display.update()

    pygame.quit()
    quit()

# 啟動遊戲迴圈
game_loop()
