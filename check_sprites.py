import pygame
import os

def check_sprite_file():
    """Проверка файла спрайтов"""
    
    pygame.init()
    
    sprite_path = os.path.join("assets", "original", "sprites.png")
    
    print(f"Проверка файла: {sprite_path}")
    print(f"Абсолютный путь: {os.path.abspath(sprite_path)}")
    print(f"Файл существует: {os.path.exists(sprite_path)}")
    
    if os.path.exists(sprite_path):
        try:
            # Получаем информацию о файле
            file_size = os.path.getsize(sprite_path)
            print(f"Размер файла: {file_size} байт")
            
            # Пытаемся загрузить изображение
            image = pygame.image.load(sprite_path)
            width, height = image.get_size()
            print(f"Размер изображения: {width}x{height} пикселей")
            print(f"Ожидаемый размер: 256x160 пикселей")
            
            if width == 256 and height == 160:
                print("✅ Размер изображения соответствует ожидаемому!")
            else:
                print("⚠️  Размер изображения НЕ соответствует ожидаемому!")
                print("   Это может быть причиной проблем с загрузкой спрайтов")
            
            # Проверяем формат
            print(f"Формат изображения: {image.get_flags()}")
            print(f"Битность: {image.get_bitsize()}")
            
            # Проверяем, можно ли извлечь тестовый спрайт
            test_sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
            test_sprite.blit(image, (0, 0), pygame.Rect(0, 16, 16, 16))  # Первый спрайт героя
            
            print("✅ Тестовое извлечение спрайта прошло успешно!")
            
        except pygame.error as e:
            print(f"❌ Ошибка загрузки изображения: {e}")
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
    else:
        print("❌ Файл спрайтов не найден!")
        print("\nДля решения проблемы:")
        print("1. Убедитесь, что файл sprites.png находится в папке assets/original/")
        print("2. Проверьте, что файл не поврежден")
        print("3. Убедитесь, что размер файла 256x160 пикселей")
        
        # Проверяем структуру папок
        print("\nПроверка структуры папок:")
        assets_path = "assets"
        if os.path.exists(assets_path):
            print(f"✅ Папка {assets_path} существует")
            
            original_path = os.path.join(assets_path, "original")
            if os.path.exists(original_path):
                print(f"✅ Папка {original_path} существует")
                
                # Показываем содержимое папки
                files = os.listdir(original_path)
                print(f"Содержимое папки {original_path}:")
                for file in files:
                    print(f"  - {file}")
            else:
                print(f"❌ Папка {original_path} НЕ существует")
        else:
            print(f"❌ Папка {assets_path} НЕ существует")

if __name__ == "__main__":
    check_sprite_file()
