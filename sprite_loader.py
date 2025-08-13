import pygame
import os

class SpriteLoader:
    """Базовый загрузчик спрайтов для обратной совместимости"""
    
    def __init__(self):
        self.sprites = {}
        self.sprite_size = 64
        self.load_sprites()
    
    def load_sprites(self):
        """Загрузка спрайтов"""
        # Попытка загрузить спрайт-лист из темы "original"
        # Оригинальный путь был "assets/sprites/art.png", но фактическое расположение:
        # assets/sprites/original/art.png (или assets/original/sprites.png для старого скрипта)
        # Поэтому ищем в подпапке темы.
        art_path = os.path.join("assets", "sprites", "original", "art.png")
        
        if os.path.exists(art_path):
            try:
                self.load_from_spritesheet(art_path)
                print(f"Загружен файл спрайтов: {art_path}")
            except pygame.error as e:
                print(f"Ошибка загрузки {art_path}: {e}")
                self.create_placeholder_sprites()
        else:
            print(f"Файл {art_path} не найден. Создаю заглушки...")
            self.create_placeholder_sprites()
    
    def load_from_spritesheet(self, sprite_path):
        """Загрузка спрайтов из спрайт-листа"""
        sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        
        # Основные элементы (первый ряд)
        self.sprites['empty'] = None  # Пустые тайлы не рисуем
        self.sprites['earth'] = self.get_sprite_from_sheet(sprite_sheet, 1, 0)
        self.sprites['brick_wall'] = self.get_sprite_from_sheet(sprite_sheet, 2, 0)
        self.sprites['stone'] = self.get_sprite_from_sheet(sprite_sheet, 3, 0)
        self.sprites['exit'] = self.get_sprite_from_sheet(sprite_sheet, 4, 0)
        
        # Анимация героя (третий ряд)
        self.sprites['hero'] = []
        for i in range(4):
            self.sprites['hero'].append(self.get_sprite_from_sheet(sprite_sheet, i, 2))
        
        # Анимация кристалла (седьмой ряд)
        self.sprites['crystal'] = []
        for i in range(4):
            self.sprites['crystal'].append(self.get_sprite_from_sheet(sprite_sheet, i, 6))
        
        # Дополнительные объекты
        self.sprites['worm'] = self.get_sprite_from_sheet(sprite_sheet, 5, 0)
        self.sprites['bubble'] = self.get_sprite_from_sheet(sprite_sheet, 6, 0)
    
    def get_sprite_from_sheet(self, sprite_sheet, col, row):
        """Извлечение одного спрайта из листа"""
        rect = pygame.Rect(col * self.sprite_size, row * self.sprite_size, 
                          self.sprite_size, self.sprite_size)
        sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        sprite.blit(sprite_sheet, (0, 0), rect)
        return sprite
    
    def create_placeholder_sprites(self):
        """Создание заглушек если файл не найден"""
        # Создаем простые цветные квадраты как заглушки
        self.sprites['empty'] = None
        
        # Земля разных цветов
        self.sprites['earth'] = self.create_colored_sprite((139, 69, 19))
        self.sprites['earth_brown'] = self.create_colored_sprite((139, 69, 19))
        self.sprites['earth_blue'] = self.create_colored_sprite((0, 0, 139))
        self.sprites['earth_red'] = self.create_colored_sprite((139, 0, 0))
        self.sprites['earth_green'] = self.create_colored_sprite((0, 139, 0))
        self.sprites['earth_gray'] = self.create_colored_sprite((105, 105, 105))
        
        # Стены разных типов
        self.sprites['brick_wall'] = self.create_colored_sprite((165, 42, 42))
        self.sprites['wall_brick_red'] = self.create_colored_sprite((165, 42, 42))
        self.sprites['wall_brick_purple'] = self.create_colored_sprite((128, 0, 128))
        self.sprites['wall_concrete_gray'] = self.create_colored_sprite((128, 128, 128))
        
        # Камни разных цветов
        self.sprites['stone'] = self.create_colored_sprite((128, 128, 128))
        self.sprites['stone_gray'] = self.create_colored_sprite((128, 128, 128))
        self.sprites['stone_blue'] = self.create_colored_sprite((0, 0, 255))
        self.sprites['stone_red'] = self.create_colored_sprite((255, 0, 0))
        self.sprites['stone_green'] = self.create_colored_sprite((0, 255, 0))
        
        # Двери разных цветов
        self.sprites['exit'] = self.create_colored_sprite((255, 215, 0))
        self.sprites['door_yellow'] = self.create_colored_sprite((255, 215, 0))
        self.sprites['door_blue'] = self.create_colored_sprite((0, 0, 255))
        self.sprites['door_red'] = self.create_colored_sprite((255, 0, 0))
        self.sprites['door_green'] = self.create_colored_sprite((0, 255, 0))
        
        # Огонь
        self.sprites['fire'] = self.create_colored_sprite((255, 100, 0))
        
        # Анимация героя
        self.sprites['hero'] = []
        colors = [(0, 255, 0), (0, 200, 0), (0, 255, 50), (0, 200, 50)]
        for i, color in enumerate(colors):
            sprite = self.create_colored_sprite(color)
            # Добавляем номер кадра
            font = pygame.font.Font(None, 24)
            text = font.render(str(i+1), True, (255, 255, 255))
            sprite.blit(text, (self.sprite_size//2 - 6, self.sprite_size//2 - 12))
            self.sprites['hero'].append(sprite)
        
        # Мертвый герой
        self.sprites['hero_dead'] = self.create_colored_sprite((255, 0, 0))
        
        # Анимация кристалла
        self.sprites['crystal'] = []
        crystal_colors = [(255, 0, 255), (255, 50, 255), (255, 100, 255), (255, 150, 255)]
        for color in crystal_colors:
            self.sprites['crystal'].append(self.create_colored_sprite(color))
        
        # Червяк
        self.sprites['worm'] = self.create_colored_sprite((255, 100, 100))
        
        # Пузырь
        self.sprites['bubble'] = self.create_colored_sprite((0, 255, 255))
        
        print("Созданы цветные заглушки для спрайтов")
    
    def create_colored_sprite(self, color):
        """Создание цветного спрайта"""
        sprite = pygame.Surface((self.sprite_size, self.sprite_size))
        sprite.fill(color)
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        return sprite
    
    def get_sprite(self, name):
        """Получение спрайта по имени"""
        sprite = self.sprites.get(name, None)
        if isinstance(sprite, list):
            return sprite[0] if sprite else None
        return sprite
    
    def get_animation(self, name):
        """Получение анимации по имени"""
        sprite = self.sprites.get(name, None)
        if isinstance(sprite, list):
            return sprite
        return None
    
    def get_sprite_size(self):
        """Получение размера спрайта"""
        return 64  # Размер по умолчанию
    
    def scale_sprite(self, sprite, target_size):
        """Масштабирование спрайта до нужного размера"""
        if not sprite:
            return None
        
        current_size = sprite.get_width()
        if current_size == target_size:
            return sprite
        
        return pygame.transform.scale(sprite, (target_size, target_size))
    
    def scale_animation(self, animation, target_size):
        """Масштабирование анимации до нужного размера"""
        if not animation:
            return None
        
        return [self.scale_sprite(frame, target_size) for frame in animation]
    
    def get_scaled_sprite(self, name, target_size=64):
        """Получение масштабированного спрайта"""
        sprite = self.get_sprite(name)
        return self.scale_sprite(sprite, target_size)
    
    def get_scaled_animation(self, name, target_size=64):
        """Получение масштабированной анимации"""
        animation = self.get_animation(name)
        return self.scale_animation(animation, target_size)
