#!/usr/bin/env python3
"""
Скрипт для проверки доступных спрайтов
"""

import pygame
from sprite_loaders.sprite_loader_factory import SpriteLoaderFactory

def check_sprites():
    """Проверка доступных спрайтов"""
    pygame.init()
    
    loader = SpriteLoaderFactory.create_loader("original")
    
    print("=== Доступные спрайты ===")
    print("Одиночные спрайты:")
    for name in sorted(loader.sprites.keys()):
        print(f"  - {name}")
    
    print("\nАнимации:")
    for name in sorted(loader.animations.keys()):
        frames = len(loader.animations[name])
        print(f"  - {name}: {frames} кадров")
    
    print("\n=== Проверка соответствия с уровнем ===")
    
    # Проверим, какие имена используются в уровне
    level_names = [
        'earth_brown', 'earth_blue', 'earth_red', 'earth_green', 'earth_gray',
        'stone_gray', 'stone_blue', 'stone_red', 'stone_green',
        'wall_brick_red', 'wall_brick_purple', 'wall_concrete_gray',
        'door_yellow', 'door_blue', 'door_red', 'door_green',
        'crystal', 'worm', 'bubble', 'fire'
    ]
    
    print("Проверка имен из уровня:")
    for name in level_names:
        if name in loader.sprites:
            print(f"  ✓ {name}: есть как одиночный спрайт")
        elif name in loader.animations:
            print(f"  ✓ {name}: есть как анимация ({len(loader.animations[name])} кадров)")
        else:
            print(f"  ✗ {name}: НЕ НАЙДЕН")
    
    # Проверим альтернативные имена
    print("\nПроверка альтернативных имен:")
    alt_names = {
        'earth_brown': ['earth_brown', 'earth'],
        'stone_gray': ['stone_gray', 'stone'],
        'wall_brick_red': ['wall_brick_red', 'wall_brick'],
        'door_yellow': ['door_yellow', 'door', 'exit']
    }
    
    for original, alts in alt_names.items():
        found = []
        for alt in alts:
            if alt in loader.sprites:
                found.append(f"{alt} (спрайт)")
            elif alt in loader.animations:
                found.append(f"{alt} (анимация)")
        if found:
            print(f"  {original} -> {', '.join(found)}")
        else:
            print(f"  {original} -> НЕ НАЙДЕНО")

if __name__ == "__main__":
    check_sprites()