import pygame

class LevelSelectScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Настройки меню
        self.font = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 64)
        
        # Доступные уровни
        self.max_levels = 4
        self.levels_per_row = 4
        self.selected_level = 1
        
    def handle_event(self, event):
        """Обработка событий экрана выбора уровня"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.selected_level > 1:
                    self.selected_level -= 1
            elif event.key == pygame.K_RIGHT:
                if self.selected_level < self.max_levels:
                    self.selected_level += 1
            elif event.key == pygame.K_UP:
                if self.selected_level > self.levels_per_row:
                    self.selected_level -= self.levels_per_row
            elif event.key == pygame.K_DOWN:
                if self.selected_level + self.levels_per_row <= self.max_levels:
                    self.selected_level += self.levels_per_row
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return f"START_LEVEL_{self.selected_level}"
            elif event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"
        
        return None
    
    def update(self, dt, input_handler):
        """Обновление экрана выбора уровня"""
        pass
    
    def render(self, screen):
        """Отрисовка экрана выбора уровня"""
        # Заливаем фон
        screen.fill((0, 0, 0))
        
        # Заголовок
        title = self.font_large.render("ВЫБОР УРОВНЯ", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        screen.blit(title, title_rect)
        
        # Сетка уровней
        start_x = self.width // 2 - (self.levels_per_row * 100) // 2
        start_y = 200
        
        for level in range(1, self.max_levels + 1):
            row = (level - 1) // self.levels_per_row
            col = (level - 1) % self.levels_per_row
            
            x = start_x + col * 120
            y = start_y + row * 120
            
            # Цвет уровня
            if level == self.selected_level:
                color = (255, 255, 0)  # Желтый для выбранного
                border_color = (255, 255, 255)
            else:
                color = (255, 255, 255)  # Белый для остальных
                border_color = (128, 128, 128)
            
            # Рамка уровня
            pygame.draw.rect(screen, border_color, (x - 50, y - 50, 100, 100), 3)
            
            # Номер уровня
            level_text = self.font.render(str(level), True, color)
            level_rect = level_text.get_rect(center=(x, y))
            screen.blit(level_text, level_rect)
        
        # Подсказки управления
        controls = [
            "Стрелки - Навигация",
            "ENTER - Выбрать уровень",
            "ESC - Назад"
        ]
        
        control_start_y = self.height - 120
        for i, control in enumerate(controls):
            control_surface = pygame.font.Font(None, 24).render(control, True, (128, 128, 128))
            control_rect = control_surface.get_rect(center=(self.width // 2, control_start_y + i * 25))
            screen.blit(control_surface, control_rect)
