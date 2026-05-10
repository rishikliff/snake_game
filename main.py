import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
UPDATE_DELAY = 150

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Snake Game")
        self.canvas = tk.Canvas(
            self.master,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="#111111",
        )
        self.canvas.pack()

        self.score_label = tk.Label(
            self.master,
            text="Score: 0",
            font=("Consolas", 14),
            fg="#ffffff",
            bg="#111111",
        )
        self.score_label.pack(pady=8)

        self.master.bind("<Up>", lambda event: self.change_direction("Up"))
        self.master.bind("<Down>", lambda event: self.change_direction("Down"))
        self.master.bind("<Left>", lambda event: self.change_direction("Left"))
        self.master.bind("<Right>", lambda event: self.change_direction("Right"))
        
        self.master.bind("<space>", lambda event: self.restart())

        # Bind 'P' key for pause/resume
        self.master.bind("<p>", lambda event: self.toggle_pause())
        self.master.bind("<P>", lambda event: self.toggle_pause())

        self.reset_game()
        self.paused = False
        self.running = True
        self.update()

    def reset_game(self):
        self.direction = "Right"
        self.next_direction = "Right"
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
                      (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                      (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
        self.score = 0
        self.apples = set()
        self.game_over = False
        self.spawn_apple()
        self.draw()
        self.score_label.config(text=f"Score: {self.score}")

    def spawn_apple(self):
        available_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake and (x, y) not in self.apples
        ]
        if available_cells:
            self.apples.add(random.choice(available_cells))

    def change_direction(self, new_direction):
        if self.game_over:
            return
        opposite = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left",
        }
        if new_direction != opposite.get(self.direction):
            self.next_direction = new_direction

    def update(self):
        if not self.game_over and not self.paused:
            self.direction = self.next_direction
            head_x, head_y = self.snake[0]
            if self.direction == "Up":
                head_y -= 1
            elif self.direction == "Down":
                head_y += 1
            elif self.direction == "Left":
                head_x -= 1
            elif self.direction == "Right":
                head_x += 1

            new_head = (head_x, head_y)

            if (
                head_x < 0
                or head_x >= GRID_WIDTH
                or head_y < 0
                or head_y >= GRID_HEIGHT
                or new_head in self.snake
            ):
                self.end_game()
            else:
                self.snake.insert(0, new_head)
                if new_head in self.apples:
                    self.apples.remove(new_head)
                    self.score += 1
                    self.score_label.config(text=f"Score: {self.score}")
                    self.spawn_apple()
                else:
                    self.snake.pop()
                self.draw()
        self.master.after(UPDATE_DELAY, self.update)

    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused
            self.draw()

    def draw(self):
        self.canvas.delete("all")

        for x, y in self.apples:
            self.draw_cell(x, y, "#ff5555")

        for index, (x, y) in enumerate(self.snake):
            color = "#53d769" if index == 0 else "#66ff88"
            self.draw_cell(x, y, color)

        if self.game_over:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE / 2,
                GRID_HEIGHT * CELL_SIZE / 2,
                text="Game Over\nPress Space to Restart",
                fill="#ffffff",
                font=("Consolas", 24, "bold"),
                justify="center",
            )
        elif self.paused:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE / 2,
                GRID_HEIGHT * CELL_SIZE / 2,
                text="Paused",
                fill="#ffff00",
                font=("Consolas", 32, "bold"),
                justify="center",
            )

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill=color, outline="#111111")

    def end_game(self):
        self.game_over = True
        self.draw()

    def restart(self):
        if self.game_over:
            self.reset_game()
            self.game_over = False
            self.just_restarted = True
            self.draw()
            self.master.after(1000, self.clear_restart_message)

        def clear_restart_message(self):
            self.just_restarted = False
            self.draw()


def main():
    root = tk.Tk()

    if getattr(self, 'just_restarted', False):
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE / 2,
                GRID_HEIGHT * CELL_SIZE / 2,
                text="Game Restarted!",
                fill="#00ffff",
                font=("Consolas", 24, "bold"),
                justify="center",
            )
    game = SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
