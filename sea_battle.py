import random
import time

mark_O='O'
mark_ship='■'
mark_X='X'
mark_T='T'
mark_ship_out='*'
class cell:

    def __init__(self,x,y,mark=mark_O):
        self.mark = mark
        self.x=x
        self.y=y

    def set_mark(self, mark):
        self.mark = mark

    def get_mark(self):
        return self.mark

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class ship:

    def __init__(self,ship):
        self.ship_point=[]
        sort_ship = sorted(ship)
        for i in sort_ship:
            self.ship_point.append([i[0], i[1]])
        self.nose_ship = sort_ship[0]
        self.length = len(ship)
        self.health = len(ship)
        if  all(x[0] == ship[0][0] for x in ship):
            direction='col'
        else:
            direction='row'
        self.direction=direction

    @property
    def ship_border(self):
        ship_border = []
        bord=self.ship_point
        if self.direction!='row':
            chek = -1 if bord[0][1] > 0 else 0
            for i in range(chek,len(bord)+1):
                if -1<bord[0][1]+i<6 and bord[0][0] - 1!=-1: ship_border.append([bord[0][0] - 1,bord[0][1] + i])
                if -1<bord[0][1]+i<6 and not [bord[0][0],bord[0][1] + i] in bord: ship_border.append([bord[0][0],bord[0][1] + i])
                if -1<bord[0][1]+i<6 and bord[0][0] + 1!=6:ship_border.append([bord[0][0] + 1,bord[0][1] + i])
        else:
            chek = -1 if bord[0][0] >0 else 0
            for i in range( chek , len(bord) + 1):
                if  bord[0][1]-1!=-1 and -1<(bord[0][0]+i)<6 :ship_border.append([bord[0][0] +i,bord[0][1] -1])
                if  -1<(bord[0][0]+i)<6 and not [bord[0][0] + i, bord[0][1]] in bord : ship_border.append([bord[0][0] +i,bord[0][1]])
                if bord[0][1]+1!=6 and -1<(bord[0][0]+i)<6:ship_border.append([bord[0][0] +i,bord[0][1] +1])
        return ship_border

    def out(self):
        if all(-1 < point[0] < 6 for point in self.ship_point) and all(-1 < point[1] < 6 for point in self.ship_point):
            pass
        else:
            raise Exception
            #print('Точки находяться за пределами поля')
        for i in range(self.length):
            if not self.ship_point[i][0]==self.nose_ship[0]+i:
                raise Exception
                #print('Корабль не наодной линии')

class board:
    hid = True

    def __init__(self, size=6):
        self.ships = []
        self.cells = []
        self.size = size
        for i in range(size):
            row = []
            for j in range(size):
                row.append(cell(i, j))
            self.cells.append(row)

    @property
    def health(self):
        health=0
        for ship in self.ships:
            health+=ship.health
        return health

    def get_size(self):
        return self.size

    def add_ship(self, ship):
        for ship_ in self.ships:
            for j in ship.ship_point:
                if [j[0],j[1]] in ship_.ship_point or [j[0],j[1]] in ship_.ship_border:
                    raise ValueError()
        for ship_ in ship.ship_point:
            self.cells[ship_[0]][ship_[1]].set_mark(mark_ship)
        self.ships.append(ship)

    def shot(self,point):
        if not -1<point[0]<6 or not -1<point[1]<6:
            print('За пределами поля')
            raise Exception('За пределами поля')
        if self.cells[point[0]][point[1]].mark == mark_T or self.cells[point[0]][point[1]].mark == mark_X:
            raise SystemError('Вы сюда стриляли')
        for ship_ in self.ships:
            if point in ship_.ship_point :
                self.cells[point[0]][point[1]].set_mark(mark_X)
                ship_.health-=1
                if ship_.health==0:
                    print('Убил')
                    for j in ship_.ship_border:
                        self.cells[j[0]][j[1]].set_mark(mark_T)
                    raise Warning
                else:
                    print('Попал')
                    raise Warning
        self.cells[point[0]][point[1]].set_mark(mark_T)
        print('Не попал')

    def render(self):
        list_=[]
        for i in range(self.get_size()):
            row = []
            for j in range(self.get_size()):
                row.append(self.cells[i][j].get_mark())
            list_.append(row)
        for i in self.ships:
            for j in i.ship_border:
                list_[j[0]][j[1]]=mark_T
        print(' |1|2|3|4|5|6 ')
        for i in range(self.get_size()):
            row = []
            for j in range(self.get_size()):
                row.append(list_[i][j])
            print(str(i+1) + '|' + "|".join(row))

    def render2(self,zdoard,player):
        print(f' Поле {player.name}    Поле противника')
        print(' |1|2|3|4|5|6   |1|2|3|4|5|6 ')
        st = self.get_size()
        for i in range(st):
            row = []
            str_ = ''
            for j in range(st):
                if self.hid==True and self.cells[i][j].get_mark()==mark_ship:
                    row.append(mark_O)
                else:
                    row.append(self.cells[i][j].get_mark())
            str_=str(i+1) + '|' + "|".join(row)+'  '
            row = []
            for j in range(st):
                if zdoard.hid==True and zdoard.cells[i][j].get_mark()==mark_ship:
                    row.append(mark_O)
                else:
                    row.append(zdoard.cells[i][j].get_mark())
            str_ += str(i+1) + '|' + "|".join(row)
            print(str_)

    def clear(self):
        self.ships = []
        self.cells = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(cell(i, j))
            self.cells.append(row)

class player:
    def __init__(self):
        self.board=board()
        self.zboard=[]
    def ask(self):
        pass
    def move(self,player):
        if self.name!='bot':
            if player.name == 'bot':
                self.board.hid=False
            else:
                self.board.hid = True
            self.zboard.hid=True
            time.sleep(1)
            self.board.render2(self.zboard, self)
        else:
            self.board.hid = True
            self.zboard.hid = False
            self.zboard.render2(self.board, player)
            print('Ходить бот ...')
            time.sleep(2)
        try:
            self.zboard.shot(self.ask())
        except SystemError:
            if self.name != 'bot':
                print('Вы сюда стриляли')
            self.move(player)
        except Warning:
            if self.zboard.health == 0:
                print(f'Победил {self.name}')
                return
            self.move(player)
        except:
            print('Что-то пошло не так попробуйте ввести данные повторно')
            self.move(player)

class AI(player):
    name = 'bot'
    prev_m = []
    list_avail_moves=[]
    def ask(self):
        if self.prev_m!=[]:
            if self.zboard.cells[self.prev_m[0]][self.prev_m[1]].mark == mark_X:
                self.list_avail_moves=self.board_hit_set()
                if not self.list_avail_moves:
                    self.prev_m = random.choice(self.list_moves)
                    return self.prev_m
                self.prev_m = random.choice(self.list_avail_moves)
                return self.prev_m
            if  self.list_avail_moves!=[]:
                self.prev_m=random.choice(self.list_avail_moves)
                return self.prev_m
        self.prev_m=random.choice(self.list_moves)
        return self.prev_m

    @property
    def list_moves(self):
        board=[]
        for i in range(self.zboard.size):
            for j in range(self.zboard.size):
                if self.zboard.cells[i][j].mark == mark_O or self.zboard.cells[i][j].mark == mark_ship:
                    board.append([self.zboard.cells[i][j].x,self.zboard.cells[i][j].y])
        return board
    def board_hit_set(self):    #Логика хода после поподания
        board1=[]
        if -1 < self.prev_m[0] - 1 < 6 :
            if self.zboard.cells[self.prev_m[0] - 1][self.prev_m[1]].mark == mark_X:
                if [self.prev_m[0] + 1, self.prev_m[1]] in self.list_moves:board1.append([self.prev_m[0] + 1, self.prev_m[1]])
                if -1<self.prev_m[0]-2<6 and [self.prev_m[0] - 2, self.prev_m[1]] in self.list_moves : board1.append([self.prev_m[0] - 2, self.prev_m[1]])
                return board1
        if -1 < self.prev_m[0] + 1 < 6 and [self.prev_m[0] + 1, self.prev_m[1]] in self.list_moves:
            if self.zboard.cells[self.prev_m[0] + 1][self.prev_m[1]].mark == mark_X:
                if [self.prev_m[0] - 1, self.prev_m[1]] in self.list_moves:board1.append([self.prev_m[0] - 1, self.prev_m[1]])
                if -1<self.prev_m[0]+2<6 and [self.prev_m[0] + 2, self.prev_m[1]] in self.list_moves:board1.append([self.prev_m[0] + 2, self.prev_m[1]])
                return board1
        if -1 < self.prev_m[1] - 1 < 6 and [self.prev_m[0] - 1, self.prev_m[1]] in self.list_moves:
            if self.zboard.cells[self.prev_m[0]][self.prev_m[1] - 1].mark == mark_X:
                if [self.prev_m[0], self.prev_m[1] + 1] in self.list_moves:board1.append([self.prev_m[0] , self.prev_m[1] + 1])
                if -1 < self.prev_m[0] - 2 < 6 and [self.prev_m[0], self.prev_m[1] - 2] in self.list_moves: board1.append([self.prev_m[0], self.prev_m[1] - 2])
                return board1
        if -1 < self.prev_m[1] + 1 < 6 and [self.prev_m[0] - 1, self.prev_m[1]] in self.list_moves:
            if self.zboard.cells[self.prev_m[0]][self.prev_m[1] + 1].mark == mark_X:
                if [self.prev_m[0], self.prev_m[1] - 1] in self.list_moves:board1.append([self.prev_m[0], self.prev_m[1] - 1])
                if -1 < self.prev_m[0] - 2 < 6 and [self.prev_m[0], self.prev_m[1] + 2] in self.list_moves: board1.append([self.prev_m[0], self.prev_m[1] + 2])
                return board1

        if -1<self.prev_m[0]-1<6 and [self.prev_m[0] - 1, self.prev_m[1]] in self.list_moves:board1.append([self.prev_m[0] - 1, self.prev_m[1]])
        if -1<self.prev_m[0]+1<6 and [self.prev_m[0] + 1, self.prev_m[1]] in self.list_moves:board1.append([self.prev_m[0] + 1, self.prev_m[1]])
        if -1<self.prev_m[1]-1<6 and [self.prev_m[0], self.prev_m[1] - 1] in self.list_moves:board1.append([self.prev_m[0] , self.prev_m[1] - 1])
        if -1<self.prev_m[1]+1<6 and [self.prev_m[0], self.prev_m[1] + 1] in self.list_moves:board1.append([self.prev_m[0], self.prev_m[1] + 1])
        return board1

class User(player):
    name=''

    def ask(self):
        list_=list(map(int, list(input(f'{self.name}. Введите координаты выстрела\n').split(" "))))
        return [list_[0]-1,list_[1]-1]

class game:

    def __init__(self):
        self.player1=None
        self.bord_player1=None
        self.player2=None
        self.bord_player2=None
    def random_board(self, board, counter=3):
        tic = time.perf_counter()
        for i in range(4 - counter):
            while True:
                try:
                    vektor=['row','col']
                    r_vektor=random.choice(vektor)
                    r_point=[random.randint(0, 5),random.randint(0, 5)]
                    points=[]
                    for i1 in range(counter):
                        points.append(r_point.copy())
                        if r_vektor == 'row':
                            r_point[0]=r_point[0]+1
                        else:
                            r_point[1]=r_point[1]+1
                        if r_point[0]>5 or r_point[1]>5:
                            break
                    if len(points)!=counter:
                        continue
                    ship1=ship(points)
                    toc = time.perf_counter()
                    if toc - tic > 0.002:
                        board.clear()
                        return self.random_board(board)
                    if ship1.out()==False:
                        continue
                    if board.add_ship(ship1)==False:
                        continue
                    break
                except:
                    continue
        counter-=1
        if counter==0:
            return
        return self.random_board(board, counter)




    def greet(self):
        pass

    def creat_board(self,player):
        if input(f'{player.name}. \nСоздать рандомную доску - 0\n')=='0':
            self.random_board(player.board)
        else:
            for i in range(3):
                for kol in range(i+1):
                    while True:
                        try:
                            ship_s = list(map(int, list(input(f'Введите координаты {3-i} палубного корабля\n').split(" "))))
                            ship_ = []
                            for j in range(0,(3-i)*2,2):
                                ship_.append([ship_s[j]-1, ship_s[j+1]-1])
                            ship_p=ship(ship_)
                            ship_p.out()
                            player.board.add_ship(ship_p)
                            player.board.render()
                            break
                        except:
                            continue

    def loop(self):
        self.player1.move(self.player2)
        if self.player1.zboard.health == 0:
            return
        self.player2.move(self.player1)
        if self.player2.zboard.health == 0:
            return
        self.loop()

    def start(self):
        self.greet()
        player1 =User()
        player1.name='player1'
        self.player1 = player1
        self.bord_player1=player1.board
        if input('PvP - 0 \nPvE - 1\n')=='1':
            player2 = AI()
        else:
            player2 = User()
            player2.name = 'player2'
        self.player2 = player2
        self.bord_player2 = player2.board
        self.creat_board(player1)
        if player2.name=='bot':
            self.random_board(player2.board)
        else:
            self.creat_board(self.player2)
        self.player1.zboard=self.player2.board
        self.player1.zboard.hid=False
        self.player2.zboard = self.player1.board
        self.player2.zboard.hid=False
        self.loop()
        return

g=game()
g.start()



