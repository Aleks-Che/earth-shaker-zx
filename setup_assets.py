import os

def create_assets_folder():
    """Создание папки assets и подпапок если их нет"""
    
    # Основная папка assets
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("Создана папка assets/")
    
    # Подпапки
    subfolders = ["sounds", "music", "sprites"]
    
    for folder in subfolders:
        folder_path = os.path.join("assets", folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Создана папка {folder_path}/")
    
    # Создаем файл README в папке assets
    readme_path = os.path.join("assets", "README.txt")
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("""Папка ресурсов EarthShaker

Структура папок:
- sounds/ - звуковые эффекты (.wav, .ogg)
- music/ - фоновая музыка (.ogg, .mp3)
- sprites/ - спрайты и изображения (.png)

Для полноценной работы игры поместите соответствующие файлы в эти папки.
Игра будет работать и без них, используя цветные заглушки.
""")
        print("Создан файл assets/README.txt")

if __name__ == "__main__":
    create_assets_folder()