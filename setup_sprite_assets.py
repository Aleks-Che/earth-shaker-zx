import os

def create_sprite_directories():
    """Создает структуру папок для спрайтов"""
    
    directories = [
        "assets/original",
        "assets/enhanced", 
        "assets/modern"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Создана папка: {directory}")
    
    # Создаем README файлы для каждой папки
    readme_contents = {
        "assets/original/README.md": """# Оригинальные спрайты ZX80

Поместите сюда файл `sprites.png` с оригинальными спрайтами из ZX80 версии игры.

Размер спрайт-листа: 256x160 пикселей
Размер одного спрайта: 16x16 пикселей
Сетка: 16 столбцов × 10 рядов
""",
        "assets/enhanced/README.md": """# Улучшенные оригинальные спрайты

Поместите сюда файл `sprites.png` с улучшенными версиями оригинальных спрайтов.

Структура должна соответствовать оригинальному спрайт-листу, но с лучшим качеством.
""",
        "assets/modern/README.md": """# Современные спрайты

Поместите сюда файл `sprites.png` с современными спрайтами.

Размер спрайтов может быть больше (например, 64x64 пикселя).
Структура может отличаться от оригинала.
"""
    }
    
    for file_path, content in readme_contents.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Создан файл: {file_path}")

if __name__ == "__main__":
    create_sprite_directories()
    print("Структура папок для спрайтов создана!")