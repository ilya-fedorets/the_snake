import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Изгиб Питона")

# Частота обновления экрана
clock = pygame.time.Clock()
FPS = 20

class GameObject:
    """Базовый класс для всех игровых объектов."""
    
    def __init__(self, position=(0, 0), color=WHITE):
        """Инициализация объекта с позицией и цветом."""
        self.position = position
        self.color = color
    
    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass

class Apple(GameObject):
    """Класс для яблока."""
    
    def __init__(self):
        """Инициализация яблока с красным цветом и случайной позицией."""
        super().__init__(color=RED)
        self.randomize_position()
    
    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        )
    
    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, self.color, rect)

class Snake(GameObject):
    """Класс для змейки."""
    
    def __init__(self):
        """Инициализация змейки с начальной позицией и зелёным цветом."""
        super().__init__(color=GREEN)
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = None
    
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        """Двигает змейку в текущем направлении."""
        current_head = self.positions[0]
        new_head = (
            (current_head[0] + self.direction[0] * CELL_SIZE) % WIDTH,
            (current_head[1] + self.direction[1] * CELL_SIZE) % HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, self.color, rect)
    
    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = None

def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.next_direction = (1, 0)

def main():
    """Основной игровой цикл."""
    snake = Snake()
    apple = Apple()
    
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        
        screen.fill(BLACK)
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()