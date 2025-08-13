import config

class GameSettings:
    """Класс для управления настройками игры"""
    
    def __init__(self):
        self.smooth_movement = True
        self.sound_volume = 0.8
        self.music_volume = 0.7
        self.sprite_theme = "original"  # Тема спрайтов
        
        # Доступные темы спрайтов
        self.available_sprite_themes = {
            "original": "Original ZX80",
            "enhanced": "Enhanced Original", 
            "modern": "Modern"
        }
        
    def toggle_smooth_movement(self):
        """Переключение плавного движения"""
        self.smooth_movement = not self.smooth_movement
        return self.smooth_movement
    
    def set_sound_volume(self, volume):
        """Установка громкости звуков"""
        self.sound_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """Установка громкости музыки"""
        self.music_volume = max(0.0, min(1.0, volume))
    
    def set_sprite_theme(self, theme):
        """Установка темы спрайтов"""
        if theme in self.available_sprite_themes:
            self.sprite_theme = theme
            self.save_settings()
            return True
        return False
    
    def get_sprite_theme_name(self):
        """Получение названия текущей темы спрайтов"""
        return self.available_sprite_themes.get(self.sprite_theme, "Неизвестная")
    
    def get_next_sprite_theme(self):
        """Получение следующей темы спрайтов для переключения"""
        themes = list(self.available_sprite_themes.keys())
        current_index = themes.index(self.sprite_theme)
        next_index = (current_index + 1) % len(themes)
        return themes[next_index]
    
    def save_settings(self):
        """Сохранение настроек в файл"""
        settings_data = {
            "smooth_movement": self.smooth_movement,
            "sound_volume": self.sound_volume,
            "music_volume": self.music_volume,
            "sprite_theme": self.sprite_theme
        }
        
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)
            print(f"Настройки сохранены в {self.settings_file}")
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def load_settings(self):
        """Загрузка настроек из файла"""
        if not os.path.exists(self.settings_file):
            print("Файл настроек не найден, используются настройки по умолчанию")
            return
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
            
            self.smooth_movement = settings_data.get("smooth_movement", self.smooth_movement)
            self.sound_volume = settings_data.get("sound_volume", self.sound_volume)
            self.music_volume = settings_data.get("music_volume", self.music_volume)
            self.sprite_theme = settings_data.get("sprite_theme", self.sprite_theme)
            
            # Проверяем, что тема спрайтов существует
            if self.sprite_theme not in self.available_sprite_themes:
                print(f"Неизвестная тема спрайтов: {self.sprite_theme}, используем 'original'")
                self.sprite_theme = "original"
            
            print(f"Настройки загружены из {self.settings_file}")
            print(f"Тема спрайтов: {self.get_sprite_theme_name()}")
            
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
            print("Используются настройки по умолчанию")
    
    def reset_to_defaults(self):
        """Сброс настроек к значениям по умолчанию"""
        self.smooth_movement = True
        self.sound_volume = 0.8
        self.music_volume = 0.7
        self.sprite_theme = "original"
        self.save_settings()
        print("Настройки сброшены к значениям по умолчанию")