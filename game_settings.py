import config

class GameSettings:
    """Класс для управления настройками игры"""
    
    def __init__(self):
        self.smooth_movement = True
        self.sound_volume = 0.8
        self.music_volume = 0.7
        
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