import pygame

class GameOverScreen:
    def __init__(self, width, height, victory=False, level_number=1, crystals_collected=0):
        self.width = width
        self.height = height
        self.victory = victory
        self.level_number = level_number
        self.crystals_collected = crystals_collected
        
        # Настройки
        self.font = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 72)
        
        # Пункты меню
        if victory:
            self.menu_items = [
                "Следующий уровень",
                "Главное меню",
                "Выход"
            ]
        else:
            self.menu_items = [
                "Повторить уровень",
                "Главное меню",
                "Выход"
            ]
        
        self.selected_item = 0
        
        # Анимация
        self.animation_timer = 0.0
        
    def handle_event(self, event):
        """Обработка событий экрана завершения игры"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.activate_menu_item()
            elif event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"
        
        return None
    
    def activate_menu_item(self):
        """Активация выбранного пункта меню"""
        item_name = self.menu_items[self.selected_item]
        
        if item_name == "Следующий уровень":
            return f"START_LEVEL_{self.level_number + 1}"
        elif item_name == "Повторить уровень":
            return f"START_LEVEL_{self.level_number}"
        elif item_name == "Главное меню":
            return "MAIN_MENU"
        elif item_name == "Выход":
            return "QUIT"
        
        return None
    
    def update(self, dt, input_handler):
        """Обновление экрана завершения игры"""
        self.animation_timer += dt
    
    def render(self, screen):
        """Отрисовка экрана завершения игры"""
        # Заливаем фон
        screen.fill((0, 0, 0))
        
        # Заголовок
        if self.victory:
            title_text = "УРОВЕНЬ ПРОЙДЕН!"
            title_color = (0, 255, 0)  # Зеленый для победы
        else:
            title_text = "ИГРА ОКОНЧЕНА"
            title_color = (255, 0, 0)  # Красный для поражения
        
        title = self.font_large.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        screen.blit(title, title_rect)
        
        # Статистика
        stats = [
            f"Уровень: {self.level_number}",
            f"Кристаллов собрано: {self.crystals_collected}"
        ]
        
        for i, stat in enumerate(stats):
            stat_surface = pygame.font.Font(None, 36).render(stat, True, (255, 255, 255))
            stat_rect = stat_surface.get_rect(center=(self.width // 2, 220 + i * 40))
            screen.blit(stat_surface, stat_rect)
        
        # Пункты меню
        start_y = 350
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
            "ESC - Главное меню"
        ]
        
        control_start_y = self.height - 100
        for i, control in enumerate(controls):
            control_surface = pygame.font.Font(None, 24).render(control, True, (128, 128, 128))
            control_rect = control_surface.get_rect(center=(self.width // 2, control_start_y + i * 25))
            screen.blit(control_surface, control_rect)