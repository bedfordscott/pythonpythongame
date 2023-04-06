import tkinter as tk
import random

# Set up the game board
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20

# Set up the initial snake
SNAKE_LENGTH = 3
SNAKE_COLOR = 'green'
SNAKE_START_X = 5
SNAKE_START_Y = 5

# Set up the food
FOOD_COLOR = 'red'

# Set up the game speed (milliseconds per frame)
GAME_SPEED = 110

class SnakeGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Snake Game")
        self.pack()
        self.create_widgets()
        self.bind_keys()
        self.init_game()
        self.after(GAME_SPEED, self.game_loop)

    def create_widgets(self):
        # Create the canvas
        self.canvas = tk.Canvas(self, width=GRID_WIDTH*CELL_SIZE, height=GRID_HEIGHT*CELL_SIZE)
        self.canvas.pack()

        # Create the score label
        self.score_label = tk.Label(self, text="Score: 0")
        self.score_label.pack()

    def bind_keys(self):
        # Bind the arrow keys to the corresponding movement functions
        self.master.bind('<Left>', lambda event: self.change_direction(-1, 0))
        self.master.bind('<Right>', lambda event: self.change_direction(1, 0))
        self.master.bind('<Up>', lambda event: self.change_direction(0, -1))
        self.master.bind('<Down>', lambda event: self.change_direction(0, 1))

    def init_game(self):
        # Initialize the snake
        self.snake = [[SNAKE_START_X, SNAKE_START_Y]]
        for i in range(1, SNAKE_LENGTH):
            self.snake.append([SNAKE_START_X - i, SNAKE_START_Y])
        self.direction = [1, 0]

        # Add the food
        self.add_food()

        # Initialize the score
        self.score = 0

    def add_food(self):
        # Add a new food to a random location on the board
        x = random.randint(0, GRID_WIDTH-1)
        y = random.randint(0, GRID_HEIGHT-1)
        self.food = [x, y]

    def game_loop(self):
        # Move the snake
        self.move_snake()

        # Check for collisions
        if self.check_collisions():
            self.game_over()
            return

        # Check if the snake has eaten the food
        if self.snake[0] == self.food:
            self.score += 1
            self.score_label.config(text="Score: " + str(self.score))
            self.add_food()
            self.snake.append(self.snake[-1])

        # Redraw the board
        self.draw_board()

        # Schedule the next frame
        self.after(GAME_SPEED, self.game_loop)

    def move_snake(self):
        # Move the snake in the current direction
        new_head = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]
        self.snake.insert(0, new_head)
        self.snake.pop()

    def check_collisions(self):
    # Check for collisions with the walls
        if self.snake[0][0] < 0 or self.snake[0][0] >= GRID_WIDTH or self.snake[0][1] < 0 or self.snake[0][1] >= GRID_HEIGHT:
            return True

    # Check for collisions with the snake's body
        for i in range(1, len(self.snake)):
            if self.snake[0] == self.snake[i]:
                return True

    # No collisions
        return False
        
    def game_over(self):
        # Stop the game loop and display a game over message
        self.after_cancel(self.game_loop_id)
        self.canvas.create_text(GRID_WIDTH*CELL_SIZE/2, GRID_HEIGHT*CELL_SIZE/2, text="Game Over", font=("Helvetica", 24))

    def change_direction(self, dx, dy):
        # Change the direction of the snake
        if (dx, dy) != tuple(map(lambda x: -x, self.direction)) and (dx, dy) != tuple(self.direction):
            self.direction = [dx, dy]

    def draw_board(self):
        # Clear the canvas
        self.canvas.delete(tk.ALL)

        # Draw the food
        self.canvas.create_rectangle(self.food[0]*CELL_SIZE, self.food[1]*CELL_SIZE, (self.food[0]+1)*CELL_SIZE, (self.food[1]+1)*CELL_SIZE, fill=FOOD_COLOR)

        # Draw the snake
        for i in range(len(self.snake)):
            self.canvas.create_rectangle(self.snake[i][0]*CELL_SIZE, self.snake[i][1]*CELL_SIZE, (self.snake[i][0]+1)*CELL_SIZE, (self.snake[i][1]+1)*CELL_SIZE, fill=SNAKE_COLOR)

    def start_game(self):
        # Start the game loop
        self.game_loop_id = self.after(GAME_SPEED, self.game_loop)

# Create the game window and start the game
root = tk.Tk()
game = SnakeGame(root)
game.start_game()
game.mainloop()
