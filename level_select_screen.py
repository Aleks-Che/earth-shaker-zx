import pygame

class LevelSelectScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Уровни
        self.max_levels = 4
        self.selected_level = 1
        
    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_level = max(1, self.selected_level - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_level = min(self.max_levels, self.selected_level + 1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return f"START_LEVEL_{self.selected_level}"
            elif event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"
        
        return None
    
    def update(self, dt, input_handler):
        """Обновление экрана"""
        pass
    
    def render(self, screen):
        """Отрисовка экрана выбора уровня"""
        # Заливка фона
        screen.fill((20, 20, 40))
        
        # Заголовок
        title = self.font_large.render("SELECT LEVEL", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        screen.blit(title, title_rect)
        
        # Уровни
        start_x = self.width // 2 - (self.max_levels * 80) // 2
        start_y = 250
        
        for i in range(1, self.max_levels + 1):
            x = start_x + (i - 1) * 80
            y = start_y
            
            # Цвет в зависимости от выбора
            if i == self.selected_level:
                color = (255, 255, 0)
                # Рамка
                pygame.draw.rect(screen, color, (x - 5, y - 5, 70, 70), 3)
            else:
                color = (255, 255, 255)
            
            # Квадрат уровня
            pygame.draw.rect(screen, (100, 100, 100), (x, y, 60, 60))
            pygame.draw.rect(screen, color, (x, y, 60, 60), 2)
            
            # Номер уровня
            level_text = self.font_medium.render(str(i), True, color)
            level_rect = level_text.get_rect(center=(x + 30, y + 30))
            screen.blit(level_text, level_rect)
        
        # Подсказки
        controls = [
            "←→ - Select Level",
            "ENTER - Start Level",
            "ESC - Back to Menu"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (200, 200, 200))
            text_rect = text.get_rect(center=(self.width // 2, 400 + i * 25))
            screen.blit(text, text_rect)
