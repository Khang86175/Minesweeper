import sys
import subprocess
import random

# --- Cài đặt thư viện ---
try:
    import pygame
except ImportError:
    print("Đang cài thư viện pygame...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

# --- Nhập dữ liệu an toàn ---
# numbom = 10% row*col : dễ
# numbom = 10% row*col : trung bình 
# numbom = 10% row*col : khó
while True:
    inp = input('Enter size of map (row col numbom,numbum should be <=row*col*0.4): ').split()
    if len(inp) != 3:
        print("Invalid input. Please try again.")
        continue
    n, m, bom = map(int, inp)
    if n > 0 and m > 0 and 0 < bom <= n*m*0.4:
        break
    print("Invalid input. Please try again.")
# Setup Game
CELL_SIZE = 40
WIDTH = n * CELL_SIZE
HEIGHT = m * CELL_SIZE
game_base = [[0 for _ in range(m+2)] for _ in range(n+2)]
game_display = [[9 for _ in range(m+2)] for _ in range(n+2)]
# game_base biểu thị full map : bom là -1, các số còn lại là số bom xung quanh
# game_display hiện thị map đã chơi : 9 là chưa mở, -1 là cờ, các số còn lại là số bom xung quanh

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Tạo text
text_win = pygame.font.Font(None, 72).render("You win!", True, (255, 255, 255))
text_win_rect = text_win.get_rect(center=(WIDTH // 2, HEIGHT // 2))
text_lose = pygame.font.Font(None, 72).render("You lose!", True, (255, 255, 255))
text_lose_rect = text_lose.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Tạo màu số
COLORS = [(0,0,0), (0,0,255), (0,128,0), (255,0,0), (0,0,128), (128,0,0), (0,128,128), (0,0,0), (128,128,128)]
texts = [font.render(str(i), True, COLORS[i]) for i in range(9)] # 0 sẽ không dùng

# Load ảnh
flag=pygame.image.load("assets/flag.png").convert_alpha()

def generatebom(n, m, bomb_count, xbase, ybase):
    count = bomb_count
    while count > 0:
        rx = random.randint(1, n)
        ry = random.randint(1, m)
        # Không đặt bom trùng, không đặt vào ô click đầu tiên và 8 ô xung quanh
        if game_base[rx][ry] != -1 and not (abs(rx-xbase) <= 1 and abs(ry-ybase) <= 1):
            game_base[rx][ry] = -1
            count -= 1
            
    # Tính số bom xung quanh
    for i in range(1, n+1):
        for j in range(1, m+1):
            if game_base[i][j] != -1:
                cnt = 0
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if game_base[x][y] == -1:
                            cnt += 1
                game_base[i][j] = cnt

# Mở các ô trống xung quanh ô đầu tiên được click
def open_empty_cells(start_x, start_y):
    stack = [(start_x, start_y)]
    opened_count = 0
    
    while stack:
        cx, cy = stack.pop()
        
        if game_display[cx][cy] != 9: # Nếu đã mở hoặc cắm cờ thì bỏ qua
            continue
            
        game_display[cx][cy] = game_base[cx][cy]
        opened_count += 1
        
        # Nếu là ô trống (số 0), thêm các ô xung quanh vào stack
        if game_base[cx][cy] == 0:
            for xi in range(cx-1, cx+2):
                for yj in range(cy-1, cy+2):
                    if 1 <= xi <= n and 1 <= yj <= m:
                        if game_display[xi][yj] == 9: # Chỉ thêm ô chưa mở
                            stack.append((xi, yj))
    return opened_count

game_running = 0
cell_opened = 0
first_click = True
#game_running = 0 : đang chơi
#game_running = 1 : win
#game_running = -1 : lose

# bắt đầu trò chơi
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
            if 1 <= x <= n and 1 <= y <= m:
                if event.button == 1 and game_display[x][y] == 9:  # left click
                    if first_click:
                        generatebom(n, m, bom, x, y)
                        first_click = False
                    if game_base[x][y] == -1:
                        game_running = -1
                        game_display[x][y] = -1
                    else:
                        cell_opened += open_empty_cells(x, y)
                elif event.button == 3:  # right click
                    if game_display[x][y] == 9:
                        game_display[x][y] = -1
                    elif game_display[x][y] == -1:
                        game_display[x][y] = 9
                if n*m - cell_opened == bom:
                    game_running = 1

    screen.fill((192, 192, 192))
    if game_running == 1:
        screen.blit(text_win, text_win_rect)
    if game_running != 0:
        if game_running == 1:
            screen.blit(text_win, text_win_rect)
        else:
            screen.blit(text_lose, text_lose_rect)
    else :
        for i in range(1, n+1):
            for j in range(1, m+1):
                rect = ((j-1)*CELL_SIZE, (i-1)*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                rect_2 = ((j-1)*CELL_SIZE+5, (i-1)*CELL_SIZE+5, CELL_SIZE-5, CELL_SIZE-5)
                rect_3 = ((j-1)*CELL_SIZE+5, (i-1)*CELL_SIZE+5, CELL_SIZE-10, CELL_SIZE-10)
                val = game_display[i][j]
                
                if val == 9: # Chưa mở
                    pygame.draw.rect(screen, (230, 230, 230), rect) # góc sáng
                    pygame.draw.rect(screen, (140, 140, 140), rect_2) # góc tối
                    pygame.draw.rect(screen, (160, 160, 160), rect_3) # mặt chính
                elif val == -1: # Cờ
                    pygame.draw.rect(screen, (160, 160, 160), rect)
                    if flag:
                        r_center = flag.get_rect(center=((j-1)*CELL_SIZE + CELL_SIZE//2, (i-1)*CELL_SIZE + CELL_SIZE//2))
                        screen.blit(flag, r_center)
                    else:
                        pygame.draw.rect(screen, (255, 0, 0), ((j-1)*CELL_SIZE+10, (i-1)*CELL_SIZE+10, 20, 20))
                else: # Đã mở
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                    pygame.draw.rect(screen, (100, 100, 100), rect, 1) # Viền chìm
                    if val > 0:
                        txt = texts[val]
                        txt_r = txt.get_rect(center=((j-1)*CELL_SIZE + CELL_SIZE//2, (i-1)*CELL_SIZE + CELL_SIZE//2))
                        screen.blit(txt, txt_r)
        for i in range(0, m+1):
            pygame.draw.line(screen, (100, 100, 100), (i*CELL_SIZE, 0), (i*CELL_SIZE, HEIGHT), 1)
        for j in range(0, n+1):
            pygame.draw.line(screen, (100, 100, 100), (0, j*CELL_SIZE), (WIDTH, j*CELL_SIZE), 1)

    #text_debug = font.render(f'Steps: {step}', True, (255, 255, 255))
    #screen.blit(text_debug, (10, 10))
    pygame.display.flip()
    clock.tick(30)
