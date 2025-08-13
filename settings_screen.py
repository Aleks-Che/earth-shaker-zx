import pygame

class SettingsScreen:
    def __init__(self, width, height, sound_manager, game_settings):
        self.width = width
        self.height = height
        self.sound_manager = sound_manager
        self.game_settings = game_settings
        
        # Настройки меню
        self.font = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 64)
        
        # Пункты настроек
        self.settings_items = [
            "Плавное движение",
            "Громкость звуков",
            "Громкость музыки",
            "Тема спрайтов",
            "Назад"
        ]
        
        self.selected_item = 0
        
    def handle_event(self, event):
        """Обработка событий экрана настроек"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.settings_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.settings_items)
            elif event.key == pygame.K_LEFT:
                self.adjust_setting(-1)
            elif event.key == pygame.K_RIGHT:
                self.adjust_setting(1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.activate_setting()
            elif event.key == pygame.K_ESCAPE:
                return "MAIN_MENU"
        
        return None
    
    def adjust_setting(self, direction):
        """Изменение значения настройки"""
        setting_name = self.settings_items[self.selected_item]
        
        if setting_name == "Плавное движение":
            self.game_settings.toggle_smooth_movement()
        elif setting_name == "Громкость звуков":
            new_volume = self.game_settings.sound_volume + direction * 0.1
            self.game_settings.set_sound_volume(new_volume)
            self.sound_manager.set_sound_volume(self.game_settings.sound_volume)
        elif setting_name == "Громкость музыки":
            new_volume = self.game_settings.music_volume + direction * 0.1
            self.game_settings.set_music_volume(new_volume)
            self.sound_manager.set_music_volume(self.game_settings.music_volume)
        elif setting_name == "Тема спрайтов":
            self.cycle_sprite_theme()
    
    def activate_setting(self):
        """Активация настройки"""
        setting_name = self.settings_items[self.selected_item]
        
        if setting_name == "Плавное движение":
            self.game_settings.toggle_smooth_movement()
        elif setting_name == "Тема спрайтов":
            self.cycle_sprite_theme()
        elif setting_name == "Назад":
            return "MAIN_MENU"
        
        return None
    
    def cycle_sprite_theme(self):
        """Переключение на следующую тему спрайтов"""
        next_theme = self.game_settings.get_next_sprite_theme()
        self.game_settings.set_sprite_theme(next_theme)
        print(f"Переключена тема спрайтов на: {self.game_settings.get_sprite_theme_name()}")
    
    def get_setting_value_text(self, setting_name):
        """Получение текста значения настройки"""
        if setting_name == "Плавное движение":
            return "Вкл" if self.game_settings.smooth_movement else "Выкл"
        elif setting_name == "Громкость звуков":
            return f"{int(self.game_settings.sound_volume * 100)}%"
        elif setting_name == "Громкость музыки":
            return f"{int(self.game_settings.music_volume * 100)}%"
        elif setting_name == "Тема спрайтов":
            return self.game_settings.get_sprite_theme_name()
        
        return ""
    
    def update(self, dt, input_handler):
        """Обновление экрана настроек"""
        pass
    
    def render(self, screen):
        """Отрисовка экрана настроек"""
        # Заливаем фон
        screen.fill((0, 0, 0))
        
        # Заголовок
        title = self.font_large.render("НАСТРОЙКИ", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        screen.blit(title, title_rect)
        
        # Пункты настроек
        start_y = 200
        for i, item in enumerate(self.settings_items):
            # Цвет пункта меню
            if i == self.selected_item:
                color = (255, 255, 0)  # Желтый для выбранного
                # Добавляем стрелку
                arrow = self.font.render(">", True, color)
                arrow_rect = arrow.get_rect(center=(100, start_y + i * 60))
                screen.blit(arrow, arrow_rect)
            else:
                color = (255, 255, 255)  # Белый для остальных
            
            # Название настройки
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(300, start_y + i * 60))
            screen.blit(text, text_rect)
            
            # Значение настройки (кроме "Назад")
            if item != "Назад":
                value_text = self.get_setting_value_text(item)
                if value_text:
                    value_surface = self.font.render(value_text, True, color)
                    value_rect = value_surface.get_rect(center=(500, start_y + i * 60))
                    screen.blit(value_surface, value_rect)
        
        # Подсказки управления
        controls = [
            "↑↓ - Навигация",
            "←→ - Изменить значение",
            "ENTER - Переключить",
            "ESC - Назад"
        ]
        
        control_start_y = self.height - 120
        for i, control in enumerate(controls):
            control_surface = pygame.font.Font(None, 24).render(control, True, (128, 128, 128))
            control_rect = control_surface.get_rect(center=(self.width // 2, control_start_y + i * 25))
            screen.blit(control_surface, control_rect)
