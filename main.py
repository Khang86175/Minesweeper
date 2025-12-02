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

'''
hướng dẫn chơi :
    0 là ô có thể đào
    . là ô đã đào và không có bom xung quanh
    có số khác là ô đã đào và có số bom xung quanh
'''

# game_base hiện thị full map : bom là -1, số bom xung quanh là số khác
# game_display hiện thị map đã chơi : 0 là chưa chơi, 1 là đã chơi

n, m, bom = map(int, input('Enter size of map (n row m col numbom): ').split())
# print('Enter size of map (n row m col numbom): ')
# n = int(input())
# m = int(input())
# bom = int(input())

game_base = [[0 for _ in range(m+2)] for _ in range(n+2)]
game_display = [[9 for _ in range(m+2)] for _ in range(n+2)]
num_bombs = bom

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
        if event.type == pygame.MOUSEBUTTONDOWN and game_running == 0 and event.button == 1:
            pos = pygame.mouse.get_pos()
            x = pos[1] // 40 + 1
            y = pos[0] // 40 + 1
            if step == 0:
                bomb(n, m, bom, x, y)
            if game_display[x][y] == 9:
                game_display[x][y] = game_base[x][y]
                if game_display[x][y] == -1:
                    game_running = -1
                elif n*m - step - 1 == num_bombs:
                    game_running = 1
                step += 1

    screen.fill((0, 200, 0))
    if game_running == 1:
        screen.blit(text_win, text_win_rect)
    elif game_running == 0:
        for i in range(1, n+1):
            for j in range(1, m+1):
                if(game_display[i][j] == 9):
                    pygame.draw.rect(screen, (30, 190, 30), ((j-1)*40, (i-1)*40, 40, 40), 0)
                elif(game_display[i][j] == 0):
                    pygame.draw.rect(screen, (80, 80, 80), ((j-1)*40, (i-1)*40, 40, 40), 0)
                else:
                    pygame.draw.rect(screen, (80, 80, 80), ((j-1)*40, (i-1)*40, 40, 40), 0)
                    text_rect = texts[game_display[i][j]].get_rect(center=((j-1)*40 + 20, (i-1)*40 + 20))
                    screen.blit(texts[game_display[i][j]], text_rect)
        for i in range(0, n+1):
            pygame.draw.line(screen, (0, 0, 0), (i*40, 0), (i*40, HEIGHT), 1)
        for j in range(0, m+1):
            pygame.draw.line(screen, (0, 0, 0), (0, j*40), (WIDTH, j*40), 1)
    else:
        screen.blit(text_lose, text_lose_rect)
    pygame.display.flip()
    clock.tick(30)
