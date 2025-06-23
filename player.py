import pygame

class Player:
    def __init__(self, x, y, sprite_loader, game_settings):
        self.x = x
        self.y = y
        self.sprite_loader = sprite_loader
        self.game_settings = game_settings
        self.tile_size = 64
        self.speed = 200  # пикселей в секунду
        
        # Анимация
        self.animation_timer = 0
        self.animation_frame = 0
        self.animation_speed = 0.25  # смена кадра каждые 0.25 секунды
        
        # Состояние движения
        self.is_moving = False
        self.move_timer = 0
        self.move_duration = 0.2  # время на один шаг
        self.start_pos = (x, y)
        self.target_pos = (x, y)
        
        # Для поддержки удержания клавиш
        self.key_repeat_timer = 0
        self.key_repeat_delay = 0.15  # задержка между повторами при удержании
        
        # Игровая статистика
        self.crystals_collected = 0
        
    def update(self, dt, input_handler, level):
        """Обновление игрока"""
        # Обновляем анимацию
        self.update_animation(dt)
        
        # Если не двигаемся, проверяем ввод
        if not self.is_moving:
            result = self.handle_input(input_handler, level, dt)
            if result:
                return result
        else:
            # Продолжаем движение (только если включена плавная анимация)
            if self.game_settings.smooth_movement:
                result = self.update_movement(dt, level)
                if result:
                    return result
            else:
                # При выключенной анимации движение уже завершено в start_movement
                pass
        
        return None
    
    def update_animation(self, dt):
        """Обновление анимации"""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
    
    def handle_input(self, input_handler, level, dt):
        """Обработка ввода с поддержкой удержания клавиш"""
        if not input_handler:
            return
        
        # Проверяем нажатие клавиш (для первого движения)
        direction = None
        if input_handler.is_action_just_pressed('LEFT'):
            direction = 'LEFT'
            self.key_repeat_timer = 0
        elif input_handler.is_action_just_pressed('RIGHT'):
            direction = 'RIGHT'
            self.key_repeat_timer = 0
        elif input_handler.is_action_just_pressed('UP'):
            direction = 'UP'
            self.key_repeat_timer = 0
        elif input_handler.is_action_just_pressed('DOWN'):
            direction = 'DOWN'
            self.key_repeat_timer = 0
        
        # Если клавиша не была только что нажата, проверяем удержание
        if direction is None:
            self.key_repeat_timer += dt
            if self.key_repeat_timer >= self.key_repeat_delay:
                self.key_repeat_timer = 0
                
                if input_handler.is_action_pressed('LEFT'):
                    direction = 'LEFT'
                elif input_handler.is_action_pressed('RIGHT'):
                    direction = 'RIGHT'
                elif input_handler.is_action_pressed('UP'):
                    direction = 'UP'
                elif input_handler.is_action_pressed('DOWN'):
                    direction = 'DOWN'
        
        # Выполняем движение если есть направление
        if direction:
            self.try_move(direction, level)
    
    def try_move(self, direction, level):
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
        
        # Проверяем, можно ли двигаться
        if self.can_move_to(new_x, new_y, level):
            self.start_movement(new_x, new_y, level)
    
    def can_move_to(self, x, y, level):
        """Проверка, можно ли двигаться в указанную позицию"""
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size
        
        # Используем метод уровня для проверки
        return level.can_player_move_to(tile_x, tile_y)
    
    def start_movement(self, target_x, target_y, level):
        """Начало движения к цели"""
        self.is_moving = True
        self.move_timer = 0
        self.start_pos = (self.x, self.y)
        self.target_pos = (target_x, target_y)
        
        # Если плавная анимация выключена, сразу перемещаемся и обрабатываем взаимодействие
        if not self.game_settings.smooth_movement:
            self.x, self.y = self.target_pos
            self.is_moving = False
            result = self.handle_tile_interaction(level)
            return result
        
        return None
    
    def update_movement(self, dt, level):
        """Обновление движения (только для плавной анимации)"""
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
        
        # Проверяем выход
        if tile_type == 'exit':
            # Можно войти в выход только если собраны все кристаллы
            if level.get_crystals_count() == 0:
                print("Level completed!")
                return "LEVEL_COMPLETE"
            else:
                print(f"Collect all crystals first! {level.get_crystals_count()} left")
        
        # Собираем кристаллы и других существ
        # Важно: собираем объекты только когда игрок полностью переместился
        if not self.is_moving:
            collected = level.collect_object(tile_x, tile_y)
            if collected:
                if collected == 'crystal':
                    self.crystals_collected += 1
                    print(f"Crystals collected: {self.crystals_collected}")
                    print(f"Crystals left: {level.get_crystals_count()}")
                elif collected == 'worm':
                    print("Worm collected!")
    
    def get_current_sprite(self):
        """Получение текущего спрайта для анимации"""
        hero_sprites = self.sprite_loader.get_sprite('hero')
        if hero_sprites and len(hero_sprites) > 0:
            return hero_sprites[self.animation_frame]
        return None
    
    def render(self, screen, camera_x, camera_y):
        """Отрисовка игрока"""
        # Вычисляем позицию на экране с учетом камеры
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
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

    def get_current_tile_pos(self):
        """Получение текущей позиции в тайлах"""
        return (int(self.x // self.tile_size), int(self.y // self.tile_size))

    def get_target_tile_pos(self):
        """Получение целевой позиции в тайлах (куда движется игрок)"""
        if self.is_moving:
            return (int(self.target_pos[0] // self.tile_size), int(self.target_pos[1] // self.tile_size))
        else:
            return self.get_current_tile_pos()

    def get_start_tile_pos(self):
        """Получение стартовой позиции в тайлах (откуда движется игрок)"""
        if self.is_moving:
            return (int(self.start_pos[0] // self.tile_size), int(self.start_pos[1] // self.tile_size))
        else:
            return self.get_current_tile_pos()

    def get_occupied_tiles(self):
        """Получение всех тайлов, которые занимает или будет занимать игрок"""
        tiles = set()
        
        # Добавляем текущую позицию
        current_tile = self.get_current_tile_pos()
        tiles.add(current_tile)
        
        # Если движется, добавляем стартовую и целевую позицию
        if self.is_moving:
            start_tile = self.get_start_tile_pos()
            target_tile = self.get_target_tile_pos()
            tiles.add(start_tile)
            tiles.add(target_tile)
        
        return tiles