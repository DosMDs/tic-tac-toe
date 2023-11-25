from random import getrandbits, randint
from terminaltables import SingleTable


class TicTacToe:
    def __init__(self, field_size: int = 3) -> None:
        self.field_size: int = field_size
        self.empty_char: str = "-"
        self.game_field: list[list[str]] = self.get_game_field()
        self.moves: list[tuple] = []
        self.player_move: bool = bool(getrandbits(1))
        player_mark: str = "X"
        enemy_mark: str = "O"
        print("Добро пожаловать в игру Крестики-Нолики!")
        if self.player_move:
            print("Вы ходите первым")
        else:
            print("Компьютер ходит первым")
            player_mark, enemy_mark = enemy_mark, player_mark
        self.player_mark: str = player_mark
        self.enemy_mark: str = enemy_mark

    def get_game_field(self) -> list[list[str]]:
        """
        Генерация игрового поля
        """
        return [
            [self.empty_char] * self.field_size
            for _ in range(self.field_size)
        ]

    def print_field(self) -> None:
        """
        Вывод игрового поля
        """
        view_fild = [[" "] + [n for n in range(1, self.field_size + 1)]]
        for i, row in enumerate(self.game_field, start=1):
            view_fild.append([i] + row)
        print(SingleTable(view_fild).table)

    def game_finish(self) -> bool:
        """
        Проверка на завершение игры и вывод результата.
        """
        if len(self.moves) == self.field_size**2:
            print("Ничья")
            return True
        else:
            win_mark: str = ""
            # проверяю строки
            for row in self.game_field:
                r_value: set = set(row)
                if len(r_value) == 1 and self.empty_char not in r_value:
                    win_mark = r_value.pop()
                    break
            # проверяю колонки
            for col in range(self.field_size):
                c_value: set = {row[col] for row in self.game_field}
                if len(c_value) == 1 and self.empty_char not in c_value:
                    win_mark = c_value.pop()
                    break
            # проверка главной диагонали
            base: set = {self.game_field[i][i] for i in range(self.field_size)}
            if len(base) == 1 and self.empty_char not in base:
                win_mark = base.pop()
            # проверка побочной диагонали
            side: set = {
                self.game_field[i][self.field_size - i - 1]
                for i in range(self.field_size)
            }
            if len(side) == 1 and self.empty_char not in side:
                win_mark = side.pop()

            if win_mark == "":
                return False

            if win_mark == self.player_mark:
                print("Игрок выиграл")
            else:
                print("Компьютер выиграл")
            self.print_field()

            return True

    def main_loop(self):
        while not self.game_finish():
            if self.player_move:
                self.print_field()
                x, y = self.get_player_coord()
                self.make_move(x, y, self.player_mark)
            else:
                x = randint(0, self.field_size - 1)
                y = randint(0, self.field_size - 1)
                self.make_move(x, y, self.enemy_mark)

    def make_move(self, x: int, y: int, mark: str):
        """
        Проеверяет ход и устанавливает в координаты метку ходящего
        """
        if (x, y) in self.moves:
            print("Ход уже был сделан ранее")
            return
        self.game_field[x][y] = mark
        self.player_move = not self.player_move
        self.moves.append((x, y))

    def get_player_coord(self) -> tuple[int, int]:
        """
        Получение координтат хода игрока и проверка их на валидность,
        c преобразованием к нужным значениям.
        """
        c_text = input(
            "Введите номер строки и колонки своего хода через пробел: "
        ).split()
        if len(c_text) == 2:
            try:
                c_list = list(
                    filter(lambda x: x > 0
                           and x <= self.field_size, map(int, c_text))
                )
                if len(c_list) == 2:
                    return c_list[0] - 1, c_list[1] - 1
                else:
                    print(f"Номер должен быть в диапазоне "
                          f"от 1 до {self.field_size}")
                    return self.get_player_coord()
            except ValueError:
                print("Номер строки и колонки должены быть цифрами")
                return self.get_player_coord()
        else:
            print("Должно быть укзано 2 цифры через пробел")
            return self.get_player_coord()


if __name__ == "__main__":
    game = TicTacToe()
    game.main_loop()
