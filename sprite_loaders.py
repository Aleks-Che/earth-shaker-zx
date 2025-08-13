import pygame
import os
from abc import ABC, abstractmethod

class BaseSpriteLoader(ABC):
    """Базовый класс для загрузчиков спрайтов"""
    
    def __init__(self):
        self.sprites = {}
        self.sprite_size = 64
        self.load_sprites()
    
    @abstractmethod
    def load_sprites(self):
        """Загрузка спрайтов - должен быть реализован в наследниках"""
        pass
    
    def get_sprite(self, name):
        """Получение спрайта по имени"""
        return self.sprites.get(name, None)
    
    def get_animation(self, name):
        """Получение анимации по имени"""
        sprite = self.sprites.get(name, None)
        if isinstance(sprite, list):
            return sprite
        return None
    
    def create_colored_sprite(self, size, color):
        """Создание цветного спрайта"""
        sprite = pygame.Surface((size, size))
        sprite.fill(color)
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        return sprite

class OriginalSpriteLoader(BaseSpriteLoader):
    """Загрузчик оригинальных спрайтов"""
    
    def load_sprites(self):
        """Загрузка оригинальных спрайтов"""
        art_path = os.path.join("assets", "art.png")
        
        if os.path.exists(art_path):
            try:
                sprite_sheet = pygame.image.load(art_path).convert_alpha()
                self.extract_sprites_from_sheet(sprite_sheet)
                print("Загружены оригинальные спрайты")
                return
            except pygame.error as e:
                print(f"Ошибка загрузки {art_path}: {e}")
        
        # Если файл не найден, создаем заглушки
        self.create_placeholder_sprites()
    
    def extract_sprites_from_sheet(self, sprite_sheet):
        """Извлечение спрайтов из листа"""
        # Основные элементы
        self.sprites['empty'] = self.get_sprite_from_sheet(sprite_sheet, 0, 0)
        self.sprites['earth'] = self.get_sprite_from_sheet(sprite_sheet, 1, 0)
        self.sprites['earth_brown'] = self.get_sprite_from_sheet(sprite_sheet, 1, 0)
        self.sprites['brick_wall'] = self.get_sprite_from_sheet(sprite_sheet, 2, 0)
        self.sprites['wall_brick_red'] = self.get_sprite_from_sheet(sprite_sheet, 2, 0)
        self.sprites['stone'] = self.get_sprite_from_sheet(sprite_sheet, 3, 0)
        self.sprites['stone_gray'] = self.get_sprite_from_sheet(sprite_sheet, 3, 0)
        self.sprites['exit'] = self.get_sprite_from_sheet(sprite_sheet, 4, 0)
        self.sprites['door_yellow'] = self.get_sprite_from_sheet(sprite_sheet, 4, 0)
        
        # Анимации
        self.sprites['hero'] = []
        for i in range(4):
            self.sprites['hero'].append(self.get_sprite_from_sheet(sprite_sheet, i, 2))
        
        self.sprites['crystal'] = []
        for i in range(4):
            self.sprites['crystal'].append(self.get_sprite_from_sheet(sprite_sheet, i, 6))
        
        # Дополнительные объекты
        self.sprites['worm'] = self.get_sprite_from_sheet(sprite_sheet, 5, 0)
        self.sprites['bubble'] = self.get_sprite_from_sheet(sprite_sheet, 6, 0)
    
    def get_sprite_from_sheet(self, sprite_sheet, col, row):
        """Извлечение спрайта из листа"""
        rect = pygame.Rect(col * self.sprite_size, row * self.sprite_size, 
                          self.sprite_size, self.sprite_size)
        sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        sprite.blit(sprite_sheet, (0, 0), rect)
        return sprite
    
    def create_placeholder_sprites(self):
        """Создание заглушек"""
        # Базовые спрайты
        self.sprites['empty'] = self.create_colored_sprite(self.sprite_size, (0, 0, 0))
        self.sprites['earth'] = self.create_colored_sprite(self.sprite_size, (139, 69, 19))
        self.sprites['earth_brown'] = self.create_colored_sprite(self.sprite_size, (139, 69, 19))
        self.sprites['brick_wall'] = self.create_colored_sprite(self.sprite_size, (165, 42, 42))
        self.sprites['wall_brick_red'] = self.create_colored_sprite(self.sprite_size, (165, 42, 42))
        self.sprites['stone'] = self.create_colored_sprite(self.sprite_size, (128, 128, 128))
        self.sprites['stone_gray'] = self.create_colored_sprite(self.sprite_size, (128, 128, 128))
        self.sprites['exit'] = self.create_colored_sprite(self.sprite_size, (255, 215, 0))
        self.sprites['door_yellow'] = self.create_colored_sprite(self.sprite_size, (255, 215, 0))
        self.sprites['fire'] = self.create_colored_sprite(self.sprite_size, (255, 100, 0))
        
        # Дополнительные цвета
        self.sprites['earth_blue'] = self.create_colored_sprite(self.sprite_size, (0, 0, 139))
        self.sprites['earth_red'] = self.create_colored_sprite(self.sprite_size, (139, 0, 0))
        self.sprites['earth_green'] = self.create_colored_sprite(self.sprite_size, (0, 139, 0))
        self.sprites['earth_gray'] = self.create_colored_sprite(self.sprite_size, (105, 105, 105))
        
        self.sprites['wall_brick_purple'] = self.create_colored_sprite(self.sprite_size, (128, 0, 128))
        self.sprites['wall_concrete_gray'] = self.create_colored_sprite(self.sprite_size, (128, 128, 128))
        
        self.sprites['stone_blue'] = self.create_colored_sprite(self.sprite_size, (0, 0, 255))
        self.sprites['stone_red'] = self.create_colored_sprite(self.sprite_size, (255, 0, 0))
        self.sprites['stone_green'] = self.create_colored_sprite(self.sprite_size, (0, 255, 0))
        
        self.sprites['door_blue'] = self.create_colored_sprite(self.sprite_size, (0, 0, 255))
        self.sprites['door_red'] = self.create_colored_sprite(self.sprite_size, (255, 0, 0))
        self.sprites['door_green'] = self.create_colored_sprite(self.sprite_size, (0, 255, 0))
        
        # Анимации
        self.sprites['hero'] = []
        colors = [(0, 255, 0), (0, 200, 0), (0, 255, 50), (0, 200, 50)]
        for i, color in enumerate(colors):
            sprite = self.create_colored_sprite(self.sprite_size, color)
            font = pygame.font.Font(None, 24)
            text = font.render(str(i+1), True, (255, 255, 255))
            sprite.blit(text, (self.sprite_size//2 - 6, self.sprite_size//2 - 12))
            self.sprites['hero'].append(sprite)
        
        self.sprites['hero_dead'] = self.create_colored_sprite(self.sprite_size, (255, 0, 0))
        
        self.sprites['crystal'] = []
        crystal_colors = [(255, 0, 255), (255, 50, 255), (255, 100, 255), (255, 150, 255)]
        for color in crystal_colors:
            self.sprites['crystal'].append(self.create_colored_sprite(self.sprite_size, color))
        
        self.sprites['worm'] = self.create_colored_sprite(self.sprite_size, (255, 100, 100))
        self.sprites['bubble'] = self.create_colored_sprite(self.sprite_size, (0, 255, 255))
        
        print("Созданы заглушки для оригинальной темы")

class EnhancedSpriteLoader(OriginalSpriteLoader):
    """Улучшенная версия оригинальных спрайтов"""
    
    def create_placeholder_sprites(self):
        """Создание улучшенных заглушек"""
        super().create_placeholder_sprites()
        # Здесь можно добавить улучшения
        print("Созданы заглушки для улучшенной темы")

class ModernSpriteLoader(BaseSpriteLoader):
    """Современные спрайты"""
    
    def load_sprites(self):
        """Загрузка современных спрайтов"""
        # Пока используем заглушки
        self.create_placeholder_sprites()
    
    def create_placeholder_sprites(self):
        """Создание современных заглушек"""
        # Более яркие и современные цвета
        self.sprites['empty'] = self.create_colored_sprite(self.sprite_size, (0, 0, 0))
        self.sprites['earth'] = self.create_colored_sprite(self.sprite_size, (101, 67, 33))
        self.sprites['earth_brown'] = self.create_colored_sprite(self.sprite_size, (101, 67, 33))
        self.sprites['brick_wall'] = self.create_colored_sprite(self.sprite_size, (139, 69, 19))
        self.sprites['wall_brick_red'] = self.create_colored_sprite(self.sprite_size, (139, 69, 19))
        self.sprites['stone'] = self.create_colored_sprite(self.sprite_size, (105, 105, 105))
        self.sprites['stone_gray'] = self.create_colored_sprite(self.sprite_size, (105, 105, 105))
        self.sprites['exit'] = self.create_colored_sprite(self.sprite_size, (255, 223, 0))
        self.sprites['door_yellow'] = self.create_colored_sprite(self.sprite_size, (255, 223, 0))
        self.sprites['fire'] = self.create_colored_sprite(self.sprite_size, (255, 69, 0))
        
        # Дополнительные цвета
        self.sprites['earth_blue'] = self.create_colored_sprite(self.sprite_size, (30, 144, 255))
        self.sprites['earth_red'] = self.create_colored_sprite(self.sprite_size, (220, 20, 60))
        self.sprites['earth_green'] = self.create_colored_sprite(self.sprite_size, (34, 139, 34))
        self.sprites['earth_gray'] = self.create_colored_sprite(self.sprite_size, (128, 128, 128))
        
        self.sprites['wall_brick_purple'] = self.create_colored_sprite(self.sprite_size, (147, 112, 219))
        self.sprites['wall_concrete_gray'] = self.create_colored_sprite(self.sprite_size, (169, 169, 169))
        
        self.sprites['stone_blue'] = self.create_colored_sprite(self.sprite_size, (70, 130, 180))
        self.sprites['stone_red'] = self.create_colored_sprite(self.sprite_size, (178, 34, 34))
        self.sprites['stone_green'] = self.create_colored_sprite(self.sprite_size, (60, 179, 113))
        
        self.sprites['door_blue'] = self.create_colored_sprite(self.sprite_size, (30, 144, 255))
        self.sprites['door_red'] = self.create_colored_sprite(self.sprite_size, (220, 20, 60))
        self.sprites['door_green'] = self.create_colored_sprite(self.sprite_size, (34, 139, 34))
        
        # Анимации с более яркими цветами
        self.sprites['hero'] = []
        colors = [(50, 205, 50), (34, 139, 34), (0, 255, 127), (46, 139, 87)]
        for i, color in enumerate(colors):
            sprite = self.create_colored_sprite(self.sprite_size, color)
            font = pygame.font.Font(None, 24)
            text = font.render(str(i+1), True, (255, 255, 255))
            sprite.blit(text, (self.sprite_size//2 - 6, self.sprite_size//2 - 12))
            self.sprites['hero'].append(sprite)
        
        self.sprites['hero_dead'] = self.create_colored_sprite(self.sprite_size, (220, 20, 60))
        
        self.sprites['crystal'] = []
        crystal_colors = [(255, 20, 147), (255, 105, 180), (255, 182, 193), (255, 192, 203)]
        for color in crystal_colors:
            self.sprites['crystal'].append(self.create_colored_sprite(self.sprite_size, color))
        
        self.sprites['worm'] = self.create_colored_sprite(self.sprite_size, (255, 140, 0))
        self.sprites['bubble'] = self.create_colored_sprite(self.sprite_size, (0, 191, 255))
        
        print("Созданы заглушки для современной темы")

class SpriteLoaderFactory:
    """Фабрика для создания загрузчиков спрайтов"""
    
    @staticmethod
    def create_loader(theme):
        """Создание загрузчика по теме"""
        if theme == "original":
            return OriginalSpriteLoader()
        elif theme == "enhanced":
            return EnhancedSpriteLoader()
        elif theme == "modern":
            return ModernSpriteLoader()
        else:
            print(f"Неизвестная тема: {theme}, используем оригинальную")
            return OriginalSpriteLoader()