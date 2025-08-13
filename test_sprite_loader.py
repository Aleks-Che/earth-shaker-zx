#!/usr/bin/env python3
"""
Тестовый скрипт для проверки загрузки спрайтов
"""

import pygame
import sys
import os
from sprite_loaders.sprite_loader_factory import SpriteLoaderFactory

def test_sprite_loader():
    """Тестирование загрузки спрайтов"""
    print("=== Тест загрузки спрайтов ===")
    
    # Инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Тест загрузки спрайтов")
    
    # Тестируем оригинальный загрузчик
    print("\n1. Тестируем оригинальный загрузчик...")
    original_loader = SpriteLoaderFactory.create_loader("original")
    
    print(f"   Размер спрайта: {original_loader.sprite_size}")
    print(f"   Количество спрайтов: {len(original_loader.sprites)}")
    print(f"   Количество анимаций: {len(original_loader.animations)}")
    
    # Проверяем основные спрайты
    essential_sprites = ['hero', 'crystal', 'stone_blue', 'earth_brown', 'wall_brick_red']
    for sprite_name in essential_sprites:
        if sprite_name in original_loader.sprites:
            print(f"   ✓ {sprite_name}: загружен")
        elif sprite_name in original_loader.animations:
            print(f"   ✓ {sprite_name}: анимация загружена ({len(original_loader.animations[sprite_name])} кадров)")
        else:
            print(f"   ✗ {sprite_name}: не найден")
    
    # Отображаем спрайты
    running = True
    clock = pygame.time.Clock()
    
    # Подготавливаем список спрайтов для отображения
    display_sprites = []
    y_offset = 50
    
    # Добавляем одиночные спрайты
    single_sprites = ['stone_blue', 'earth_brown', 'wall_brick_red', 'door_blue']
    for name in single_sprites:
        if name in original_loader.sprites:
            sprite = pygame.transform.scale(original_loader.sprites[name], (32, 32))
            display_sprites.append((name, sprite, (50, y_offset)))
            y_offset += 40
    
    # Добавляем анимации
    animation_sprites = ['hero', 'crystal', 'bubble']
    for name in animation_sprites:
        if name in original_loader.animations:
            frames = original_loader.animations[name]
            if frames:
                sprite = pygame.transform.scale(frames[0], (32, 32))
                display_sprites.append((f"{name}_anim", sprite, (50, y_offset)))
                y_offset += 40
    
    print(f"\n2. Отображение {len(display_sprites)} спрайтов...")
    
    font = pygame.font.Font(None, 24)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((0, 0, 0))
        
        # Отображаем спрайты
        for name, sprite, pos in display_sprites:
            screen.blit(sprite, pos)
            text = font.render(name, True, (255, 255, 255))
            screen.blit(text, (pos[0] + 40, pos[1] + 8))
        
        # Инструкции
        instructions = [
            "ESC - выход",
            f"Загружено спрайтов: {len(original_loader.sprites)}",
            f"Загружено анимаций: {len(original_loader.animations)}"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, (255, 255, 255))
            screen.blit(text, (10, 10 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("\n=== Тест завершен ===")

if __name__ == "__main__":
    test_sprite_loader()