import sys
import subprocess

# Danh sách thư viện cần thiết
required = ["pygame"]

# Tự động cài nếu chưa có
for pkg in required:
    try:
        __import__(pkg)
    except ImportError:
        print(f"Đang cài thư viện {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# Sau khi chắc chắn có pygame mới import
import random
import pygame


n, m, bom = map(int, input('Enter size of map (n row m col numbom): ').split())
# print('Enter size of map (n row m col numbom): ')
# n = int(input())
# m = int(input())
# bom = int(input())

game_base = [[0 for _ in range(m+2)] for _ in range(n+2)]
game_display = [[9 for _ in range(m+2)] for _ in range(n+2)]
num_bombs = bom

# game_base biểu thị full map : bom là -1, các số còn lại là số bom xung quanh
# game_display hiện thị map đã chơi : 9 là chưa mở, -1 là cờ, các số còn lại là số bom xung quanh

HEIGHT = n*40
WIDTH = m*40
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

text_win = pygame.font.Font(None, 72).render("You win!", True, (255, 255, 255))
text_win_rect = text_win.get_rect(center=(WIDTH // 2, HEIGHT // 2))
text_lose = pygame.font.Font(None, 72).render("You lose!", True, (255, 255, 255))
text_lose_rect = text_lose.get_rect(center=(WIDTH // 2, HEIGHT // 2))
texts = [font.render(str(i), True, (255, 255, 255)) for i in range(0, 10)]

flag=pygame.image.load("assets/flag.png").convert_alpha()

def generatebom(n, m, bom, xbase, ybase):
    while bom:
        id = random.randint(1, m*n)
        x = (id-1)//m + 1
        y = (id-1)%m + 1
        if game_base[x][y] != -1 and not(abs(x-xbase) <= 1 and abs(y-ybase) <= 1):
            game_base[x][y] = -1
            bom -= 1
    # đếm số bom xung quanh mỗi ô
    for i in range(1, n+1):
        for j in range(1, m+1):
            if game_base[i][j] != -1:
                count = 0
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if game_base[x][y] == -1:
                            count += 1
                game_base[i][j] = count

game_running = 0
#game_running = 0 : đang chơi
#game_running = 1 : win
#game_running = -1 : lose

# bắt đầu trò chơi
step = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_running == 0:
            pos = pygame.mouse.get_pos()
            x = pos[1] // 40 + 1
            y = pos[0] // 40 + 1
            if event.button == 1:  # left click
                if step == 0:
                    generatebom(n, m, bom, x, y)
                if game_base[x][y] == -1:
                    game_running = -1
                else:
                    # mở ô
                    def open_cell(i, j):
                        global step
                        if game_display[i][j] != 9:
                            return
                        step += 1
                        game_display[i][j] = game_base[i][j]
                        if game_base[i][j] == 0:
                            for xi in range(i-1, i+2):
                                for yj in range(j-1, j+2):
                                    if 1 <= xi <= n and 1 <= yj <= m:
                                        open_cell(xi, yj)
                    open_cell(x, y)
            elif event.button == 3:  # right click
                if game_display[x][y] == 9:
                    game_display[x][y] = -1
                elif game_display[x][y] == -1:
                    game_display[x][y] = 9
            if n*m - step - 1 == num_bombs:
                game_running = 1

    screen.fill((0, 200, 0))
    if game_running == 1:
        screen.blit(text_win, text_win_rect)
    elif game_running == 0:
        for i in range(1, n+1):
            for j in range(1, m+1):
                if(game_display[i][j] == 9 or game_display[i][j] == -1):
                    pygame.draw.rect(screen, (30, 190, 30), ((j-1)*40, (i-1)*40, 40, 40), 0)
                    if game_display[i][j] == -1:
                        flag_rect = flag.get_rect(center=((j-1)*40 + 20, (i-1)*40 + 20))
                        screen.blit(flag,flag_rect)
                else:
                    pygame.draw.rect(screen, (80, 80, 80), ((j-1)*40, (i-1)*40, 40, 40), 0)
                    if(game_display[i][j] > 0):
                        text_rect = texts[game_display[i][j]].get_rect(center=((j-1)*40 + 20, (i-1)*40 + 20))
                        screen.blit(texts[game_display[i][j]], text_rect)
        for i in range(0, n+1):
            pygame.draw.line(screen, (0, 0, 0), (i*40, 0), (i*40, HEIGHT), 1)
        for j in range(0, m+1):
            pygame.draw.line(screen, (0, 0, 0), (0, j*40), (WIDTH, j*40), 1)
    else:
        screen.blit(text_lose, text_lose_rect)
    #text_debug = font.render(f'Steps: {step}', True, (255, 255, 255))
    #screen.blit(text_debug, (10, 10))
    pygame.display.flip()
    clock.tick(30)
