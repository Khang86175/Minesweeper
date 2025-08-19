import random
import pygame
import sys
'''
hướng dẫn chơi :
    0 là ô có thể đào
    . là ô đã đào và không có bom xung quanh
    có số khác là ô đã đào và có số bom xung quanh
'''
# game_base hiện thị full map : bom là -1, số bom xung quanh là số khác
# game_display hiện thị map đã chơi : 0 là chưa chơi, 1 là đã chơi
n,m,bom=map(int, input('Enter size of map (n row m col numbom): ').split())
game_base=[[0 for _ in range(m+2)] for _ in range(n+2)]
game_display=[[9 for _ in range(m+2)] for _ in range(n+2)]
num_bombs = bom

HEIGHT = n*40
WIDTH = m*40
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
texts = [font.render(str(i), True, (255, 255, 255)) for i in range(0, 10)]

def bomb(n,m,bom,xbase,ybase):
    while bom:
        id = random.randint(1,m*n)
        x=(id-1)//m +1
        y=(id-1)%m+1
        if game_base[x][y] != -1 and abs(x-xbase) > 1 and abs(y-ybase) > 1:
            game_base[x][y] = -1
            bom -= 1
    # đếm số bom xung quanh mỗi ô
    for i in range(1,n+1):
        for j in range(1,m+1):
            if game_base[i][j] != -1:
                count = 0
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if game_base[x][y] == -1:
                            count += 1
                game_base[i][j] = count

# bắt đầu trò chơi
step=0
while True:

    # hiển thị bản đồ sau mỗi bước
    print("Current map (bombs ", num_bombs, "):")
    for i in range(1,n+1):
        for j in range(1,m+1):
            if(game_display[i][j] == 9):
                print('0 ',end='')
            elif(game_display[i][j] == 0):
                print('. ',end='')
            else:
                print(game_display[i][j], end='')
                print(' ', end = '')
        print()

    # đào hết thì thắng ( chắc vậy =] )
    if step == (n)*(m) - num_bombs:
        print("You win!")
        break

    # nhập tọa độ muốn đào
    x,y= map(int, input('Enter coordinates (row col): ').split())
    
    if step == 0:
        bomb(n,m,bom,x,y)
    
    game_display[x][y] = game_base[x][y]
    if game_display[x][y] == -1:
        print("Game Over! point: ", step)
        break
    
    step+=1
    
