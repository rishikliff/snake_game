import os
import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
BASE_DELAY = 120
SPEED_INCREMENT = 3
MIN_DELAY = 40
HIGH_SCORE_FILE = "highscore.txt"

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(
            self.master,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="#111111",
        )
        self.canvas.pack()

        self.score_label = tk.Label(
            self.master,
            text="Score: 0 | High Score: 0",
            font=("Consolas", 14),
            fg="#ffffff",
            bg="#111111",
        )
        self.score_label.pack(pady=4)

        self.status_label = tk.Label(
            self.master,
            text="Press Space to Start",
            font=("Consolas", 12),
            fg="#cccccc",
            bg="#111111",
        )
        self.status_label.pack(pady=2)

        self.master.bind("<Up>", lambda event: self.change_direction("Up"))
        self.master.bind("<Down>", lambda event: self.change_direction("Down"))
        self.master.bind("<Left>", lambda event: self.change_direction("Left"))
        self.master.bind("<Right>", lambda event: self.change_direction("Right"))
        self.master.bind("p", lambda event: self.toggle_pause())
        self.master.bind("r", lambda event: self.restart())
        self.master.bind("<space>", lambda event: self.start_or_restart())

        self.high_score = self.load_high_score()
        self.reset_game(starting=True)
        self.update()

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as handle:
                    return int(handle.read().strip() or 0)
            except ValueError:
                return 0
        return 0

    def save_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as handle:
                handle.write(str(self.high_score))
        except OSError:
            pass

    def reset_game(self, starting=False):
        self.direction = "Right"
        self.next_direction = "Right"
        self.snake = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
        ]
        self.score = 0
        self.apples = set()
        self.paused = False
        self.game_over = False
        self.spawn_apple()
        if starting:
            self.status = "Press Space to Start"
        else:
            self.status = "Playing"
        self.update_score_labels()
        self.draw()

    def start_or_restart(self):
        if self.game_over:
            self.reset_game()
            self.game_over = False
            self.status = "Playing"
            self.update_score_labels()
        elif self.status == "Press Space to Start":
            self.status = "Playing"
            self.update_score_labels()

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
        if self.game_over or self.paused or self.status == "Press Space to Start":
            return
        opposite = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left",
        }
        if new_direction != opposite.get(self.direction):
            self.next_direction = new_direction

    def toggle_pause(self):
        if self.game_over or self.status == "Press Space to Start":
            return
        self.paused = not self.paused
        self.status = "Paused" if self.paused else "Playing"
        self.update_score_labels()

    def get_delay(self):
        return max(MIN_DELAY, BASE_DELAY - self.score * SPEED_INCREMENT)

    def is_collision(self, position):
        x, y = position
        return (
            x < 0
            or x >= GRID_WIDTH
            or y < 0
            or y >= GRID_HEIGHT
            or position in self.snake
        )

    def update(self):
        if self.game_over or self.status == "Press Space to Start":
            self.master.after(self.get_delay(), self.update)
            return

        if not self.paused:
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
            if self.is_collision(new_head):
                self.end_game()
            else:
                self.snake.insert(0, new_head)
                if new_head in self.apples:
                    self.apples.remove(new_head)
                    self.score += 1
                    if self.score > self.high_score:
                        self.high_score = self.score
                    self.spawn_apple()
                else:
                    self.snake.pop()
                self.draw()
                self.update_score_labels()

        self.master.after(self.get_delay(), self.update)

    def update_score_labels(self):
        self.score_label.config(
            text=f"Score: {self.score} | High Score: {self.high_score}"
        )
        self.status_label.config(text=self.status)

    def draw(self):
        self.canvas.delete("all")

        for x, y in self.apples:
            self.draw_cell(x, y, "#ff5555")

        for index, (x, y) in enumerate(self.snake):
            color = "#53d769" if index == 0 else "#66ff88"
            self.draw_cell(x, y, color)

        if self.game_over:
            self.status = "Game Over - Press Space to Restart"
            self.update_score_labels()
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE / 2,
                GRID_HEIGHT * CELL_SIZE / 2,
                text="Game Over\nPress Space to Restart",
                fill="#ffffff",
                font=("Consolas", 24, "bold"),
                justify="center",
            )

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(
            x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill=color, outline="#111111"
        )

    def end_game(self):
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.draw()

    def restart(self):
        if self.game_over:
            self.reset_game()
            self.game_over = False
            self.status = "Playing"
            self.update_score_labels()


def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
