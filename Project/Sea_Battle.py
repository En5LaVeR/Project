import random


class SeaBattleGame:
    def __init__(self):
        self.board_size = 6
        self.player_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ships = {'Submarine': 3, 'Destroyer-1': 2, 'Destroyer-2': 2,
                      'Patrol Boat-1': 1, 'Patrol Boat-2': 1, 'Patrol Boat-3': 1, 'Patrol Boat-4': 1}
        self.computer_ships = {'Submarine': 3, 'Destroyer-1': 2, 'Destroyer-2': 2,
                               'Patrol Boat-1': 1, 'Patrol Boat-2': 1, 'Patrol Boat-3': 1, 'Patrol Boat-4': 1}

    def print_boards(self, player=True, hide_computer_ships=True):
        print("   Player Board              Computer Board")
        print("   1 2 3 4 5 6                1 2 3 4 5 6")
        print("  -------------              -------------")
        for i in range(self.board_size):
            player_row = f"{chr(65 + i)}| {' '.join(self.player_board[i])} |"

            if hide_computer_ships:
                # Скрываем корабли на поле компьютера
                computer_row = f"{chr(65 + i)}| {' '.join([' ' if cell == 'O' else cell for cell in self.computer_board[i]])} |"
            else:
                # Отображаем корабли как "X" на поле компьютера
                computer_row = f"{chr(65 + i)}| {' '.join(['X' if cell == 'O' else cell for cell in self.computer_board[i]])} |"

            print(player_row.ljust(26), computer_row)

    def place_ships(self, board, ships, player=True):
        for ship, size in ships.items():
            while True:
                if player:
                    print(f"Расставьте корабль '{ship}' ({size} клеток):")
                    orientation = input("Выберите ориентацию (h - горизонтально/ v - вертикально): ").lower()
                    start_pos = input("Введите начальные координаты (например, A3): ").upper()
                else:
                    orientation = random.choice(['h', 'v'])
                    start_row = random.randint(0, self.board_size - 1)
                    start_col = random.randint(0, self.board_size - 1)
                    start_pos = f"{chr(65 + start_row)}{start_col + 1}"

                try:
                    # Проверяем формат ввода начальных координат
                    if len(start_pos) != 2 or not ('A' <= start_pos[0] <= chr(65 + self.board_size - 1)) or not (
                            '1' <= start_pos[1] <= str(self.board_size)):
                        raise ValueError("Неверный формат ввода. Попробуйте снова.")

                    start_row, start_col = ord(start_pos[0]) - 65, int(start_pos[1]) - 1

                    # Проверяем, что корабль может быть размещен в выбранной позиции
                    if (player and orientation == 'h' and start_col + size <= self.board_size and
                            all(board[start_row][start_col + i] == ' ' for i in range(size)) and
                            all(board[i][j] == ' ' for i in
                                range(max(0, start_row - 1), min(self.board_size, start_row + 2))
                                for j in range(max(0, start_col - 1), min(self.board_size, start_col + size + 1)))):
                        for i in range(size):
                            board[start_row][start_col + i] = 'O'
                        break
                    elif (player and orientation == 'v' and start_row + size <= self.board_size and
                          all(board[start_row + i][start_col] == ' ' for i in range(size)) and
                          all(board[i][j] == ' ' for i in
                              range(max(0, start_row - 1), min(self.board_size, start_row + size + 1))
                              for j in range(max(0, start_col - 1), min(self.board_size, start_col + 2)))):
                        for i in range(size):
                            board[start_row + i][start_col] = 'O'
                        break
                    elif (not player and orientation == 'h' and start_col + size <= self.board_size and
                          all(board[start_row][start_col + i] == ' ' for i in range(size)) and
                          all(board[i][j] == ' ' for i in
                              range(max(0, start_row - 1), min(self.board_size, start_row + 2))
                              for j in range(max(0, start_col - 1), min(self.board_size, start_col + size + 1)))):
                        for i in range(size):
                            board[start_row][start_col + i] = 'O'
                        break
                    elif (not player and orientation == 'v' and start_row + size <= self.board_size and
                          all(board[start_row + i][start_col] == ' ' for i in range(size)) and
                          all(board[i][j] == ' ' for i in
                              range(max(0, start_row - 1), min(self.board_size, start_row + size + 1))
                              for j in range(max(0, start_col - 1), min(self.board_size, start_col + 2)))):
                        for i in range(size):
                            board[start_row + i][start_col] = 'O'
                        break
                    else:
                        raise ValueError("Корабль не может быть размещен здесь. Попробуйте снова.")
                except ValueError as e:
                    print(e)

            self.print_boards(player)

    def play(self):
        print("Добро пожаловать в игру 'Морской бой'!")
        self.place_ships(self.player_board, self.ships, player=True)  # для игрока
        self.place_ships(self.computer_board, self.computer_ships, player=False)  # для компьютора

        while any('O' in row for row in self.player_board) and any('O' in row for row in self.computer_board):
            self.print_boards()  # Скрыть расстановку компьютерных кораблей
            self.player_turn()
            if any('O' in row for row in self.computer_board):
                self.computer_turn()

        self.print_boards()
        if not any('O' in row for row in self.computer_board):
            print("Вы победили! Все корабли компьютера уничтожены.")
        else:
            print("Вы проиграли! Ваши корабли потоплены.")

    def player_turn(self):
        print("\nВаш ход!")
        while True:
            try:
                guess = input("Введите координаты выстрела (например, A3): ").upper()
                if len(guess) != 2 or not ('A' <= guess[0] <= chr(65 + self.board_size - 1)) or not (
                        '1' <= guess[1] <= str(self.board_size)):
                    raise ValueError("Неверный формат ввода. Попробуйте снова.")
                row, col = ord(guess[0]) - 65, int(guess[1]) - 1

                # Проверяем, был ли сделан выстрел в эту клетку ранее
                if self.computer_board[row][col] == 'X' or self.computer_board[row][col] == '-':
                    raise ValueError("Вы уже стреляли в эту клетку. Попробуйте снова.")

                # Проверяем, попал ли выстрел в корабль соперника
                if self.computer_board[row][col] == 'O':
                    print("Попадание!")
                    self.computer_board[row][col] = 'X'
                else:
                    print("Мимо!")
                    self.computer_board[row][col] = 'T'

                break
            except ValueError as e:
                print(e)

    def computer_turn(self):
        print("\nХод компьютера!")
        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            if self.player_board[row][col] == ' ' or self.player_board[row][col] == 'O':
                break

        if self.player_board[row][col] == 'O':
            print("Компьютер попал в ваш корабль!")
            self.player_board[row][col] = 'X'
        else:
            print("Компьютер промахнулся!")
            self.player_board[row][col] = 'T'


if __name__ == "__main__":
    game = SeaBattleGame()
    game.play()
