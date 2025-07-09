from tkinter import *
from tkinter import ttk


DIMENSOES = (600, 600)  # Define the dimensions of the grid
cell_size = 20  # Size of each cell in pixels
offset = 8
canvas_row = 5

class CellAutomaton:
    """Main Class"""

    def __init__(self, root):
        
        self.cell_grid_list_cur = []
        self.root = root
        self.alive_rules = [2, 3]
        self.dead_rules = [3]
        self.after_ID = None

        main_frame = ttk.Frame(root)
        main_frame.grid(row=0, column=0, sticky="N S W E")

        root.title("Cellular Automaton")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.running = False

        self.cell_grid_list_cur = [["black" for _ in range(DIMENSOES[0] // cell_size)] for _ in range(DIMENSOES[1] // cell_size)]
        self.cell_grid_list_next = []

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

        start_btt = ttk.Button(main_frame, text="Start", command=self.start_simulation)
        start_btt.grid(row=canvas_row + 1, column=1, sticky="N S")

        reset_btt = ttk.Button(main_frame, text="Reset", command=self.break_simulation)
        reset_btt.grid(row=canvas_row + 2, column=1, sticky="N S")
    
    def draw_grid(self, event=None):
        """Draw the grid on the canvas."""

        for i in range(DIMENSOES[0] // cell_size):
            for j in range(DIMENSOES[1] // cell_size):
                self.cell_grid.create_rectangle(i*cell_size + offset, j*cell_size  + offset, (i + 1)*cell_size  + offset, (j + 1)*cell_size  + offset, outline="gray", fill=self.cell_grid_list_cur[i][j])

    def toggle_cell(self, event):

        row = (event.x - offset)//cell_size
        col = (event.y - offset)//cell_size
        if (DIMENSOES[0]//cell_size) <= row < 0 and (DIMENSOES[1]//cell_size) <= col < 0:
            return
        if self.cell_grid_list_cur[row][col] == "black":
            self.cell_grid_list_cur[row][col] = "white"
        else:
            self.cell_grid_list_cur[row][col] = "black"
        
        self.cell_grid.create_rectangle(row*cell_size + offset, col*cell_size  + offset, (row + 1)*cell_size  + offset, (col + 1)*cell_size  + offset, outline="gray", fill=self.cell_grid_list_cur[row][col])
    
    def get_neighbors(self, row, col):
        total_alive = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                cur_row = row + i
                cur_col = col + j
                if cur_row < 0 or cur_row >= (DIMENSOES[0]//cell_size) or cur_col < 0 or cur_col >= (DIMENSOES[1]//cell_size):
                    continue
                if self.cell_grid_list_cur[cur_row][cur_col] == "white":
                    total_alive += 1
        return total_alive
    
    def get_rules(self):
        rules = self.rules_entry.get("1.0", "end-1c")
        self.rules = rules.split("\n")
        print(self.rules)
    
    def start_simulation(self):
        self.cell_grid.unbind("<Button-1>")
        self.get_rules()
        self.running = True
        self.simulation_loop()        

    def simulation_loop(self):
        changed = False
        self.cell_grid_list_next = [row[:] for row in self.cell_grid_list_cur]
        for i in range(DIMENSOES[0]//cell_size):
            for j in range(DIMENSOES[1]//cell_size):
                n_neighbors = self.get_neighbors(i, j)
                if self.cell_grid_list_cur[i][j] == "white":
                    if not self.apply_alive_rules(n_neighbors):
                        self.cell_grid_list_next[i][j] = "black"
                        changed = True
                else:
                    if self.apply_dead_rules(n_neighbors):
                        self.cell_grid_list_next[i][j] = "white"
                        changed = True
        self.cell_grid_list_cur = self.cell_grid_list_next
        self.draw_grid()
        if not changed:
            self.running = False
        if self.running:
            self.after_ID = self.root.after(500, self.simulation_loop)
        
    def apply_alive_rules(self, n_neighbors):
        live = False
        for i in self.alive_rules:
            if n_neighbors == i:
                live = True
                continue
        return live
    
    def apply_dead_rules(self, n_neighbors):
        live = False
        for i in self.dead_rules:
            if n_neighbors == i:
                live = True
                continue
        return live

    def break_simulation(self):
        self.running = False
        if self.after_ID is not None:
            self.root.after_cancel(self.after_ID)
            self.after_ID = None
        self.cell_grid.bind("<Button-1>", self.toggle_cell)
        
        # Reset the grid
        self.cell_grid_list_cur = [["black" for _ in range(DIMENSOES[0] // cell_size)] for _ in range(DIMENSOES[1] // cell_size)]
        self.cell_grid_list_next = []
        self.draw_grid()

if __name__ == "__main__":
    root = Tk()
    CellAutomaton(root=root)
    root.mainloop()

