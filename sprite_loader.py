import pygame
import os

class SpriteLoader:
    def __init__(self):
        self.sprites = {}
        self.load_sprites()
    
    def load_sprites(self):
        """Загрузка спрайтов из art.png"""
        art_path = os.path.join("assets", "art.png")
        
        if not os.path.exists(art_path):
            print(f"Файл {art_path} не найден. Создаю заглушки...")
            self.create_placeholder_sprites()
            return
            
        try:
            # Загружаем основной файл спрайтов
            sprite_sheet = pygame.image.load(art_path).convert_alpha()
            print(f"Загружен файл спрайтов: {art_path}")
            
            # Размеры спрайта
            sprite_size = 64
            
            # Извлекаем спрайты
            self.extract_sprites(sprite_sheet, sprite_size)
            print("Спрайты успешно загружены")
            
        except pygame.error as e:
            print(f"Ошибка загрузки {art_path}: {e}")
            self.create_placeholder_sprites()
    
    def extract_sprites(self, sprite_sheet, sprite_size):
        """Извлечение спрайтов из спрайт-листа"""
        
        # Основные элементы (первый ряд)
        self.sprites['empty'] = self.get_sprite_from_sheet(sprite_sheet, 0, 0, sprite_size)
        self.sprites['earth'] = self.get_sprite_from_sheet(sprite_sheet, 1, 0, sprite_size)
        self.sprites['brick_wall'] = self.get_sprite_from_sheet(sprite_sheet, 2, 0, sprite_size)
        self.sprites['stone'] = self.get_sprite_from_sheet(sprite_sheet, 3, 0, sprite_size)
        
        # Выход (дверь)
        self.sprites['exit'] = self.get_sprite_from_sheet(sprite_sheet, 4, 0, sprite_size)
        
        # Анимация героя (третий ряд)
        self.sprites['hero'] = []
        for i in range(4):
            self.sprites['hero'].append(self.get_sprite_from_sheet(sprite_sheet, i, 2, sprite_size))
        
        # Анимация кристалла (седьмой ряд)
        self.sprites['crystal'] = []
        for i in range(4):
            self.sprites['crystal'].append(self.get_sprite_from_sheet(sprite_sheet, i, 6, sprite_size))
        
        # Дополнительные объекты (если есть в спрайт-листе)
        # Червяк (можно взять из другого ряда или использовать заглушку)
        self.sprites['worm'] = self.get_sprite_from_sheet(sprite_sheet, 5, 0, sprite_size)
        
        # Пузырь
        self.sprites['bubble'] = self.get_sprite_from_sheet(sprite_sheet, 6, 0, sprite_size)
    
    def get_sprite_from_sheet(self, sprite_sheet, col, row, sprite_size):
        """Извлечение одного спрайта из листа"""
        rect = pygame.Rect(col * sprite_size, row * sprite_size, sprite_size, sprite_size)
        sprite = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
        sprite.blit(sprite_sheet, (0, 0), rect)
        return sprite
    
    def create_placeholder_sprites(self):
        """Создание заглушек если файл не найден"""
        sprite_size = 64
        
        # Создаем простые цветные квадраты как заглушки
        self.sprites['empty'] = self.create_colored_sprite(sprite_size, (0, 0, 0))
        self.sprites['earth'] = self.create_colored_sprite(sprite_size, (139, 69, 19))
        self.sprites['brick_wall'] = self.create_colored_sprite(sprite_size, (165, 42, 42))
        self.sprites['stone'] = self.create_colored_sprite(sprite_size, (128, 128, 128))
        
        # Выход (дверь) - яркий цвет
        self.sprites['exit'] = self.create_colored_sprite(sprite_size, (255, 215, 0))  # Золотой
        
        # Анимация героя
        self.sprites['hero'] = []
        colors = [(0, 255, 0), (0, 200, 0), (0, 255, 50), (0, 200, 50)]
        for i, color in enumerate(colors):
            sprite = self.create_colored_sprite(sprite_size, color)
            # Добавляем номер кадра
            font = pygame.font.Font(None, 24)
            text = font.render(str(i+1), True, (255, 255, 255))
            sprite.blit(text, (sprite_size//2 - 6, sprite_size//2 - 12))
            self.sprites['hero'].append(sprite)
        
        # Анимация кристалла
        self.sprites['crystal'] = []
        crystal_colors = [(255, 0, 255), (255, 50, 255), (255, 100, 255), (255, 150, 255)]
        for color in crystal_colors:
            self.sprites['crystal'].append(self.create_colored_sprite(sprite_size, color))
        
        # Червяк
        self.sprites['worm'] = self.create_colored_sprite(sprite_size, (255, 100, 100))
        
        # Пузырь
        self.sprites['bubble'] = self.create_colored_sprite(sprite_size, (0, 255, 255))
        
        print("Созданы цветные заглушки для спрайтов")

    def create_colored_sprite(self, size, color):
        """Создание цветного спрайта"""
        sprite = pygame.Surface((size, size))
        sprite.fill(color)
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        return sprite
    
    def get_sprite(self, name):
        """Получение спрайта по имени"""
        return self.sprites.get(name, None)
