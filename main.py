import random
'''
hướng dẫn chơi :
    0 là ô có thể đào
    . là ô đã đào và không có bom xung quanh
    có số khác là ô đã đào và có số bom xung quanh
'''
# game_base hiện thị full map : bom là -1, số bom xung quanh là số khác
# game_display hiện thị map đã chơi : 0 là chưa chơi, 1 là đã chơi
game_base=[[0 for _ in range(12)] for _ in range(12)]
game_display=[[0 for _ in range(12)] for _ in range(12)]

# tạo bom ngẫu nhiên
for i in range(1,11):
    for j in range(1,11):
        if(random.randint(0, 3) == 0):
            game_base[i][j] = -1

# đếm số bom xung quanh mỗi ô
for i in range(1,11):
    for j in range(1,11):
        if game_base[i][j] != -1:
            count = 0
            if game_base[i][j] != -1:
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if game_base[x][y] == -1:
                            count += 1
            game_base[i][j] = count

# hiển thị bản đồ ban đầu
print("Welcome to Minesweeper!")
for i in range(12):
    for j in range(12):
        print('0 ',end='')
    print()
# bắt đầu trò chơi
step=0
while True:
    # đào hết thì thắng ( chắc vậy =] )
    step += 1
    if step == 74:
        print("You win!")
        break

    # nhập tọa độ muốn đào
    n,m= map(int, input('Enter coordinates (row col): ').split())
    game_display[n-1][m-1] = 1
    if game_base[n-1][m-1] == -1:
        print("Game Over! point: ", step)
        break

    # hiển thị bản đồ sau mỗi bước
    print("Current map:")
    for i in range(12):
        for j in range(12):
            if(game_display[i][j] == 0):
                print('0 ',end='')
            elif(game_base[i][j] == 0):
                print('. ',end='')
            else:
                print(game_base[i][j], end='')
                print(' ', end = '')
        print()
