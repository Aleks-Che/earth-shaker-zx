import pygame
import os
from .original_sprite_loader import OriginalSpriteLoader

class ModernSpriteLoader(OriginalSpriteLoader):
    """Современный загрузчик спрайтов (пока наследует от оригинального)"""
    
    def __init__(self):
        print("Инициализация ModernSpriteLoader (используется оригинальный)...")
        super().__init__()
        self.sprite_size = 64  # Современные спрайты больше
        self.load_sprites()
    
    def get_sprite_sheet_path(self):
        """Путь к современному спрайт-листу"""
        return os.path.join("assets", "modern", "sprites.png")
    
    def load_sprites(self):
        """Загрузка современных спрайтов"""
        # Пока создаем только заглушки
        print("Современные спрайты пока не реализованы, создаю заглушки...")
        self.create_placeholder_sprites()
    
    def create_placeholder_sprites(self):
        """Создание современных заглушек"""
        # Создаем более красивые заглушки для современной темы
        
        # Герой с градиентом
        hero_frames = []
        for i in range(4):
            sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
            color = (0, 255 - i * 20, 0)
            pygame.draw.circle(sprite, color, (self.sprite_size//2, self.sprite_size//2), self.sprite_size//3)
            pygame.draw.circle(sprite, (255, 255, 255), (self.sprite_size//2, self.sprite_size//2), self.sprite_size//3, 2)
            hero_frames.append(sprite)
        self.animations['hero'] = hero_frames
        
        # Кристаллы с эффектом
        crystal_frames = []
        for i in range(6):
            sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
            color = (255, 0, 255 - i * 20)
            # Рисуем ромб
            points = [
                (self.sprite_size//2, 5),
                (self.sprite_size - 5, self.sprite_size//2),
                (self.sprite_size//2, self.sprite_size - 5),
                (5, self.sprite_size//2)
            ]
            pygame.draw.polygon(sprite, color, points)
            pygame.draw.polygon(sprite, (255, 255, 255), points, 2)
            crystal_frames.append(sprite)
        self.animations['crystal'] = crystal_frames
        
        # Остальные заглушки
        self.sprites['hero_dead'] = self.create_modern_placeholder((255, 0, 0), "X")
        self.sprites['monitor'] = self.create_modern_placeholder((0, 255, 255), "M")
        
        print("Созданы современные заглушки")
    
    def create_modern_placeholder(self, color, text=""):
        """Создание современной заглушки с текстом"""
        sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        
        # Градиентный фон
        for y in range(self.sprite_size):
            alpha = int(255 * (1 - y / self.sprite_size))
            line_color = (*color, alpha)
            temp_surf = pygame.Surface((self.sprite_size, 1), pygame.SRCALPHA)
            temp_surf.fill(line_color)
            sprite.blit(temp_surf, (0, y))
        
        # Рамка
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)
        
        # Текст
        if text:
            font = pygame.font.Font(None, 36)
            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(self.sprite_size//2, self.sprite_size//2))
            sprite.blit(text_surf, text_rect)
        
        return sprite