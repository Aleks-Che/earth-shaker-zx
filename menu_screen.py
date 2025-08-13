import pygame
import math

class MenuScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Настройки меню
        self.font = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 72)
        
        # Пункты меню
        self.menu_items = [
            "Новая игра",
            "Выбор уровня",
            "Настройки",
            "Выход"
        ]
        
        self.selected_item = 0
        
        # Анимация заголовка
        self.title_animation_timer = 0.0
        
    def handle_event(self, event):
        """Обработка событий главного меню"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.activate_menu_item()
            elif event.key == pygame.K_ESCAPE:
                return "QUIT"
        
        return None
    
    def activate_menu_item(self):
        """Активация выбранного пункта меню"""
        item_name = self.menu_items[self.selected_item]
        
        if item_name == "Новая игра":
            return "START_GAME"
        elif item_name == "Выбор уровня":
            return "SELECT_LEVEL"
        elif item_name == "Настройки":
            return "SETTINGS"
        elif item_name == "Выход":
            return "QUIT"
        
        return None
    
    def update(self, dt, input_handler):
        """Обновление главного меню"""
        self.title_animation_timer += dt
    
    def render(self, screen):
        """Отрисовка главного меню"""
        # Заливаем фон
        screen.fill((0, 0, 0))
        
        # Анимированный заголовок
        title_offset = math.sin(self.title_animation_timer * 2) * 10
        title_color_r = int(128 + 127 * math.sin(self.title_animation_timer))
        title_color_g = int(128 + 127 * math.sin(self.title_animation_timer + 2))
        title_color_b = int(128 + 127 * math.sin(self.title_animation_timer + 4))
        
        title = self.font_large.render("EARTHSHAKER", True, (title_color_r, title_color_g, title_color_b))
        title_rect = title.get_rect(center=(self.width // 2, 150 + title_offset))
        screen.blit(title, title_rect)
        
        # Подзаголовок
        subtitle = pygame.font.Font(None, 36).render("ZX Spectrum Remake", True, (128, 128, 128))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 200))
        screen.blit(subtitle, subtitle_rect)
        
        # Пункты меню
        start_y = 300
        for i, item in enumerate(self.menu_items):
            # Цвет пункта меню
            if i == self.selected_item:
                color = (255, 255, 0)  # Желтый для выбранного
                # Добавляем стрелку
                arrow = self.font.render(">", True, color)
                arrow_rect = arrow.get_rect(center=(self.width // 2 - 150, start_y + i * 60))
                screen.blit(arrow, arrow_rect)
            else:
                color = (255, 255, 255)  # Белый для остальных
            
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(self.width // 2, start_y + i * 60))
            screen.blit(text, text_rect)
        
        # Подсказки управления
        controls = [
            "↑↓ - Навигация",
            "ENTER - Выбрать",
            "ESC - Выход"
        ]
        
        control_start_y = self.height - 100
        for i, control in enumerate(controls):
            control_surface = pygame.font.Font(None, 24).render(control, True, (128, 128, 128))
            control_rect = control_surface.get_rect(center=(self.width // 2, control_start_y + i * 25))
            screen.blit(control_surface, control_rect)
