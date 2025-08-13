import pygame
from animated_sprite import AnimatedSprite

class Player:
    def __init__(self, x, y, sprite_loader, game_settings):
        self.x = x
        self.y = y
        self.sprite_loader = sprite_loader  # Возвращаем обратно sprite_loader
        self.game_settings = game_settings
        
        # Размер тайла
        self.tile_size = 64
        
        # Анимация
        hero_sprites = sprite_loader.get_animation('hero')
        if hero_sprites:
            self.sprite = AnimatedSprite(hero_sprites, 0.2)
        else:
            # Создаем заглушку если анимация не найдена
            placeholder = pygame.Surface((self.tile_size, self.tile_size))
            placeholder.fill((0, 255, 0))
            self.sprite = AnimatedSprite([placeholder], 0.2)
        
        # Движение
        self.is_moving = False
        self.move_start_x = x
        self.move_start_y = y
        self.move_target_x = x
        self.move_target_y = y
        self.move_progress = 0.0
        self.move_speed = 1.0 / 0.15  # Движение за 0.15 секунды
        
        # Статистика
        self.crystals_collected = 0
        
        # Состояние
        self.alive = True
        
    def update(self, dt, input_handler, level):
        """Обновление игрока"""
        # Обновляем анимацию
        self.sprite.update(dt)
        
        # Если игрок мертв, не обрабатываем движение
        if not self.alive:
            return None
        
        # Обрабатываем движение
        if self.is_moving:
            self.update_movement(dt)
        else:
            # Обрабатываем ввод только если не движемся
            if input_handler:
                self.handle_input(input_handler, level)
        
        # Проверяем завершение уровня
        if level.get_crystals_count() == 0:
            return "LEVEL_COMPLETE"
        
        return None
    
    def handle_input(self, input_handler, level):
        """Обработка пользовательского ввода"""
        dx, dy = 0, 0
        
        # Получаем направление движения
        if input_handler.is_key_pressed(pygame.K_LEFT) or input_handler.is_key_pressed(pygame.K_a):
            dx = -1
        elif input_handler.is_key_pressed(pygame.K_RIGHT) or input_handler.is_key_pressed(pygame.K_d):
            dx = 1
        elif input_handler.is_key_pressed(pygame.K_UP) or input_handler.is_key_pressed(pygame.K_w):
            dy = -1
        elif input_handler.is_key_pressed(pygame.K_DOWN) or input_handler.is_key_pressed(pygame.K_s):
            dy = 1
        
        # Если есть движение, пытаемся переместиться
        if dx != 0 or dy != 0:
            self.try_move(dx, dy, level)
    
    def try_move(self, dx, dy, level):
        """Попытка движения в указанном направлении"""
        current_tile_x = self.x // self.tile_size
        current_tile_y = self.y // self.tile_size
        
        new_tile_x = current_tile_x + dx
        new_tile_y = current_tile_y + dy
        
        # Проверяем, можно ли двигаться
        if level.can_player_move_to(new_tile_x, new_tile_y):
            # Копаем землю если она есть
            tile_type = level.get_tile(new_tile_x, new_tile_y)
            if tile_type and tile_type.startswith('earth_'):
                level.set_tile(new_tile_x, new_tile_y, 'empty')
            
            # Собираем объекты
            collected = level.collect_object(new_tile_x, new_tile_y)
            if collected == 'crystal':
                self.crystals_collected += 1
                print(f"Собран кристалл! Всего: {self.crystals_collected}")
            elif collected == 'worm':
                print("Собран червяк!")
            
            # Начинаем движение
            self.start_movement(new_tile_x * self.tile_size, new_tile_y * self.tile_size)
    
    def start_movement(self, target_x, target_y):
        """Начало плавного движения"""
        if self.game_settings.smooth_movement:
            self.is_moving = True
            self.move_start_x = self.x
            self.move_start_y = self.y
            self.move_target_x = target_x
            self.move_target_y = target_y
            self.move_progress = 0.0
        else:
            # Мгновенное движение
            self.x = target_x
            self.y = target_y
    
    def update_movement(self, dt):
        """Обновление плавного движения"""
        if not self.is_moving:
            return
        
        self.move_progress += self.move_speed * dt
        
        if self.move_progress >= 1.0:
            # Движение завершено
            self.move_progress = 1.0
            self.x = self.move_target_x
            self.y = self.move_target_y
            self.is_moving = False
        else:
            # Интерполяция позиции
            self.x = self.move_start_x + (self.move_target_x - self.move_start_x) * self.move_progress
            self.y = self.move_start_y + (self.move_target_y - self.move_start_y) * self.move_progress
    
    def get_occupied_tiles(self):
        """Получение списка тайлов, занимаемых игроком"""
        current_tile = (self.x // self.tile_size, self.y // self.tile_size)
        
        if self.is_moving:
            # Если движемся, возвращаем и текущий, и целевой тайл
            target_tile = (self.move_target_x // self.tile_size, self.move_target_y // self.tile_size)
            return [current_tile, target_tile]
        else:
            return [current_tile]
    
    def kill(self):
        """Убить игрока"""
        self.alive = False
        # Можно добавить анимацию смерти
        dead_sprite = self.sprite_loader.get_sprite('hero_dead')
        if dead_sprite:
            self.sprite = AnimatedSprite([dead_sprite], 1.0)
    
    def render(self, screen, camera_x, camera_y):
        """Отрисовка игрока"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        current_sprite = self.sprite.get_current_sprite()
        if current_sprite:
            # Масштабируем спрайт если нужно
            if current_sprite.get_width() != self.tile_size:
                current_sprite = pygame.transform.scale(current_sprite, (self.tile_size, self.tile_size))
            screen.blit(current_sprite, (screen_x, screen_y))
        else:
            # Заглушка если спрайт не найден
            pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y, self.tile_size, self.tile_size))