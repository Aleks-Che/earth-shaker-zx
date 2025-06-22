import os
import pygame

def create_assets_folder():
    """Создание папки assets если её нет"""
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("Создана папка assets")
    
    # Проверяем наличие art.png
    if not os.path.exists(os.path.join("assets", "art.png")):
        print("ВНИМАНИЕ: Файл art.png не найден в папке assets")
        print("Игра будет использовать цветные заглушки вместо спрайтов")
        create_placeholder_art()

def create_placeholder_art():
    """Создание заглушки для art.png"""
    pygame.init()
    
    # Создаем заглушку 640x640
    surface = pygame.Surface((640, 640))
    surface.fill((50, 50, 50))
    
    # Рисуем простые спрайты
    tile_size = 64
    
    # Пустой тайл (черный)
    pygame.draw.rect(surface, (0, 0, 0), (0, 0, tile_size, tile_size))
    
    # Земля (коричневый)
    pygame.draw.rect(surface, (139, 69, 19), (tile_size, 0, tile_size, tile_size))
    
    # Кирпичная стена (красно-коричневый)
    pygame.draw.rect(surface, (165, 42, 42), (tile_size * 2, 0, tile_size, tile_size))
    
    # Камень (серый)
    pygame.draw.rect(surface, (128, 128, 128), (tile_size * 3, 0, tile_size, tile_size))
    
    # Герой (зеленый) - 4 кадра анимации
    for i in range(4):
        color_intensity = 200 + i * 10
        pygame.draw.rect(surface, (0, color_intensity, 0), 
                        (i * tile_size, tile_size * 2, tile_size, tile_size))
    
    # Кристалл (фиолетовый) - 4 кадра анимации
    for i in range(4):
        color_intensity = 200 + i * 10
        pygame.draw.rect(surface, (color_intensity, 0, 255), 
                        (i * tile_size, tile_size * 6, tile_size, tile_size))
    
    # Сохраняем заглушку
    pygame.image.save(surface, os.path.join("assets", "art.png"))
    print("Создан файл-заглушка art.png")

if __name__ == "__main__":
    create_assets_folder()