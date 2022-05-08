# -*- coding: utf-8 -*-
from tkinter import Tk, Frame, Button, Label
import random

WIDTH = 1440
HEIGHT = 720
GRID = 6
CELL_COUNT = GRID **2
MINES_CNT = CELL_COUNT // 4

def height_prct(percentage):
    return HEIGHT * 0.01 * percentage

def width_prct(percentage):
    return WIDTH * 0.01 * percentage

class Cell:
    all = []
    cell_count = CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append to list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=4,
            height=4,
            text ="",
            bg='#d9d9d9',
        )
        btn.bind('<Button-1>', self.left_click_actions) #left click
        btn.bind('<Button-3>', self.right_click_actions) #right click
        self.cell_btn_object = btn

    @staticmethod #usage case of the class and not the instance Python OOP Introduction of him
    def create_cell_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"remaining cells: {Cell.cell_count}",
            width=20,
            height=4,
            font=("", 24)
                )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell()
            if Cell.cell_count == 0:
                Cell.cell_count_label_object.configure(
                    text=f"Congratulations!!! \nGame ended"
                    )

    def get_cell_by_axis(self,x,y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
    @property
    def surrounded_cells(self):
        cells = []
        for x in range(-1,2):
            if self.x - x < 0 or self.x - x == GRID:
                    continue
            for y in range(-1,2):
                if self.y - y < 0 or self.y - y == GRID:
                    continue
                cells.append(self.get_cell_by_axis(self.x - x, self.y - y))
        return cells

    @property
    def count_surrounded_mines(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if self.cell_btn_object.cget('text') == "":
            self.cell_btn_object.configure(text=self.count_surrounded_mines)
            if self.count_surrounded_mines == 0:
                for cell in self.surrounded_cells:
                    cell.show_cell()
            Cell.cell_count -= 1
            Cell.cell_count_label_object.configure(
                    text=f"remaining cells: {Cell.cell_count}"
                    )
            self.cell_btn_object.unbind('<Button-1>')
            self.cell_btn_object.unbind('<Button-3>')

    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        Cell.cell_count_label_object.configure(
                    text=f"MINE!!! Game Over"
                    )
        for cell in Cell.all:
            if cell.cell_btn_object.cget('text') == "":
                cell.cell_btn_object.unbind('<Button-1>')
                cell.cell_btn_object.unbind('<Button-3>')

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                    bg='orange'
                    )
            Cell.cell_count -= 1
        else:
            self.cell_btn_object.configure(
                    bg='#d9d9d9'
                    )
            Cell.cell_count += 1
        self.is_mine_candidate = not self.is_mine_candidate
        Cell.cell_count_label_object.configure(
                    text=f"remaining cells: {Cell.cell_count}"
                    )
        if Cell.cell_count == 0:
                Cell.cell_count_label_object.configure(
                    text=f"Congratulations!!! \nGame ended"
                    )

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, MINES_CNT)
        for cell in picked_cells:
            cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

# Overwrite settings of the window
root = Tk()
root.configure(bg="black")
root.geometry(f'{WIDTH}x{HEIGHT}')
root.title("Minesweeper")
root.resizable(False, False)

top_frame = Frame(
    root,
    bg="black",
    width=WIDTH,
    height=height_prct(25)
)
top_frame.place(x=0, y=0)

game_title = Label(
        top_frame,
        bg='black',
        fg='white',
        text='Minesweeper',
        font=('', 48)
        )
game_title.place(
        x=width_prct(25), y=10
        )

left_frame = Frame(
    root,
    bg="black",
    width=width_prct(25),
    height=height_prct(75)
)
left_frame.place(x=0, y=height_prct(25))

center_frame = Frame(
    root,
    bg="black",
    width=width_prct(75),
    height=height_prct(75)
)
center_frame.place(x=width_prct(25), y=height_prct(25))

for x in range(GRID):
    for y in range(GRID):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
        column=x, row=y
        )
#print(Cell.all)

Cell.create_cell_label(left_frame)
Cell.cell_count_label_object.place(
        x=10, y=0
        )

Cell.randomize_mines()



# Run the window
root.mainloop()

 #video timestamp: 58:38
#python game develeopment project using OOP. Minesweeper tutorial from FreeCodeCamp.org