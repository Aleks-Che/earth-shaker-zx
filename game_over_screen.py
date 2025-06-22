import pygame

class GameOverScreen:
    def __init__(self, width, height, score, crystals_collected):
        self.width = width
        self.height = height
        self.score = score
        self.crystals_collected = crystals_collected
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Анимация
        self.fade_alpha = 0
        self.fade_speed = 200
        self.show_text = False
        
        # Пункты меню
        self.menu_items = ['Play Again', 'Main Menu']
        self.selected_item = 0
        
    def handle_event(self, event):
        """Обработка событий"""
        if not self.show_text:
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_item == 0:
                    return "START_GAME"
                else:
                    return "MAIN_MENU"
            elif event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"
        
        return None
    
    def update(self, dt, input_handler):
        """Обновление экрана"""
        # Анимация появления
        if self.fade_alpha < 255:
            self.fade_alpha += self.fade_speed * dt
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.show_text = True
    
    def render(self, screen):
        """Отрисовка экрана завершения игры"""
        # Полупрозрачный черный фон
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(min(200, self.fade_alpha))
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        if not self.show_text:
            return
        
        # Заголовок
        title = self.font_large.render("GAME OVER", True, (255, 100, 100))
        title_rect = title.get_rect(center=(self.width // 2, 150))
        screen.blit(title, title_rect)
        
        # Статистика
        stats = [
            f"Crystals Collected: {self.crystals_collected}",
            f"Final Score: {self.score}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font_small.render(stat, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width // 2, 220 + i * 40))
            screen.blit(text, text_rect)
        
        # Пункты меню
        start_y = 320
        spacing = 60
        
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected_item else (255, 255, 255)
            text_surface = self.font_medium.render(item, True, color)
            text_rect = text_surface.get_rect(center=(self.width // 2, start_y + i * spacing))
            screen.blit(text_surface, text_rect)
            
            # Рамка для выбранного пункта
            if i == self.selected_item:
                pygame.draw.rect(screen, (255, 255, 0), 
                               (text_rect.left - 10, text_rect.top - 5, 
                                text_rect.width + 20, text_rect.height + 10), 2)
        
        # Подсказки
        controls = ["↑↓ - Navigate", "ENTER - Select", "ESC - Main Menu"]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (200, 200, 200))
            screen.blit(text, (20, self.height - 80 + i * 20))