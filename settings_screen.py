import pygame

class SettingsScreen:
    def __init__(self, width, height, sound_manager, game_settings):
        self.width = width
        self.height = height
        self.sound_manager = sound_manager
        self.game_settings = game_settings
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Выбранный элемент меню
        self.selected_item = 0
        self.menu_items = ['Sound Volume', 'Music Volume', 'Movement Mode', 'Back']
        
    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_LEFT:
                self.adjust_setting(-0.1)
            elif event.key == pygame.K_RIGHT:
                self.adjust_setting(0.1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_item == 2:  # Movement Mode
                    self.game_settings.toggle_smooth_movement()
                elif self.selected_item == len(self.menu_items) - 1:  # Back
                    return "MAIN_MENU"
            elif event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"
        
        return None
    
    def adjust_setting(self, delta):
        """Изменение настройки"""
        if self.selected_item == 0:  # Sound Volume
            new_volume = max(0.0, min(1.0, self.sound_manager.sound_volume + delta))
            if self.sound_manager:
                self.sound_manager.set_sound_volume(new_volume)
        elif self.selected_item == 1:  # Music Volume
            new_volume = max(0.0, min(1.0, self.sound_manager.music_volume + delta))
            if self.sound_manager:
                self.sound_manager.set_music_volume(new_volume)
        elif self.selected_item == 2:  # Movement Mode
            self.game_settings.toggle_smooth_movement()
    
    def update(self, dt, input_handler):
        """Обновление экрана настроек"""
        pass
    
    def render(self, screen):
        """Отрисовка экрана настроек"""
        # Заливка фона
        screen.fill((20, 20, 40))
        
        # Заголовок
        title = self.font_large.render("SETTINGS", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        screen.blit(title, title_rect)
        
        # Пункты меню
        start_y = 200
        spacing = 80
        
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected_item else (255, 255, 255)
            
            if item == 'Sound Volume':
                text = f"Sound Volume: {int(self.sound_manager.sound_volume * 100)}%"
            elif item == 'Music Volume':
                text = f"Music Volume: {int(self.sound_manager.music_volume * 100)}%"
            elif item == 'Movement Mode':
                mode = "Smooth" if self.game_settings.smooth_movement else "Grid"
                text = f"Movement: {mode}"
            else:
                text = item
            
            text_surface = self.font_medium.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.width // 2, start_y + i * spacing))
            screen.blit(text_surface, text_rect)
            
            # Индикатор выбора
            if i == self.selected_item:
                pygame.draw.rect(screen, (255, 255, 0), 
                               (text_rect.left - 10, text_rect.top - 5, 
                                text_rect.width + 20, text_rect.height + 10), 2)
        
        # Подсказки управления
        controls = [
            "↑↓ - Navigate",
            "←→ - Adjust / Toggle",
            "ENTER - Select",
            "ESC - Back"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (200, 200, 200))
            screen.blit(text, (20, self.height - 100 + i * 20))
