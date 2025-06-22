import pygame

class Player:
    def __init__(self, x, y, sprite_loader):
        self.x = x
        self.y = y
        self.sprite_loader = sprite_loader
        self.tile_size = 64
        self.speed = 200  # пикселей в секунду
        
        # Анимация
        self.animation_timer = 0
        self.animation_frame = 0
        self.animation_speed = 0.25
        
        # Состояние движения
        self.is_moving = False
        self.move_timer = 0
        self.move_duration = 0.2
        self.start_pos = (x, y)
        self.target_pos = (x, y)
        
        # Непрерывное движение
        self.move_repeat_timer = 0
        self.move_repeat_delay = 0.15  # Задержка между повторами движения
        self.current_direction = None
        
        # Игровая статистика
        self.crystals_collected = 0
        self.is_alive = True  # Добавляем это свойство
        
    def update(self, dt, input_handler, level):
        """Обновление игрока"""
        if not self.is_alive:
            return
            
        # Обновляем анимацию
        self.update_animation(dt)
        
        # Убираем этот вызов, так как теперь обновление уровня происходит в game_screen.py
        # level.update_with_player_pos(dt, (self.x, self.y))
        
        # Если не двигаемся, проверяем ввод
        if not self.is_moving:
            self.handle_input(input_handler, level)
        else:
            # Продолжаем движение
            self.update_movement(dt, level)
        
        # Обрабатываем непрерывное движение
        self.handle_continuous_movement(dt, input_handler, level)
    
    def handle_continuous_movement(self, dt, input_handler, level):
        """Обработка непрерывного движения при удержании клавиши"""
        if not input_handler or self.is_moving:
            return
        
        # Определяем текущее направление
        current_dir = None
        if input_handler.is_action_pressed('LEFT'):
            current_dir = 'LEFT'
        elif input_handler.is_action_pressed('RIGHT'):
            current_dir = 'RIGHT'
        elif input_handler.is_action_pressed('UP'):
            current_dir = 'UP'
        elif input_handler.is_action_pressed('DOWN'):
            current_dir = 'DOWN'
        
        if current_dir:
            if self.current_direction == current_dir:
                # Продолжаем движение в том же направлении
                self.move_repeat_timer += dt
                if self.move_repeat_timer >= self.move_repeat_delay:
                    self.move_repeat_timer = 0
                    self.try_move_in_direction(current_dir, level)
            else:
                # Новое направление
                self.current_direction = current_dir
                self.move_repeat_timer = 0
        else:
            # Клавиши не нажаты
            self.current_direction = None
            self.move_repeat_timer = 0
    
    def try_move_in_direction(self, direction, level):
        """Попытка движения в указанном направлении"""
        new_x, new_y = self.x, self.y
        
        if direction == 'LEFT':
            new_x = self.x - self.tile_size
        elif direction == 'RIGHT':
            new_x = self.x + self.tile_size
        elif direction == 'UP':
            new_y = self.y - self.tile_size
        elif direction == 'DOWN':
            new_y = self.y + self.tile_size
        
        if self.can_move_to(new_x, new_y, level):
            self.start_movement(new_x, new_y)
    
    def update_animation(self, dt):
        """Обновление анимации"""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
    
    def handle_input(self, input_handler, level):
        """Обработка ввода"""
        if not input_handler:
            return
            
        new_x, new_y = self.x, self.y
        
        if input_handler.is_action_just_pressed('LEFT'):
            new_x = self.x - self.tile_size
        elif input_handler.is_action_just_pressed('RIGHT'):
            new_x = self.x + self.tile_size
        elif input_handler.is_action_just_pressed('UP'):
            new_y = self.y - self.tile_size
        elif input_handler.is_action_just_pressed('DOWN'):
            new_y = self.y + self.tile_size
        
        # Проверяем, можно ли двигаться
        if (new_x, new_y) != (self.x, self.y):
            if self.can_move_to(new_x, new_y, level):
                self.start_movement(new_x, new_y)
    
    def can_move_to(self, x, y, level):
        """Проверка, можно ли двигаться в указанную позицию"""
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size
        
        # Проверяем границы уровня
        if tile_x < 0 or tile_x >= level.width or tile_y < 0 or tile_y >= level.height:
            return False
        
        # Проверяем тип тайла
        tile_type = level.get_tile(tile_x, tile_y)
        
        # Нельзя проходить через стены и камни-тайлы
        if tile_type in ['brick_wall', 'stone']:
            return False
        
        # Проверяем объекты в этой позиции
        obj = level.get_object_at(tile_x, tile_y)
        if obj and obj.active:
            # Можно проходить через кристаллы и червяков (собираем их)
            if obj.object_type in ['crystal', 'worm']:
                return True
            # Нельзя проходить через камни и пузыри
            elif obj.object_type in ['stone', 'bubble']:
                return False
        
        # Можно ходить по пустым местам и земле
        return True
    
    def try_push_object(self, obj_tile_x, obj_tile_y, level):
        """Попытка толкнуть объект"""
        # Определяем направление толчка
        player_tile_x = self.x // self.tile_size
        player_tile_y = self.y // self.tile_size
        
        push_dir_x = obj_tile_x - player_tile_x
        push_dir_y = obj_tile_y - player_tile_y
        
        # Целевая позиция для объекта
        target_x = obj_tile_x + push_dir_x
        target_y = obj_tile_y + push_dir_y
        
        # Проверяем, можно ли толкнуть
        if level.can_push_object(obj_tile_x, obj_tile_y, target_x, target_y):
            # Толкаем объект
            level.push_object(obj_tile_x, obj_tile_y, target_x, target_y)
            return True
        
        return False
    
    def start_movement(self, target_x, target_y):
        """Начало движения к цели"""
        self.is_moving = True
        self.move_timer = 0
        self.start_pos = (self.x, self.y)
        self.target_pos = (target_x, target_y)
    
    def update_movement(self, dt, level):
        """Обновление движения"""
        self.move_timer += dt
        progress = min(1.0, self.move_timer / self.move_duration)
        
        # Интерполяция позиции
        start_x, start_y = self.start_pos
        target_x, target_y = self.target_pos
        
        self.x = start_x + (target_x - start_x) * progress
        self.y = start_y + (target_y - start_y) * progress
        
        # Завершаем движение
        if progress >= 1.0:
            self.x, self.y = self.target_pos
            self.is_moving = False
            
            # Обрабатываем взаимодействие с тайлом
            self.handle_tile_interaction(level)
    
    def handle_tile_interaction(self, level):
        """Обработка взаимодействия с тайлом"""
        tile_x = self.x // self.tile_size
        tile_y = self.y // self.tile_size
        
        tile_type = level.get_tile(tile_x, tile_y)
        
        # Копаем землю
        if tile_type == 'earth':
            level.set_tile(tile_x, tile_y, 'empty')
        
        # Собираем объекты (кристаллы и червяков)
        obj = level.get_object_at(tile_x, tile_y)
        if obj and obj.active and obj.object_type in ['crystal', 'worm']:
            if obj.object_type == 'crystal':
                self.crystals_collected += 1
                print(f"Crystal collected! Total: {self.crystals_collected}")
            elif obj.object_type == 'worm':
                print("Worm collected!")
        
            obj.active = False
    
    def get_current_sprite(self):
        """Получение текущего спрайта для анимации"""
        hero_sprites = self.sprite_loader.get_sprite('hero')
        if hero_sprites and len(hero_sprites) > 0:
            return hero_sprites[self.animation_frame]
        return None
    
    def render(self, screen, camera_x, camera_y):
        """Отрисовка игрока"""
        # Вычисляем позицию на экране с учетом камеры - приводим к целым числам
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Получаем спрайт
        sprite = self.get_current_sprite()
        
        if sprite:
            screen.blit(sprite, (screen_x, screen_y))
        else:
            # Заглушка если спрайт не загружен
            pygame.draw.rect(screen, (0, 255, 0), 
                           (screen_x, screen_y, self.tile_size, self.tile_size))
            pygame.draw.rect(screen, (255, 255, 255), 
                           (screen_x, screen_y, self.tile_size, self.tile_size), 2)
