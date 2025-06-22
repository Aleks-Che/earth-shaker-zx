import pygame
import math

class MenuScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        
        # Пункты меню
        self.menu_items = ['Start Game', 'Select Level', 'Settings', 'Quit']
        self.selected_item = 0
        
        # Анимация
        self.title_pulse = 0
        self.pulse_speed = 2
        
    def handle_event(self, event):
        """Обработка событий меню"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.get_selected_action()
            elif event.key == pygame.K_ESCAPE:
                return "QUIT"
        
        return None
    
    def get_selected_action(self):
        """Получение действия для выбранного пункта"""
        if self.selected_item == 0:
            return "START_GAME"
        elif self.selected_item == 1:
            return "SELECT_LEVEL"
        elif self.selected_item == 2:
            return "SETTINGS"
        elif self.selected_item == 3:
            return "QUIT"
        return None
    
    def update(self, dt, input_handler):
        """Обновление меню"""
        # Анимация пульсации заголовка
        self.title_pulse += dt * self.pulse_speed
    
    def render(self, screen):
        """Отрисовка меню"""
        # Градиентный фон
        self.draw_gradient_background(screen)
        
        # Заголовок с пульсацией
        pulse_scale = 1.0 + 0.1 * abs(math.cos(self.title_pulse))
        title_color = (255, 255, int(200 + 55 * abs(math.sin(self.title_pulse))))
        
        title = self.font_large.render("EARTHSHAKER", True, title_color)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        screen.blit(title, title_rect)
        
        # Подзаголовок
        subtitle = self.font_small.render("ZX80 Game Remake", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 190))
        screen.blit(subtitle, subtitle_rect)
        
        # Пункты меню
        start_y = 280
        spacing = 60
        
        for i, item in enumerate(self.menu_items):
            # Цвет и эффекты для выбранного пункта
            if i == self.selected_item:
                color = (255, 255, 0)
                # Добавляем небольшое свечение
                glow_surface = self.font_medium.render(item, True, (100, 100, 0))
                for dx in [-2, -1, 1, 2]:
                    for dy in [-2, -1, 1, 2]:
                        glow_rect = glow_surface.get_rect(center=(self.width // 2 + dx, start_y + i * spacing + dy))
                        screen.blit(glow_surface, glow_rect)
            else:
                color = (255, 255, 255)
            
            # Основной текст
            text_surface = self.font_medium.render(item, True, color)
            text_rect = text_surface.get_rect(center=(self.width // 2, start_y + i * spacing))
            screen.blit(text_surface, text_rect)
            
            # Стрелка для выбранного пункта
            if i == self.selected_item:
                arrow_x = text_rect.left - 40
                arrow_y = text_rect.centery
                pygame.draw.polygon(screen, (255, 255, 0), [
                    (arrow_x, arrow_y),
                    (arrow_x - 15, arrow_y - 10),
                    (arrow_x - 15, arrow_y + 10)
                ])
        
        # Подсказки управления
        controls = [
            "↑↓ - Navigate",
            "ENTER - Select",
            "ESC - Quit"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (150, 150, 150))
            screen.blit(text, (20, self.height - 80 + i * 20))
        
        # Информация об игре
        info_text = "Collect crystals and avoid enemies!"
        info_surface = self.font_small.render(info_text, True, (180, 180, 180))
        info_rect = info_surface.get_rect(center=(self.width // 2, self.height - 40))
        screen.blit(info_surface, info_rect)
    
    def draw_gradient_background(self, screen):
        """Отрисовка градиентного фона"""
        # Простой градиент от темно-синего к черному
        for y in range(self.height):
            ratio = y / self.height
            color_value = int(40 * (1 - ratio))
            color = (0, 0, color_value)
            pygame.draw.line(screen, color, (0, y), (self.width, y))
