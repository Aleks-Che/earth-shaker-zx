import pygame
import sys
import os
from game import Game
from setup_assets import create_assets_folder

def main():
    # Создаем папку assets если её нет
    create_assets_folder()
    
    # Инициализация pygame
    pygame.init()
    
    # Настройки экрана
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EarthShaker - ZX80 Game")
    clock = pygame.time.Clock()
    
    # Создаем игру
    game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Основной игровой цикл
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Время в секундах
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Передаем события в игру
                result = game.handle_event(event)
                if result == "QUIT":
                    running = False
        
        # Обновление игры
        game.update(dt)
        
        # Отрисовка
        game.render()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()