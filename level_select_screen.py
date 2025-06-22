import pygame
from level_data import LevelData

class LevelSelectScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Доступные уровни
        self.max_levels = 4
        self.selected_level = 1
        
        # Информация об уровнях
        self.level_info = {}
        for i in range(1, self.max_levels + 1):
            level_data = LevelData.get_level(i)
            if level_data:
                self.level_info[i] = {
                    'crystals': level_data['crystals_total'],
                    'size': f"{level_data['width']}x{level_data['height']}"
                }
    
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
        """Обновление экрана выбора уровня"""
        pass
    
    def render(self, screen):
        """Отрисовка экрана выбора уровня"""
        # Заливка фона
        screen.fill((20, 20, 40))
        
        # Заголовок
        title = self.font_large.render("SELECT LEVEL", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 80))
        screen.blit(title, title_rect)
        
        # Отрисовка уровней
        levels_per_row = 2
        level_width = 200
        level_height = 150
        spacing_x = 50
        spacing_y = 30
        
        start_x = (self.width - (levels_per_row * level_width + (levels_per_row - 1) * spacing_x)) // 2
        start_y = 150
        
        for i in range(1, self.max_levels + 1):
            row = (i - 1) // levels_per_row
            col = (i - 1) % levels_per_row
            
            x = start_x + col * (level_width + spacing_x)
            y = start_y + row * (level_height + spacing_y)
            
            # Рамка уровня
            color = (255, 255, 0) if i == self.selected_level else (100, 100, 100)
            border_width = 4 if i == self.selected_level else 2
            
            pygame.draw.rect(screen, color, (x, y, level_width, level_height), border_width)
            
            # Заливка фона уровня
            bg_color = (50, 50, 80) if i == self.selected_level else (30, 30, 50)
            pygame.draw.rect(screen, bg_color, 
                           (x + border_width, y + border_width, 
                            level_width - 2 * border_width, level_height - 2 * border_width))
            
            # Номер уровня
            level_text = self.font_large.render(f"LEVEL {i}", True, (255, 255, 255))
            level_rect = level_text.get_rect(center=(x + level_width // 2, y + 40))
            screen.blit(level_text, level_rect)
            
            # Информация об уровне
            if i in self.level_info:
                info = self.level_info[i]
                
                crystals_text = f"Crystals: {info['crystals']}"
                crystals_surface = self.font_small.render(crystals_text, True, (200, 200, 200))
                crystals_rect = crystals_surface.get_rect(center=(x + level_width // 2, y + 80))
                screen.blit(crystals_surface, crystals_rect)
                
                size_text = f"Size: {info['size']}"
                size_surface = self.font_small.render(size_text, True, (200, 200, 200))
                size_rect = size_surface.get_rect(center=(x + level_width // 2, y + 100))
                screen.blit(size_surface, size_rect)
            
            # Индикатор выбора
            if i == self.selected_level:
                arrow_y = y + level_height // 2
                # Левая стрелка
                pygame.draw.polygon(screen, (255, 255, 0), [
                    (x - 20, arrow_y),
                    (x - 35, arrow_y - 10),
                    (x - 35, arrow_y + 10)
                ])
                # Правая стрелка
                pygame.draw.polygon(screen, (255, 255, 0), [
                    (x + level_width + 20, arrow_y),
                    (x + level_width + 35, arrow_y - 10),
                    (x + level_width + 35, arrow_y + 10)
                ])
        
        # Подсказки управления
        controls = [
            "←→ - Select Level",
            "ENTER - Start Level",
            "ESC - Back to Menu"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (200, 200, 200))
            screen.blit(text, (20, self.height - 80 + i * 20))
