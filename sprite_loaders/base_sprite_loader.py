import pygame

class BaseSpriteLoader:
    """Базовый класс для загрузчиков спрайтов"""
    
    def __init__(self):
        self.sprites = {}  # Одиночные спрайты
        self.animations = {}  # Анимации (списки спрайтов)
        self.sprite_size = 64  # Размер спрайта по умолчанию
    
    def get_sprite(self, name):
        """Получение спрайта по имени"""
        return self.sprites.get(name, None)
    
    def get_animation(self, name):
        """Получение анимации по имени"""
        return self.animations.get(name, None)
    
    def extract_animation(self, sprite_sheet, start_col, end_col, row):
        """Извлечение анимации из спрайт-листа"""
        frames = []
        for col in range(start_col, end_col + 1):
            sprite = self.extract_sprite(sprite_sheet, col, row)
            if sprite:
                frames.append(sprite)
        return frames
    
    def extract_sprite(self, sprite_sheet, col, row):
        """Извлечение одного спрайта - должно быть переопределено в наследниках"""
        raise NotImplementedError("Метод должен быть переопределен в наследнике")
    
    def load_sprites(self):
        """Загрузка спрайтов - должно быть переопределено в наследниках"""
        raise NotImplementedError("Метод должен быть переопределен в наследнике")