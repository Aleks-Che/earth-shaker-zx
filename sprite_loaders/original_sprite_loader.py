import pygame
import os
from .base_sprite_loader import BaseSpriteLoader

class OriginalSpriteLoader(BaseSpriteLoader):
    """Загрузчик оригинальных спрайтов ZX Spectrum Earth Shaker"""
    
    def __init__(self):
        super().__init__()
        self.sprite_size = 16  # Размер спрайта в оригинале 16x16
        print("Инициализация OriginalSpriteLoader...")
        self.load_sprites()
    
    def get_sprite_sheet_path(self):
        """Путь к оригинальному спрайт-листу"""
        return os.path.join("assets", "original", "sprites.png")
    
    def extract_sprite(self, sprite_sheet, col, row):
        """Извлекает один спрайт из листа"""
        try:
            x = col * self.sprite_size
            y = row * self.sprite_size
            
            sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
            sprite.blit(sprite_sheet, (0, 0), pygame.Rect(x, y, self.sprite_size, self.sprite_size))
            return sprite
            
        except Exception as e:
            print(f"Ошибка извлечения спрайта ({col}, {row}): {e}")
            return self.create_placeholder_sprite((255, 0, 0))
    
    def load_sprites(self):
        """Загрузка всех спрайтов из оригинального листа"""
        sprite_path = self.get_sprite_sheet_path()
        
        print(f"Загрузка спрайтов из: {sprite_path}")
        print(f"Файл существует: {os.path.exists(sprite_path)}")
        
        if not os.path.exists(sprite_path):
            print("Файл не найден, создаю заглушки...")
            self.create_placeholder_sprites()
            return
        
        try:
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            sheet_width, sheet_height = sprite_sheet.get_size()
            print(f"Загружен спрайт-лист размером: {sheet_width}x{sheet_height}")
            
            # Загружаем основные спрайты
            self.extract_basic_sprites(sprite_sheet)
            print(f"Загружено спрайтов: {len(self.sprites)}, анимаций: {len(self.animations)}")
            
        except Exception as e:
            print(f"Ошибка загрузки спрайтов: {e}")
            self.create_placeholder_sprites()
    
    def extract_basic_sprites(self, sprite_sheet):
        """Извлечение основных спрайтов для игры"""
        
        print("Извлекаю основные спрайты...")
        
        try:
            # Ряд 1: Главный герой (позиции 0-3), мертвый герой (4)
            hero_frames = []
            for i in range(4):
                frame = self.extract_sprite(sprite_sheet, i, 1)
                hero_frames.append(frame)
            self.animations['hero'] = hero_frames
            self.sprites['hero_dead'] = self.extract_sprite(sprite_sheet, 4, 1)
            
            # Кристаллы (позиции 5-10 в ряду 1)
            crystal_frames = []
            for i in range(5, 11):
                frame = self.extract_sprite(sprite_sheet, i, 1)
                crystal_frames.append(frame)
            self.animations['crystal'] = crystal_frames
            
            # Пузыри (позиции 11-14 в ряду 1)
            bubble_frames = []
            for i in range(11, 15):
                frame = self.extract_sprite(sprite_sheet, i, 1)
                bubble_frames.append(frame)
            self.animations['bubble'] = bubble_frames
            
            # Монитор (позиция 15 в ряду 1)
            self.sprites['monitor'] = self.extract_sprite(sprite_sheet, 15, 1)
            
            # Камни разных цветов (ряд 2, позиции 0-6)
            stone_colors = ['blue', 'red', 'purple', 'green', 'cyan', 'yellow', 'gray']
            for i, color in enumerate(stone_colors):
                if i < 7:
                    self.sprites[f'stone_{color}'] = self.extract_sprite(sprite_sheet, i, 2)
            
            # Земля разных цветов (ряд 2, позиции 7-13)
            for i, color in enumerate(stone_colors):
                if i < 7:
                    self.sprites[f'earth_{color}'] = self.extract_sprite(sprite_sheet, i + 7, 2)
            
            # Добавляем псевдоним earth_brown -> earth_yellow
            self.sprites['earth_brown'] = self.sprites['earth_yellow']
            
            # Стены (ряд 3, позиции 0-15)
            wall_types = ['brick_red', 'brick_purple', 'brick_cyan', 'brick_yellow',
                         'concrete_gray', 'steel_green', 'overgrown_gray', 'ice_cyan']
            for i, wall_type in enumerate(wall_types):
                if i < 16:
                    self.sprites[f'wall_{wall_type}'] = self.extract_sprite(sprite_sheet, i, 3)
            
            # Двери (ряд 5, позиции 0-6)
            door_colors = ['blue', 'red', 'purple', 'green', 'cyan', 'yellow', 'gray']
            for i, color in enumerate(door_colors):
                if i < 7:
                    self.sprites[f'door_{color}'] = self.extract_sprite(sprite_sheet, i, 5)
            
            print("Основные спрайты загружены успешно!")
            
        except Exception as e:
            print(f"Ошибка при извлечении спрайтов: {e}")
            self.create_placeholder_sprites()
    
    def create_placeholder_sprite(self, color):
        """Создание цветной заглушки"""
        sprite = pygame.Surface((self.sprite_size, self.sprite_size))
        sprite.fill(color)
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 1)
        return sprite
    
    def create_placeholder_sprites(self):
        """Создание заглушек если файл не найден"""
        print("Создаю заглушки для оригинальных спрайтов...")
        
        # Основные спрайты
        self.sprites['hero_dead'] = self.create_placeholder_sprite((255, 0, 0))
        self.sprites['monitor'] = self.create_placeholder_sprite((0, 255, 255))
        
        # Анимации как заглушки
        self.animations['hero'] = [self.create_placeholder_sprite((0, 255, 0)) for _ in range(4)]
        self.animations['crystal'] = [self.create_placeholder_sprite((255, 0, 255)) for _ in range(6)]
        self.animations['bubble'] = [self.create_placeholder_sprite((0, 255, 255)) for _ in range(4)]
        
        # Камни и земля
        colors = [(0, 0, 255), (255, 0, 0), (255, 0, 255), (0, 255, 0), 
                 (0, 255, 255), (255, 255, 0), (128, 128, 128)]
        color_names = ['blue', 'red', 'purple', 'green', 'cyan', 'yellow', 'gray']
        
        for color, name in zip(colors, color_names):
            self.sprites[f'stone_{name}'] = self.create_placeholder_sprite(color)
            earth_color = tuple(max(0, c // 2) for c in color)  # Темнее для земли
            self.sprites[f'earth_{name}'] = self.create_placeholder_sprite(earth_color)
            self.sprites[f'door_{name}'] = self.create_placeholder_sprite(color)
        
        # Стены
        wall_colors = [(165, 42, 42), (128, 0, 128), (0, 255, 255), (255, 255, 0),
                      (128, 128, 128), (0, 128, 0), (105, 105, 105), (175, 238, 238)]
        wall_types = ['brick_red', 'brick_purple', 'brick_cyan', 'brick_yellow',
                     'concrete_gray', 'steel_green', 'overgrown_gray', 'ice_cyan']
        
        for color, wall_type in zip(wall_colors, wall_types):
            self.sprites[f'wall_{wall_type}'] = self.create_placeholder_sprite(color)
        
        # Добавляем отсутствующие спрайты и псевдонимы
        self.sprites['earth_brown'] = self.sprites['earth_yellow']  # Псевдоним
        self.sprites['worm'] = self.create_placeholder_sprite((255, 0, 255))  # Червь
        self.sprites['fire'] = self.create_placeholder_sprite((255, 100, 0))  # Огонь
        
        print("Заглушки для оригинальных спрайтов созданы")