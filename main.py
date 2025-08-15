import random
'''
hướng dẫn chơi :
    0 là ô có thể đào
    . là ô đã đào và không có bom xung quanh
    có số khác là ô đã đào và có số bom xung quanh
'''
# game_base hiện thị full map : bom là -1, số bom xung quanh là số khác
# game_display hiện thị map đã chơi : 0 là chưa chơi, 1 là đã chơi
n,m=map(int, input('Enter size of map (n row m col): ').split())
game_base=[[0 for _ in range(m+2)] for _ in range(n+2)]
game_display=[[0 for _ in range(m+2)] for _ in range(n+2)]
bom = input(int())
num_bombs = bom
# tạo bom ngẫu nhiên

while bom:
    id = random.randint(1,m*n)
    if game_base[ (id-1)//m +1 ][ (id-1)%m+1 ] != -1:
        game_base[ (id-1)//m +1][ (id-1)%m+1 ] = -1
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

# hiển thị bản đồ ban đầu
print("Welcome to Minesweeper! ",num_bombs)
for i in range(n):
    for j in range(m):
        print('0 ',end='')
    print()

# bắt đầu trò chơi
step=0
while True:

    # nhập tọa độ muốn đào
    x,y= map(int, input('Enter coordinates (row col): ').split())
    game_display[x][y] = 1
    if game_base[x][y] == -1:
        print("Game Over! point: ", step)
        break

    # hiển thị bản đồ sau mỗi bước
    print("Current map (bombs ", num_bombs, "):")
    for i in range(1,n+1):
        for j in range(1,m+1):
            if(game_display[i][j] == 0):
                print('0 ',end='')
            elif(game_base[i][j] == 0):
                print('. ',end='')
            else:
                print(game_base[i][j], end='')
                print(' ', end = '')
        print()
    
    # đào hết thì thắng ( chắc vậy =] )
    step += 1
    if step == (n)*(m) - num_bombs:
        print("You win!")
        break
