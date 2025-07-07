from tkinter import *
from tkinter import ttk

DIMENSOES = (600, 600)  # Define the dimensions of the grid
cell_size = 20  # Size of each cell in pixels
offset = 8
canvas_row = 5

class CellAutomaton:
    """Main Class"""

    def __init__(self, root):
        
        self.cell_grid_list = []
        self.root = root

        main_frame = ttk.Frame(root)
        main_frame.grid(row=0, column=0, sticky="N S W E")

        root.title("Cellular Automaton")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.cell_grid_list = [["black" for _ in range(DIMENSOES[0] // cell_size)] for _ in range(DIMENSOES[1] // cell_size)]

        self.cell_grid = Canvas(main_frame, width=DIMENSOES[0] + 10, height=DIMENSOES[1] + 10, bg="gray")
        self.cell_grid.grid(row=canvas_row, column=1, sticky="N S W E")

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(canvas_row + 2, weight=1)

        self.draw_grid()
        self.cell_grid.bind("<Button-1>", self.toggle_cell)

        self.rules = ()
        rules_lbl = ttk.Label(main_frame, text="RULES:")
        rules_lbl.grid(row=canvas_row - 2, column=1, sticky="N S")
        self.rules_entry = Text(main_frame, height=10)
        self.rules_entry.grid(row=canvas_row - 1, column=1, sticky="W E")

        start_btt = ttk.Button(main_frame, text="Start", command=self.start_simulation())
        start_btt.grid(row=canvas_row + 1, column=1, sticky="N S")
    
    def draw_grid(self, event=None):
        """Draw the grid on the canvas."""

        for i in range(DIMENSOES[0] // cell_size):
            for j in range(DIMENSOES[1] // cell_size):
                self.cell_grid.create_rectangle(i*cell_size + offset, j*cell_size  + offset, (i + 1)*cell_size  + offset, (j + 1)*cell_size  + offset, outline="gray", fill=self.cell_grid_list[i][j])

    def toggle_cell(self, event):

        row = (event.x - offset)//cell_size
        col = (event.y - offset)//cell_size

        if self.cell_grid_list[row][col] == "black":
            self.cell_grid_list[row][col] = "white"
        else:
            self.cell_grid_list[row][col] = "black"
        
        self.cell_grid.create_rectangle(row*cell_size + offset, col*cell_size  + offset, (row + 1)*cell_size  + offset, (col + 1)*cell_size  + offset, outline="gray", fill=self.cell_grid_list[row][col])
    
    def get_neighbors(self, row, col):
        total_alive = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                try:
                    if self.cell_grid_list[row + i][col + j] == "white":
                        total_alive += 1
                finally:
                    continue
        return total_alive
    
    def get_rules(self):
        rules = self.rules_entry.get("1.0", "end-1c")
        self.rules = rules.split("\n")
        print(self.rules)
    
    def start_simulation(self):
        self.cell_grid.unbind("<Button-1>")
        self.get_rules()

if __name__ == "__main__":
    root = Tk()
    CellAutomaton(root=root)
    root.mainloop()

