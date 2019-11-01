import tkinter as tk
import random
from threading import Timer
from copy import deepcopy
import logging
import sys
import os

font = ('Comic Sans MS', 12)
large_font = ('Comic Sans MS', 22, 'bold')

diff = 1
mode = 1
start = 1
mark = 1
stop = 0
cpu_move = 0
stop_copy = 0


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


icon = resource_path('tictactoe.ico')


class TicTacToe(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Main)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class Main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='Tic Tac Toe', font=large_font).grid(row=0, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=1, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=2, sticky='nsew')
        tk.Button(self, text='Start game', font=font,
                  command=lambda: master.switch_frame(Game)).grid(row=3, sticky='nsew')
        tk.Button(self, text='Options', font=font,
                  command=lambda: master.switch_frame(Options)).grid(row=4, sticky='nsew')
        tk.Button(self, text='Exit', font=font, command=lambda: master.destroy()).grid(row=5, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=6, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=7, sticky='nsew')
        tk.Label(self, text=' ', font=large_font).grid(row=8, sticky='nsew')
        tk.Label(self, text='made by: Patryk Kerlin').grid(row=9, sticky='nsew')


class Options(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='Options', font=large_font).grid(row=0, columnspan=3)
        self.choose()
        tk.Button(self, text='Main menu', font=font,
                  command=lambda: master.switch_frame(Main)).grid(row=11, columnspan=3, sticky='nsew')

    def choose(self):
        global mode
        emp_lab = tk.StringVar()
        empty_label1 = tk.Label(self, textvariable=emp_lab)
        empty_label2 = tk.Label(self, textvariable=emp_lab)
        empty_label3 = tk.Label(self, textvariable=emp_lab)
        empty_label4 = tk.Label(self, textvariable=emp_lab)
        emp_lab.set('          ')
        empty_label1.grid(row=1, columnspan=3)
        empty_label2.grid(row=6, columnspan=3)
        empty_label3.grid(row=10, columnspan=3)
        empty_label4.grid(row=2, column=1)

        mod_lab = tk.StringVar()
        mode_label = tk.Label(self, textvariable=mod_lab, font=font)
        mod_lab.set('Game mode:')
        mode_label.grid(row=2, column=0, sticky='nsew')
        self.mode = tk.IntVar(self, value=mode)
        r1 = tk.Radiobutton(self, text='Player vs. CPU', font=font, variable=self.mode, value=1,
                            command=self.mode_diff_start_on, indicatoron=0)
        r1.grid(row=3, column=0, sticky='nsew')
        r2 = tk.Radiobutton(self, text='Player vs. Player', font=font, variable=self.mode, value=2,
                            command=self.player_player, indicatoron=0)
        r2.grid(row=4, column=0, sticky='nsew')
        r3 = tk.Radiobutton(self, text='CPU vs. CPU', font=font, variable=self.mode, value=3,
                            command=self.mode_diff_start_off, indicatoron=0)
        r3.grid(row=5, column=0, sticky='nsew')

        dif_lab = tk.StringVar()
        difficulty_label = tk.Label(self, textvariable=dif_lab, font=font)
        dif_lab.set('Difficulty level:')
        difficulty_label.grid(row=2, column=2, sticky='nsew')
        self.diff = tk.IntVar(self, value=diff)
        if mode == 1:
            self.diff_on()
        else:
            self.diff_off()

        mod_lab = tk.StringVar()
        mode_label = tk.Label(self, textvariable=mod_lab, font=font)
        mod_lab.set('First move:')
        mode_label.grid(row=7, column=0, sticky='nsew')
        self.start = tk.IntVar(self, value=start)
        if mode == 1:
            self.start_on()
        else:
            self.start_off()

        mod_lab = tk.StringVar()
        mode_label = tk.Label(self, textvariable=mod_lab, font=font)
        mod_lab.set('Mark:')
        mode_label.grid(row=7, column=2, sticky='nsew')
        self.mark = tk.IntVar(self, value=mark)
        if mode == 1:
            self.mark_1_player()
        elif mode == 2:
            self.mark_2_players()
        elif mode == 3:
            self.mark_off()

    def mark_1_player(self):
        global mark
        self.mark = tk.IntVar(self, value=mark)
        r8 = tk.Radiobutton(self, text='Player - X\nCPU - O', font=font, variable=self.mark, value=1,
                            command=self.mark_change, indicatoron=0)
        r8.grid(row=8, column=2, sticky='nsew')
        r9 = tk.Radiobutton(self, text='Player - 0\nCPU - X', font=font, variable=self.mark, value=2,
                            command=self.mark_change, indicatoron=0)
        r9.grid(row=9, column=2, sticky='nsew')

    def mark_2_players(self):
        global mark
        self.mark = tk.IntVar(self, value=mark)
        r8 = tk.Radiobutton(self, text='Player 1 - X\nPlayer 2 - O', font=font, variable=self.mark, value=1,
                            command=self.mark_change, indicatoron=0)
        r8.grid(row=8, column=2, sticky='nsew')
        r9 = tk.Radiobutton(self, text='Player 1 - O\nPlayer 2 - X', font=font, variable=self.mark, value=2,
                            command=self.mark_change, indicatoron=0)
        r9.grid(row=9, column=2, sticky='nsew')

    def mark_off(self):
        r8 = tk.Radiobutton(self, text='Player - X\nCPU - O', font=font, value=0,
                            command=self.mark_change, indicatoron=0, state='disabled')
        r8.grid(row=8, column=2, sticky='nsew')
        r9 = tk.Radiobutton(self, text='Player - 0\nCPU - X', font=font, value=0,
                            command=self.mark_change, indicatoron=0, state='disabled')
        r9.grid(row=9, column=2, sticky='nsew')

    def start_on(self):
        global start
        self.start = tk.IntVar(self, value=start)
        r6 = tk.Radiobutton(self, text='Player', font=font, variable=self.start, value=1,
                            command=self.start_change, indicatoron=0)
        r6.grid(row=8, column=0, sticky='nsew')
        r7 = tk.Radiobutton(self, text='CPU', font=font, variable=self.start, value=2,
                            command=self.start_change, indicatoron=0)
        r7.grid(row=9, column=0, sticky='nsew')

    def start_off(self):
        r6 = tk.Radiobutton(self, text='Player', font=font, value=0,
                            command=self.start_change, indicatoron=0, state='disabled')
        r6.grid(row=8, column=0, sticky='nsew')
        r7 = tk.Radiobutton(self, text='CPU', font=font, value=0,
                            command=self.start_change, indicatoron=0, state='disabled')
        r7.grid(row=9, column=0, sticky='nsew')

    def diff_on(self):
        global diff
        self.diff = tk.IntVar(self, value=diff)
        r4 = tk.Radiobutton(self, text='Easy', font=font, variable=self.diff, value=1,
                            command=self.diff_change, indicatoron=0)
        r4.grid(row=3, column=2, sticky='nsew')
        r5 = tk.Radiobutton(self, text='Hard', font=font, variable=self.diff, value=2,
                            command=self.diff_change, indicatoron=0)
        r5.grid(row=4, column=2, sticky='nsew')

    def diff_off(self):
        r4 = tk.Radiobutton(self, text='Easy', font=font, value=0,
                            command=self.diff_change, indicatoron=0, state='disabled')
        r4.grid(row=3, column=2, sticky='nsew')
        r5 = tk.Radiobutton(self, text='Hard', font=font, value=0,
                            command=self.diff_change, indicatoron=0, state='disabled')
        r5.grid(row=4, column=2, sticky='nsew')

    def mode_change(self):
        global mode, mark, diff, start
        mode = self.mode.get()
        mark = 1
        diff = 1
        start = 1

    def diff_change(self):
        global diff
        diff = self.diff.get()

    def start_change(self):
        global start
        start = self.start.get()

    def mark_change(self):
        global mark
        mark = self.mark.get()

    def mode_diff_start_off(self):
        self.mode_change()
        self.diff_off()
        self.start_off()
        self.mark_off()

    def player_player(self):
        self.mode_change()
        self.diff_off()
        self.start_off()
        self.mark_2_players()

    def mode_diff_start_on(self):
        self.mode_change()
        self.diff_on()
        self.start_on()
        self.mark_1_player()


class Game(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        emp_lab = tk.StringVar()
        emp_lab2 = tk.StringVar()
        empty_label1 = tk.Label(self, textvariable=emp_lab)
        empty_label2 = tk.Label(self, textvariable=emp_lab)
        empty_label3 = tk.Label(self, textvariable=emp_lab)
        empty_label4 = tk.Label(self, textvariable=emp_lab2)
        empty_label5 = tk.Label(self, textvariable=emp_lab2)
        emp_lab.set(' ')
        emp_lab2.set('                         ')
        empty_label1.grid(row=1, column=0, columnspan=5, sticky='nsew')
        empty_label2.grid(row=4, column=1, sticky='nsew')
        empty_label3.grid(row=4, column=3, sticky='nsew')
        empty_label4.grid(row=3, column=0, sticky='nsew')
        empty_label5.grid(row=3, column=2, sticky='nsew')
        global canvas
        canvas = tk.Canvas(self, width=300, height=300)
        canvas.grid(row=2, column=0, columnspan=5, sticky='nsew')
        self.first_turn()
        self.draw_board()
        if mode == 1 or mode == 2:
            canvas.bind('<Button-1>', self.player_move)
        if mode == 3 or start == 2:
            Timer(1.5, self.cpu_move).start()
        tk.Label(self, text='Tic Tac Toe', font=large_font).grid(row=0, column=0, columnspan=5, sticky='nsew')
        tk.Button(self, text='Main\nmenu', font=font,
                  command=lambda: master.switch_frame(Main)).grid(row=4, column=0, sticky='nsew')
        tk.Button(self, text='Reset', font=font,
                  command=lambda: self.reset(master)).grid(row=4, column=2, sticky='nsew')
        self.turn_indicator()

    def reset(self, master):
        self.destroy()
        master.switch_frame(Game)

    def draw_board(self):
        canvas.create_line(0, 100, 300, 100, width=5)
        canvas.create_line(0, 200, 300, 200, width=5)
        canvas.create_line(100, 0, 100, 300, width=5)
        canvas.create_line(200, 0, 200, 300, width=5)

    def first_turn(self):
        global turn, stop, board, available_moves, cpu_move
        available_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        board = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: ''}
        stop = 0
        if mode == 1:
            if start == 1:
                if mark == 1:
                    turn = 'X'
                elif mark == 2:
                    turn = 'O'
            elif start == 2:
                if mark == 1:
                    turn = 'O'
                elif mark == 2:
                    turn = 'X'
        elif mode == 2:
            if mark == 1:
                turn = 'X'
            elif mark == 2:
                turn = 'O'
        elif mode == 3:
            turn = 'X'
        if start == 1:
            cpu_move = 0
        if start == 2:
            cpu_move = 1

    def player_move(self, event):
        global key, cpu_move
        if mode == 1 and mark == 1 and turn == 'X'\
                or mode == 1 and mark == 2 and turn == 'O' or mode == 2:
            if 1 <= event.x <= 299 and 1 <= event.y <= 299:
                if board[1] == '' and stop == 0:
                    if 1 <= event.x <= 99 and 1 <= event.y <= 99:
                        key = 1
                        self.coords()
                        cpu_move = 0
                        self.draw_move()
                if board[2] == '' and stop == 0:
                    if 101 <= event.x <= 199 and 1 <= event.y <= 99:
                        key = 2
                        self.coords()
                        cpu_move = 0
                        self.draw_move()
                if board[3] == '' and stop == 0:
                    if 201 <= event.x <= 299 and 1 <= event.y <= 99:
                        key = 3
                        self.coords()
                        cpu_move = 0
                        self.draw_move()
                if board[4] == '' and stop == 0:
                    if 1 <= event.x <= 99 and 101 <= event.y <= 199:
                        key = 4
                        self.coords()
                        cpu_move = 0
                        self.draw_move()
                if board[5] == '' and stop == 0:
                    if 101 <= event.x <= 199 and 101 <= event.y <= 199:
                        key = 5
                        self.coords()
                        cpu_move = 0
                        self.draw_move()
                if board[6] == '' and stop == 0:
                    if 201 <= event.x <= 299 and 101 <= event.y <= 199:
                        key = 6
                        self.coords()
                        cpu_move = 0
                        self.draw_move()
                if board[7] == '' and stop == 0:
                    if 1 <= event.x <= 99 and 201 <= event.y <= 299:
                        key = 7
                        self.coords()
                        cpu_move = 0
                        self.draw_move()
                if board[8] == '' and stop == 0:
                    if 101 <= event.x <= 199 and 201 <= event.y <= 299:
                        key = 8
                        self.coords()
                        cpu_move = 0
                        self.draw_move()
                if board[9] == '' and stop == 0:
                    if 201 <= event.x <= 299 and 201 <= event.y <= 299:
                        key = 9
                        self.coords()
                        cpu_move = 0
                        self.draw_move()

    def change_turn_cpu_cpu(self):
        global turn
        if turn == 'O':
            turn = 'X'
            if len(available_moves) > 0:
                Timer(1.5, self.cpu_move).start()
        elif turn == 'X':
            turn = 'O'
            if len(available_moves) > 0:
                Timer(1.5, self.cpu_move).start()

    def change_turn_player_cpu(self):
        global turn, cpu_move
        if turn == 'O':
            turn = 'X'
            if cpu_move == 0:
                if len(available_moves) > 0:
                    if diff == 1:
                        Timer(1.0, self.cpu_player_move).start()
                    elif diff == 2:
                        Timer(1.0, self.ai_player_move).start()
                cpu_move = 1
        elif turn == 'X':
            turn = 'O'
            if cpu_move == 0:
                if len(available_moves) > 0:
                    if diff == 1:
                        Timer(1.0, self.cpu_player_move).start()
                    elif diff == 2:
                        Timer(1.0, self.ai_player_move).start()
                cpu_move = 1

    def change_turn_player_player(self):
        global turn
        if turn == 'O':
            turn = 'X'
        elif turn == 'X':
            turn = 'O'

    def turn_selector(self):
        if mode == 1:
            self.change_turn_player_cpu()
        if mode == 2:
            self.change_turn_player_player()
        if mode == 3:
            self.change_turn_cpu_cpu()

    def draw_move(self):
        global board
        if turn == 'X':
            canvas.create_line(x1, y1, x2, y2, width=10)
            canvas.create_line(x1, y2, x2, y1, width=10)
            board[key] = 'X'
            self.check_win()
            self.turn_selector()
        elif turn == 'O':
            canvas.create_oval(x1, y1, x2, y2, width=10)
            board[key] = 'O'
            self.check_win()
            self.turn_selector()
        self.turn_indicator()

    def popup_window_win(self):
        popup = tk.Toplevel()
        tk.Label(popup).pack()
        tk.Label(popup, text='Winner:', font=font).pack()
        tk.Label(popup, text=turn, font=large_font).pack()
        tk.Label(popup).pack()
        tk.Button(popup, text='Close', font=font, command=lambda: popup.destroy()).pack()
        tk.Label(popup).pack()
        popup.geometry('170x170+10+10')
        popup.resizable(False, False)
        popup.title('')
        popup.iconbitmap(icon)

    def popup_window_tie(self):
        popup = tk.Toplevel()
        tk.Label(popup).pack()
        tk.Label(popup, text='No one won!', font=font).pack()
        tk.Label(popup).pack()
        tk.Button(popup, text='Close', font=font, command=lambda: popup.destroy()).pack()
        tk.Label(popup).pack()
        popup.geometry('170x125+10+10')
        popup.resizable(False, False)
        popup.title('')
        popup.iconbitmap(icon)

    def check_win(self):
        global stop, win
        if board[1] == board[2] == board[3] == 'X'\
                or board[1] == board[2] == board[3] == 'O':
            stop = 1
            win = 1
            self.win_line()
            self.popup_window_win()
            self.logs()
        elif board[4] == board[5] == board[6] == 'X'\
                or board[4] == board[5] == board[6] == 'O':
            stop = 1
            win = 2
            self.win_line()
            self.popup_window_win()
            self.logs()
        elif board[7] == board[8] == board[9] == 'X'\
                or board[7] == board[8] == board[9] == 'O':
            stop = 1
            win = 3
            self.win_line()
            self.popup_window_win()
            self.logs()
        elif board[1] == board[4] == board[7] == 'X'\
                or board[1] == board[4] == board[7] == 'O':
            stop = 1
            win = 4
            self.win_line()
            self.popup_window_win()
            self.logs()
        elif board[2] == board[5] == board[8] == 'X'\
                or board[2] == board[5] == board[8] == 'O':
            stop = 1
            win = 5
            self.win_line()
            self.popup_window_win()
            self.logs()
        elif board[3] == board[6] == board[9] == 'X'\
                or board[3] == board[6] == board[9] == 'O':
            stop = 1
            win = 6
            self.win_line()
            self.popup_window_win()
            self.logs()
        elif board[1] == board[5] == board[9] == 'X'\
                or board[1] == board[5] == board[9] == 'O':
            stop = 1
            win = 7
            self.win_line()
            self.popup_window_win()
            self.logs()
        elif board[3] == board[5] == board[7] == 'X'\
                or board[3] == board[5] == board[7] == 'O':
            stop = 1
            win = 8
            self.win_line()
            self.popup_window_win()
            self.logs()
        elif '' not in board.values():
            stop = 1
            self.popup_window_tie()
        self.turn_indicator()

    def cpu_move(self):
        global available_moves, key
        random_move = random.choice(available_moves)
        available_moves.remove(random_move)
        if random_move == 1 and stop == 0:
            key = 1
            self.coords()
            self.draw_move()
        elif random_move == 2 and stop == 0:
            key = 2
            self.coords()
            self.draw_move()
        elif random_move == 3 and stop == 0:
            key = 3
            self.coords()
            self.draw_move()
        elif random_move == 4 and stop == 0:
            key = 4
            self.coords()
            self.draw_move()
        elif random_move == 5 and stop == 0:
            key = 5
            self.coords()
            self.draw_move()
        elif random_move == 6 and stop == 0:
            key = 6
            self.coords()
            self.draw_move()
        elif random_move == 7 and stop == 0:
            key = 7
            self.coords()
            self.draw_move()
        elif random_move == 8 and stop == 0:
            key = 8
            self.coords()
            self.draw_move()
        elif random_move == 9 and stop == 0:
            key = 9
            self.coords()
            self.draw_move()

    def coords(self):
        global key, x1, x2, y1, y2
        if key == 1:
            x1, x2, y1, y2 = 15, 85, 15, 85
        elif key == 2:
            x1, x2, y1, y2 = 115, 185, 15, 85
        elif key == 3:
            x1, x2, y1, y2 = 215, 285, 15, 85
        elif key == 4:
            x1, x2, y1, y2 = 15, 85, 115, 185
        elif key == 5:
            x1, x2, y1, y2 = 115, 185, 115, 185
        elif key == 6:
            x1, x2, y1, y2 = 215, 285, 115, 185
        elif key == 7:
            x1, x2, y1, y2 = 15, 85, 215, 285
        elif key == 8:
            x1, x2, y1, y2 = 115, 185, 215, 285
        elif key == 9:
            x1, x2, y1, y2 = 215, 285, 215, 285

    def cpu_player_move(self):
        global available_moves, key
        if len(available_moves) >= 2:
            available_moves.remove(key)
            random_move = random.choice(available_moves)
            available_moves.remove(random_move)
            if random_move == 1 and stop == 0:
                key = 1
                self.coords()
                self.draw_move()
            elif random_move == 2 and stop == 0:
                key = 2
                self.coords()
                self.draw_move()
            elif random_move == 3 and stop == 0:
                key = 3
                self.coords()
                self.draw_move()
            elif random_move == 4 and stop == 0:
                key = 4
                self.coords()
                self.draw_move()
            elif random_move == 5 and stop == 0:
                key = 5
                self.coords()
                self.draw_move()
            elif random_move == 6 and stop == 0:
                key = 6
                self.coords()
                self.draw_move()
            elif random_move == 7 and stop == 0:
                key = 7
                self.coords()
                self.draw_move()
            elif random_move == 8 and stop == 0:
                key = 8
                self.coords()
                self.draw_move()
            elif random_move == 9 and stop == 0:
                key = 9
                self.coords()
                self.draw_move()

    def copy_board(self):
        global board_copy
        board_copy = deepcopy(board)

    def ai_player_move(self):
        global key, stop_copy, board_copy, available_moves
        best_move = []
        available_moves.remove(key)
        if stop == 0:
            if 5 in available_moves:
                key = 5
                self.coords()
                self.draw_move()
                available_moves.remove(key)
                best_move.clear()
                stop_copy = 0
            elif 5 not in available_moves:
                if turn == 'X' or turn == 'O':
                    for key1 in available_moves:
                        self.copy_board()
                        board_copy[key1] = turn
                        self.check_win_ai()
                        if stop_copy == 1:
                            best_move.append(key1)
                if turn == 'O':
                    for key2 in available_moves:
                        self.copy_board()
                        board_copy[key2] = 'X'
                        self.check_win_ai()
                        if stop_copy == 1:
                            best_move.append(key2)
                elif turn == 'X':
                    for key3 in available_moves:
                        self.copy_board()
                        board_copy[key3] = 'O'
                        self.check_win_ai()
                        if stop_copy == 1:
                            best_move.append(key3)
                if turn == 'X' or turn == 'O':
                    for key4 in available_moves:
                        self.copy_board()
                        board_copy[key4] = turn
                        self.check_win_ai()
                        if stop_copy == 1:
                            best_move.append(key4)
                        elif stop_copy == 0:
                            for key5 in available_moves:
                                board_copy[key5] = turn
                                self.check_win_ai()
                                if stop_copy == 1:
                                    best_move.append(key5)
                if turn == 'X' or turn == 'O':
                    for move in available_moves:
                        best_move.append(move)
                if len(best_move) > 0:
                    corners = [1, 3, 7, 9]
                    if len(best_move) > 20:
                        new_move = list(set(best_move).intersection(corners))
                        key = new_move[0]
                    else:
                        key = best_move[0]
                    if key in available_moves:
                        for w in range(1):
                            self.coords()
                            self.draw_move()
                            available_moves.remove(key)
                            best_move.clear()
                            stop_copy = 0

    def check_win_ai(self):
        global stop_copy
        if board_copy[1] == board_copy[2] == board_copy[3] == 'X'\
                or board_copy[1] == board_copy[2] == board_copy[3] == 'O':
            stop_copy = 1
        elif board_copy[4] == board_copy[5] == board_copy[6] == 'X'\
                or board_copy[4] == board_copy[5] == board_copy[6] == 'O':
            stop_copy = 1
        elif board_copy[7] == board_copy[8] == board_copy[9] == 'X'\
                or board_copy[7] == board_copy[8] == board_copy[9] == 'O':
            stop_copy = 1
        elif board_copy[1] == board_copy[4] == board_copy[7] == 'X'\
                or board_copy[1] == board_copy[4] == board_copy[7] == 'O':
            stop_copy = 1
        elif board_copy[2] == board_copy[5] == board_copy[8] == 'X'\
                or board_copy[2] == board_copy[5] == board_copy[8] == 'O':
            stop_copy = 1
        elif board_copy[3] == board_copy[6] == board_copy[9] == 'X'\
                or board_copy[3] == board_copy[6] == board_copy[9] == 'O':
            stop_copy = 1
        elif board_copy[1] == board_copy[5] == board_copy[9] == 'X'\
                or board_copy[1] == board_copy[5] == board_copy[9] == 'O':
            stop_copy = 1
        elif board_copy[3] == board_copy[5] == board_copy[7] == 'X'\
                or board_copy[3] == board_copy[5] == board_copy[7] == 'O':
            stop_copy = 1

    def win_line(self):
        x3, y3, x4, y4 = 0, 0, 0, 0
        if win != 0:
            if win == 1:
                x3, y3, x4, y4 = 5, 50, 295, 50
            elif win == 2:
                x3, y3, x4, y4 = 5, 150, 295, 150
            elif win == 3:
                x3, y3, x4, y4 = 5, 250, 295, 250
            elif win == 4:
                x3, y3, x4, y4 = 50, 5, 50, 295
            elif win == 5:
                x3, y3, x4, y4 = 150, 5, 150, 295
            elif win == 6:
                x3, y3, x4, y4 = 250, 5, 250, 295
            elif win == 7:
                x3, y3, x4, y4 = 5, 5, 295, 295
            elif win == 8:
                x3, y3, x4, y4 = 5, 295, 295, 5
            canvas.create_line(x3, y3, x4, y4, width=20, fill='red')

    def logs(self):
        logging.basicConfig(filename='log.txt', level=20, format='%(asctime)s %(message)s')
        if mode == 1:
            logging.info(('Game mode:', mode, 'Diffculty level:', diff, ' Winner:', turn))
        else:
            logging.info(('Game mode:', mode, 'Winner -', turn))

    def turn_indicator(self):
        nxt_trn = tk.StringVar()
        next_turn = tk.Label(self, textvariable=nxt_trn, font=font, relief='sunken')
        if turn == 'O' and stop == 0:
            nxt_trn.set('Your turn:\nO')
        elif turn == 'X' and stop == 0:
            nxt_trn.set('Your turn:\nX')
        elif stop == 1:
            nxt_trn.set('Game\nover')
        next_turn.grid(row=4, column=4, sticky='nsew')


if __name__ == '__main__':
    app = TicTacToe()
    app.title('Tic Tac Toe')
    app.geometry('400x470+10+10')
    app.resizable(False, False)
    app.iconbitmap(icon)
    app.mainloop()
