import pygame
from sprite_loaders import SpriteLoaderFactory

class SpriteManager:
    """Менеджер спрайтов, управляет загрузчиками разных тем"""
    
    def __init__(self, settings):
        self.settings = settings
        self.current_loader = None
        self.current_theme = None
        self.load_theme(settings.sprite_theme)
    
    def load_theme(self, theme):
        """Загружает тему спрайтов"""
        if self.current_theme == theme and self.current_loader:
            return  # Тема уже загружена
        
        print(f"Загружаем тему спрайтов: {theme}")
        self.current_loader = SpriteLoaderFactory.create_loader(theme)
        self.current_theme = theme
    
    def reload_if_needed(self):
        """Перезагружает спрайты если тема изменилась в настройках"""
        if self.current_theme != self.settings.sprite_theme:
            self.load_theme(self.settings.sprite_theme)
    
    def get_sprite(self, name):
        """Получение спрайта по имени"""
        if not self.current_loader:
            return None
        return self.current_loader.get_sprite(name)
    
    def get_animation(self, name):
        """Получение анимации по имени"""
        if not self.current_loader:
            return None
        return self.current_loader.get_animation(name)
    
    def get_sprite_size(self):
        """Получение размера спрайта"""
        if not self.current_loader:
            return 64  # Размер по умолчанию
        return self.current_loader.sprite_size
    
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