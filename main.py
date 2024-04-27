import pygame
import sys
import random
from array import array
from math import sin, pi

# Constants
WIDTH, HEIGHT = 800, 600
SNAKE_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (255, 0, 0)

class SoundEngine:
    def __init__(self):
        pygame.mixer.init()
        self.eat_sound = self.generate_sound(523, 0.1)
        self.game_over_sound = self.generate_sound(310, 0.5)

    def generate_sound(self, frequency, duration):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array('h', (int(4096 * sin(2.0 * pi * frequency * x / sample_rate)) for x in range(n_samples)))
        return pygame.mixer.Sound(buffer=buf)

    def play_eat_sound(self):
        self.eat_sound.play()

    def play_game_over_sound(self):
        self.game_over_sound.play()

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2 - i * SNAKE_SIZE) for i in range(3)]
        self.direction = pygame.K_DOWN

    def move(self):
        direction_offsets = {
            pygame.K_RIGHT: (SNAKE_SIZE, 0),
            pygame.K_LEFT: (-SNAKE_SIZE, 0),
            pygame.K_UP: (0, -SNAKE_SIZE),
            pygame.K_DOWN: (0, SNAKE_SIZE)
        }
        x_offset, y_offset = direction_offsets[self.direction]
        new_head = (self.body[0][0] + x_offset, self.body[0][1] + y_offset)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self, item):
        return self.body[0] == item

    def check_boundaries(self):
        head = self.body[0]
        return head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.snake = Snake()
        self.food = self.spawn_food()
        self.sound_engine = SoundEngine()
        self.clock = pygame.time.Clock()

    def spawn_food(self):
        while True:
            food = (random.randrange(0, WIDTH, SNAKE_SIZE), random.randrange(0, HEIGHT, SNAKE_SIZE))
            if food not in self.snake.body:
                return food

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        self.snake.direction = event.key

            self.snake.move()
            if self.snake.check_collision(self.food):
                self.snake.grow()
                self.food = self.spawn_food()
                self.sound_engine.play_eat_sound()

            if self.snake.check_boundaries() or self.snake.body[0] in self.snake.body[1:]:
                self.sound_engine.play_game_over_sound()
                running = self.display_restart_prompt()

            self.render()

    def display_restart_prompt(self):
        self.screen.fill(BLACK)
        text = self.font.render("Game Over! Restart? (Y/N)", True, FONT_COLOR)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.restart_game()
                        return True
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()
        return False

    def restart_game(self):
        self.snake = Snake()  # Reset snake
        self.food = self.spawn_food()  # Reset food
        self.run()  # Restart the game loop

    def render(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.food[0], self.food[1], SNAKE_SIZE, SNAKE_SIZE))
        for segment in self.snake.body:  # Added colon at the end of the for loop statement
            pygame.draw.rect(self.screen, WHITE, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.display.flip()
        self.clock.tick(10)

if __name__ == "__main__":
    Game().run()
