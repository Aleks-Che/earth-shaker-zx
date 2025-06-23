import pygame
import random
from game_object import GameObject

class Level:
    def __init__(self, sprite_loader, game_settings=None, level_number=1):
        self.sprite_loader = sprite_loader
        self.game_settings = game_settings
        self.tile_size = 64
        self.width = 15
        self.height = 12
        self.level_number = level_number
        
        # Создаем карту уровня
        self.tiles = self.create_level()
        
        # Игровые объекты (кристаллы, камни, червяки, пузыри)
        self.game_objects = []
        self.create_objects()
        
        # Сохраняем общее количество кристаллов
        self.total_crystals = self.get_total_crystals()
        
        # Физика - замедляем падение
        self.gravity_timer = 0
        self.gravity_interval = 0.2  # Интервал гравитации
    
    def create_level(self):
        """Создание базового уровня"""
        tiles = []
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Границы уровня - кирпичные стены
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append('brick_wall')
                # Стартовая зона (левый верхний угол) - пустая
                elif x <= 2 and y <= 2:
                    row.append('empty')
                # Выход в правом нижнем углу
                elif x == self.width - 2 and y == self.height - 2:
                    row.append('exit')
                else:
                    # Случайное заполнение
                    rand = random.random()
                    if rand < 0.3:
                        row.append('earth')
                    elif rand < 0.35:  # Уменьшили количество камней-тайлов
                        row.append('stone')
                    else:
                        row.append('empty')
            tiles.append(row)
        
        return tiles
    
    def create_objects(self):
        """Создание всех объектов на уровне"""
        self.create_crystals()
        self.create_stones()
        self.create_worms()
        self.create_bubbles()
    
    def create_crystals(self):
        """Создание кристаллов на уровне"""
        crystal_count = 8
        placed = 0
        attempts = 0
        max_attempts = 100
        
        while placed < crystal_count and attempts < max_attempts:
            x = random.randint(3, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            if self.tiles[y][x] == 'empty' and not self.get_object_at(x, y):
                crystal = GameObject(x * self.tile_size, y * self.tile_size, 
                                   self.sprite_loader, 'crystal', self.game_settings)
                crystal.object_type = 'crystal'
                crystal.can_fall = True
                crystal.fall_state = 'stable'
                self.game_objects.append(crystal)
                placed += 1
            
            attempts += 1

    def create_stones(self):
        """Создание камней на уровне"""
        stone_count = 5
        placed = 0
        attempts = 0
        max_attempts = 100
        
        while placed < stone_count and attempts < max_attempts:
            x = random.randint(3, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            if self.tiles[y][x] == 'empty' and not self.get_object_at(x, y):
                # Создаем камень как объект, а не тайл
                stone = GameObject(x * self.tile_size, y * self.tile_size, 
                                 self.sprite_loader, 'stone', self.game_settings)
                stone.object_type = 'stone'
                stone.can_fall = True
                stone.fall_state = 'stable'
                self.game_objects.append(stone)
                placed += 1
            
            attempts += 1

    def create_worms(self):
        """Создание червяков на уровне"""
        worm_count = 3
        placed = 0
        attempts = 0
        max_attempts = 100
        
        while placed < worm_count and attempts < max_attempts:
            x = random.randint(3, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            if self.tiles[y][x] == 'empty' and not self.get_object_at(x, y):
                worm = GameObject(x * self.tile_size, y * self.tile_size, 
                                self.sprite_loader, 'worm', self.game_settings)
                worm.object_type = 'worm'
                worm.can_fall = True
                worm.fall_state = 'stable'
                self.game_objects.append(worm)
                placed += 1
            
            attempts += 1

    def create_bubbles(self):
        """Создание пузырей на уровне"""
        bubble_count = 2
        placed = 0
        attempts = 0
        max_attempts = 100
        
        while placed < bubble_count and attempts < max_attempts:
            x = random.randint(3, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            if self.tiles[y][x] == 'empty' and not self.get_object_at(x, y):
                bubble = GameObject(x * self.tile_size, y * self.tile_size, 
                                  self.sprite_loader, 'bubble', self.game_settings)
                bubble.object_type = 'bubble'
                bubble.can_fall = False  # Пузыри не падают сами по себе
                bubble.fall_state = 'stable'
                self.game_objects.append(bubble)
                placed += 1
            
            attempts += 1
    
    def get_tile(self, x, y):
        """Получение типа тайла"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return 'brick_wall'  # За границами - стена
    
    def set_tile(self, x, y, tile_type):
        """Установка типа тайла"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile_type
    
    def get_object_at(self, tile_x, tile_y):
        """Получение объекта в указанной позиции (в тайлах)"""
        for obj in self.game_objects:
            if obj.active:
                obj_tile_x, obj_tile_y = obj.get_tile_pos()
                if obj_tile_x == tile_x and obj_tile_y == tile_y:
                    return obj
        return None
    
    def collect_object(self, tile_x, tile_y):
        """Сбор объекта в указанной позиции"""
        obj = self.get_object_at(tile_x, tile_y)
        if obj and obj.active:
            if obj.object_type in ['crystal', 'worm']:
                obj.active = False
                return obj.object_type
        return None
    
    def get_crystals_count(self):
        """Получение количества оставшихся кристаллов"""
        return len([obj for obj in self.game_objects 
                   if obj.active and obj.object_type == 'crystal'])
    
    def get_player_start_position(self):
        """Получение стартовой позиции игрока"""
        # Возвращаем стандартную стартовую позицию (в тайлах)
        return (1, 1)

    def get_total_crystals(self):
        """Получение общего количества кристаллов на уровне"""
        return len([obj for obj in self.game_objects 
                   if obj.object_type == 'crystal'])
    
    def can_object_move_to(self, from_tile_x, from_tile_y, to_tile_x, to_tile_y):
        """Проверка, может ли объект переместиться в указанную позицию"""
        # Проверяем границы
        if to_tile_x < 0 or to_tile_x >= self.width or to_tile_y < 0 or to_tile_y >= self.height:
            return False
        
        # Проверяем тип тайла
        tile_type = self.get_tile(to_tile_x, to_tile_y)
        if tile_type != 'empty':
            return False
        
        # Проверяем, нет ли другого объекта
        target_obj = self.get_object_at(to_tile_x, to_tile_y)
        if target_obj and target_obj.active:
            return False
        
        return True
    
    def get_object_fall_direction(self, obj, player_tile_x, player_tile_y):
        """Определение направления падения объекта"""
        if not obj.can_fall or obj.is_moving:
            return None
        
        obj_tile_x, obj_tile_y = obj.get_tile_pos()
        
        # Проверяем прямое падение вниз
        if self.can_object_move_to(obj_tile_x, obj_tile_y, obj_tile_x, obj_tile_y + 1):
            # Проверяем, не заблокирован ли путь игроком
            if obj_tile_x == player_tile_x and obj_tile_y + 1 == player_tile_y:
                return None
            return 'down'
        
        # Проверяем скольжение (только для камней и кристаллов)
        if obj.object_type in ['stone', 'crystal']:
            # Что находится под объектом
            below_tile = self.get_tile(obj_tile_x, obj_tile_y + 1)
            below_obj = self.get_object_at(obj_tile_x, obj_tile_y + 1)
            
            # Объект может скользить с твердых поверхностей
            can_slide = (below_tile in ['stone', 'brick_wall'] or 
                        (below_obj and below_obj.object_type in ['stone', 'crystal']))
            
            if can_slide:
                # Приоритет скольжения: сначала вправо, потом влево
                for direction, dx in [('right', 1), ('left', -1)]:
                    new_x = obj_tile_x + dx
                    # Проверяем, можно ли скользнуть в сторону и вниз
                    if (self.can_object_move_to(obj_tile_x, obj_tile_y, new_x, obj_tile_y) and
                        self.can_object_move_to(new_x, obj_tile_y, new_x, obj_tile_y + 1)):
                        # Проверяем, не заблокирован ли путь игроком
                        if not ((new_x == player_tile_x and obj_tile_y == player_tile_y) or
                               (new_x == player_tile_x and obj_tile_y + 1 == player_tile_y)):
                            return direction
        
        return None
    
    def apply_gravity(self, player_tile_x, player_tile_y):
        """Применение гравитации к объектам"""
        for obj in self.game_objects:
            if not obj.active or obj.is_moving:
                continue
            
            direction = self.get_object_fall_direction(obj, player_tile_x, player_tile_y)
            if direction:
                target_x = obj.x
                target_y = obj.y
                
                if direction == 'down':
                    target_y += self.tile_size
                elif direction == 'left':
                    target_x -= self.tile_size
                elif direction == 'right':
                    target_x += self.tile_size
                
                # Запускаем движение
                if obj.start_movement(target_x, target_y):
                    # Устанавливаем состояние падения
                    if hasattr(obj, 'fall_state'):
                        if direction in ['left', 'right']:
                            obj.fall_state = 'sliding'
                        else:
                            obj.fall_state = 'falling'
    
    def update(self, dt, player_tile_x=None, player_tile_y=None):
        """Обновление уровня"""
        # Обновляем анимацию объектов
        for obj in self.game_objects:
            if obj.active:
                obj.update(dt)
        
        # Применяем гравитацию
        self.gravity_timer += dt
        if self.gravity_timer >= self.gravity_interval:
            self.gravity_timer = 0
            if player_tile_x is not None and player_tile_y is not None:
                self.apply_gravity(player_tile_x, player_tile_y)
    
    def render(self, screen, camera_x, camera_y):
        """Отрисовка уровня"""
        # Отрисовываем тайлы
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.tiles[y][x]
                sprite = self.sprite_loader.get_sprite(tile_type)
                
                screen_x = x * self.tile_size - camera_x
                screen_y = y * self.tile_size - camera_y
                
                if sprite:
                    screen.blit(sprite, (screen_x, screen_y))
                else:
                    # Заглушка если спрайт не найден
                    color = self.get_tile_color(tile_type)
                    pygame.draw.rect(screen, color,
                                   (screen_x, screen_y, self.tile_size, self.tile_size))
        
        # Отрисовываем игровые объекты
        for obj in self.game_objects:
            if obj.active:
                obj.render(screen, camera_x, camera_y)
    
    def get_tile_color(self, tile_type):
        """Получение цвета тайла для заглушки"""
        colors = {
            'empty': (0, 0, 0),
            'earth': (139, 69, 19),
            'brick_wall': (165, 42, 42),
            'stone': (128, 128, 128)
        }
        return colors.get(tile_type, (255, 0, 255))
    
    def can_player_move_to(self, tile_x, tile_y):
        """Проверка, может ли игрок переместиться в указанную позицию"""
        # Проверяем границы
        if tile_x < 0 or tile_x >= self.width or tile_y < 0 or tile_y >= self.height:
            return False
        
        # Проверяем тип тайла
        tile_type = self.get_tile(tile_x, tile_y)
        
        # Можно ходить по пустым местам и земле
        if tile_type in ['empty', 'earth']:
            # Проверяем, нет ли блокирующих объектов
            obj = self.get_object_at(tile_x, tile_y)
            if obj and obj.active and obj.object_type in ['stone', 'bubble']:
                return False  # Камни и пузыри блокируют движение
            return True
        
        # Можно войти в выход (дверь)
        if tile_type == 'exit':
            return True
        
        # Нельзя проходить через стены и камни-тайлы
        return False
