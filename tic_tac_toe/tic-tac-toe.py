from random import getrandbits, randint
from terminaltables import SingleTable

FIELD_SIZE = 3
INPUT_COORD_MESSAGE = "Введите номер строки и колонки своего хода через пробел: "


def get_game_field():
    return [["-"] * FIELD_SIZE for _ in range(FIELD_SIZE)]


def print_field():
    """
    Вывод игрового поля
    """
    view_fild = [[" "] + [n for n in range(1, FIELD_SIZE + 1)]]
    for i, row in enumerate(game_field, start=1):
        view_fild.append([i] + row)
    print(SingleTable(view_fild).table)


def get_player_coord():
    """
    Получение координтат хода игрока и проверка их на валидность,
    с преобразованием к нужным значениям.
    """
    c_text = input(INPUT_COORD_MESSAGE).split()
    if len(c_text) == 2:
        try:
            c_int = map(int, c_text)
            c_list = list(filter(lambda x: x > 0 and x <= FIELD_SIZE, c_int))
            if len(c_list) == 2:
                return c_list[0] - 1, c_list[1] - 1
            else:
                print(f"Номер должен быть в диапазоне от 1 до {FIELD_SIZE}")
                return get_player_coord()
        except ValueError:
            print("Номер строки и колонки должены быть цифрами")
            return get_player_coord()
    else:
        print("Должно быть укзано 2 цифры через пробел")
        return get_player_coord()


def make_move(x, y, mark):
    global player_move
    if (x, y) in moves:
        print("Ход уже был сделан ранее")
        return
    game_field[x][y] = mark
    player_move = not player_move
    moves.append((x, y))


def game_finish():
    """
    Проверка на завершение игры и вывод результата.
    """
    if len(moves) == FIELD_SIZE**2:
        print("Ниьчя")
        return True
    else:
        win_mark = ""
        # проверяю строки
        for row in game_field:
            if len(set(row)) == 1 and row[0] != "-":
                win_mark = row[0]
                break
        # проверяю колонки
        for col in range(FIELD_SIZE):
            if len({row[col] for row in game_field}) == 1 and game_field[col][0] != "-":
                win_mark = game_field[col][0]
                break
        # проверка главной диагонали
        if (
            len({game_field[i][i] for i in range(FIELD_SIZE)}) == 1
            and game_field[0][0] != "-"
        ):
            win_mark = game_field[0][0]
        # проверка побочной диагонали
        if (
            len({game_field[i][FIELD_SIZE - i - 1] for i in range(FIELD_SIZE)}) == 1
            and game_field[0][FIELD_SIZE - 1] != "-"
        ):
            win_mark = game_field[0][FIELD_SIZE - 1]

        if win_mark == "":
            return False
        if win_mark == player_mark:
            print("Игрок выиграл")
        else:
            print("Компьютер выиграл")

        return True


game_field = get_game_field()
moves = []
player_move = bool(getrandbits(1))
player_mark = "X"
enemy_mark = "O"
x = y = 0


print("Добро пожаловать в игру Крестики-Нолики!")
if player_move:
    print("Вы ходите первым")
else:
    print("Компьютер ходит первым")
    player_mark, enemy_mark = enemy_mark, player_mark

while True:
    if game_finish():
        break
    if player_move:
        print_field()
        x, y = get_player_coord()
        make_move(x, y, player_mark)
    else:
        x, y = randint(0, FIELD_SIZE - 1), randint(0, FIELD_SIZE - 1)
        if game_field[x][y] == "-":
            make_move(x, y, enemy_mark)
