import os
from .original_sprite_loader import OriginalSpriteLoader

class EnhancedSpriteLoader(OriginalSpriteLoader):
    """Улучшенный загрузчик спрайтов (пока наследует от оригинального)"""
    
    def __init__(self):
        print("Инициализация EnhancedSpriteLoader (используется оригинальный)...")
        super().__init__()
    
    def get_sprite_sheet_path(self):
        """Путь к улучшенному спрайт-листу"""
        return os.path.join("assets", "enhanced", "sprites.png")
    
    def load_sprites(self):
        """Загрузка улучшенных спрайтов"""
        # Пока используем оригинальную логику
        super().load_sprites()
        print("Загружены улучшенные спрайты (пока как оригинальные)")