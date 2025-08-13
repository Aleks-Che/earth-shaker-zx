from .original_sprite_loader import OriginalSpriteLoader
from .enhanced_sprite_loader import EnhancedSpriteLoader
from .modern_sprite_loader import ModernSpriteLoader

class SpriteLoaderFactory:
    """Фабрика для создания загрузчиков спрайтов"""
    
    @staticmethod
    def create_loader(theme):
        """Создает загрузчик спрайтов для указанной темы"""
        
        print(f"Создаем загрузчик для темы: {theme}")
        
        if theme == "original":
            return OriginalSpriteLoader()
        elif theme == "enhanced":
            return EnhancedSpriteLoader()
        elif theme == "modern":
            return ModernSpriteLoader()
        else:
            print(f"Неизвестная тема спрайтов: {theme}, используем оригинальную")
            return OriginalSpriteLoader()