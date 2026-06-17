import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS_START = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Adventure")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 100, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 220)


class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
        self.grow_next = False
# Move the snake in the current direction.
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

        if self.grow_next:
            self.grow_next = False
        else:
            self.body.pop()
#Increase the snake length after eating food.
    def grow(self):
        self.grow_next = True
#Prevent the snake from reversing direction.
    def change_direction(self, new_direction):
        dx, dy = self.direction
        ndx, ndy = new_direction
        if (dx + ndx, dy + ndy) != (0, 0):
            self.direction = new_direction
#Draw the snake on the screen
    def draw(self):
        for index, segment in enumerate(self.body):
            color = DARK_GREEN if index == 0 else GREEN
            pygame.draw.rect(screen, color, (*segment, CELL_SIZE, CELL_SIZE))
#Check if the snake has hit the wall or itself.
    def hit_wall(self):
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT

    def hit_self(self):
        return self.body[0] in self.body[1:]


class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)
#Generate a random position for the food that is not occupied by the snake.
    def random_position(self, snake_body):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            if (x, y) not in snake_body:
                return (x, y)
#Respawn the food at a new random position after being eaten.
    def respawn(self, snake_body):
        self.position = self.random_position(snake_body)
#Draw the food on the screen.
    def draw(self):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))


class Game:
    def __init__(self):
        self.high_score = 0
        self.start_new_game()
        self.started = False
#Start a new game by initializing the snake, food, score, level, speed, and game over state.
    def start_new_game(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.level = 1
        self.speed = FPS_START
        self.game_over = False
#Reset the game to the initial state when the player chooses to restart after a game over.
    def reset(self):
        self.start_new_game()
#Handle user input for starting the game, changing the snake's direction, and restarting after a game over.
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.started and event.key == pygame.K_SPACE:
                self.started = True

            if event.key in (pygame.K_UP, pygame.K_w):
                self.snake.change_direction((0, -CELL_SIZE))
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.snake.change_direction((0, CELL_SIZE))
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.snake.change_direction((-CELL_SIZE, 0))
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.snake.change_direction((CELL_SIZE, 0))
            elif event.key == pygame.K_r and self.game_over:
                self.reset()
#Update the game state by moving the snake, checking for food collisions, updating the score and level, and checking for game over conditions.
    def update(self):
        if not self.started or self.game_over:
            return

        self.snake.move()

        if self.snake.body[0] == self.food.position:
            self.score += 1

            if self.score > self.high_score:
                self.high_score = self.score

            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.update_level()

        if self.snake.hit_wall() or self.snake.hit_self():
            self.game_over = True
#Update the game level and speed based on the current score. The level increases every 5 points, and the speed increases by 2 FPS for each new level.
    def update_level(self):
        self.level = 1 + self.score // 5
        self.speed = FPS_START + (self.level - 1) * 2
#Draw text on the screen at the specified position with the given font and color.
    def draw_text(self, text, font_obj, color, x, y):
        surface = font_obj.render(text, True, color)
        screen.blit(surface, (x, y))

    def draw_start_screen(self):
        screen.fill(BLACK)
        self.draw_text("SNAKE ADVENTURE", big_font, GREEN, WIDTH // 2 - 210, 130)
        self.draw_text("WASD or Arrow Keys to Move", font, WHITE, WIDTH // 2 - 180, 230)
        self.draw_text("Eat food to increase your score", font, WHITE, WIDTH // 2 - 190, 270)
        self.draw_text("Every 5 points = New Level", font, WHITE, WIDTH // 2 - 165, 310)
        self.draw_text("Press SPACE to Start", font, BLUE, WIDTH // 2 - 130, 380)
        pygame.display.flip()

    def draw_hud(self):
        self.draw_text(f"Score: {self.score}", font, WHITE, 10, 10)
        self.draw_text(f"Level: {self.level}", font, WHITE, 10, 45)
        self.draw_text(f"Speed: {self.speed}", font, WHITE, 10, 80)
        self.draw_text(f"High Score: {self.high_score}", font, WHITE, 10, 115)
#Draw the game over screen with a semi-transparent overlay and display the final score, high score, and instructions to restart.
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        self.draw_text("GAME OVER", big_font, RED, WIDTH // 2 - 140, HEIGHT // 2 - 90)
        self.draw_text(f"Final Score: {self.score}", font, WHITE, WIDTH // 2 - 90, HEIGHT // 2 - 25)
        self.draw_text(f"High Score: {self.high_score}", font, WHITE, WIDTH // 2 - 95, HEIGHT // 2 + 15)
        self.draw_text("Press R to Restart", font, BLUE, WIDTH // 2 - 110, HEIGHT // 2 + 60)
#Draw the current game state, including the start screen, game elements (snake and food), HUD, and game over screen if applicable.
    def draw(self):
        if not self.started:
            self.draw_start_screen()
            return

        screen.fill(BLACK)
        self.food.draw()
        self.snake.draw()
        self.draw_hud()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

#The main function initializes the game and runs the main game loop, which handles events, updates the game state, and draws the game elements on the screen until the player quits.
def main():
    game = Game()
    running = True

    while running:
        clock.tick(game.speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_input(event)

        game.update()
        game.draw()

    pygame.quit()


if __name__ == "__main__":
    main()