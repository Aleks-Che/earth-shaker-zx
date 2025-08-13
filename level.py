import pygame
import random
from game_object import GameObject
from level_data import LevelData

class Level:
    def __init__(self, sprite_loader, game_settings=None, level_number=1):
        self.sprite_loader = sprite_loader  # Исправляем: используем sprite_loader везде
        self.game_settings = game_settings
        self.tile_size = 64
        self.level_number = level_number
        
        # Загружаем данные уровня
        level_data = LevelData.get_level(level_number)
        if level_data:
            print(f"Загружаем уровень {level_number} из данных")
            self.width = level_data['width']
            self.height = level_data['height']
            self.tiles = level_data['tiles']
            self.player_start = level_data['player_start']
            self.total_crystals_in_data = level_data['crystals_total']
        else:
            print(f"Данные для уровня {level_number} не найдены, создаем случайный")
            self.width = 15
            self.height = 12
            self.tiles = self.create_random_level()
            self.player_start = (1, 1)
            self.total_crystals_in_data = 8
        
        # Игровые объекты (извлекаем из карты)
        self.game_objects = []
        self.extract_objects_from_tiles()
        
        # Сохраняем общее количество кристаллов
        self.total_crystals = self.get_total_crystals()
        
        # Физика - замедляем падение
        self.gravity_timer = 0
        self.gravity_interval = 0.2  # Интервал гравитации
        
        print(f"Уровень {level_number} создан: {self.width}x{self.height}, кристаллов: {self.total_crystals}")
    
    def extract_objects_from_tiles(self):
        """Извлечение объектов из тайлов карты"""
        print("Извлекаем объекты из карты...")
        
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.tiles[y][x]
                
                # Если это объект, создаем его и заменяем тайл на пустой
                if tile_type == 'crystal':
                    crystal = GameObject(x * self.tile_size, y * self.tile_size, 
                                       self.sprite_loader, 'crystal', self.game_settings)
                    crystal.object_type = 'crystal'
                    crystal.can_fall = True
                    crystal.fall_state = 'stable'
                    self.game_objects.append(crystal)
                    self.tiles[y][x] = 'empty'  # Заменяем на пустое место
                    
                elif tile_type == 'worm':
                    worm = GameObject(x * self.tile_size, y * self.tile_size, 
                                    self.sprite_loader, 'worm', self.game_settings)
                    worm.object_type = 'worm'
                    worm.can_fall = True
                    worm.fall_state = 'stable'
                    self.game_objects.append(worm)
                    self.tiles[y][x] = 'empty'
                    
                elif tile_type == 'bubble':
                    bubble = GameObject(x * self.tile_size, y * self.tile_size, 
                                      self.sprite_loader, 'bubble', self.game_settings)
                    bubble.object_type = 'bubble'
                    bubble.can_fall = False  # Пузыри не падают сами по себе
                    bubble.fall_state = 'stable'
                    self.game_objects.append(bubble)
                    self.tiles[y][x] = 'empty'
                
                elif tile_type == 'player':
                    # Игрок не создается как объект, просто запоминаем позицию
                    self.player_start = (x, y)
                    self.tiles[y][x] = 'empty'
        
        print(f"Извлечено объектов: {len(self.game_objects)}")
    
    def create_random_level(self):
        """Создание случайного уровня (если нет данных)"""
        tiles = []
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Границы уровня - кирпичные стены
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append('wall_brick_red')
                # Стартовая зона (левый верхний угол) - пустая
                elif x <= 2 and y <= 2:
                    row.append('empty')
                # Выход в правом нижнем углу
                elif x == self.width - 2 and y == self.height - 2:
                    row.append('door_yellow')
                else:
                    # Случайное заполнение
                    rand = random.random()
                    if rand < 0.3:
                        row.append('earth_brown')
                    elif rand < 0.35:
                        row.append('stone_gray')
                    else:
                        row.append('empty')
            tiles.append(row)
        
        return tiles
    
    def get_tile(self, x, y):
        """Получение типа тайла"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return 'wall_brick_red'  # За границами - стена
    
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
        return self.player_start
    
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
    
    def get_object_fall_direction(self, obj, player_occupied_tiles, player_is_moving):
        """Определение направления падения объекта"""
        if not obj.can_fall or obj.is_moving:
            return None
        
        obj_tile_x, obj_tile_y = obj.get_tile_pos()
        
        # Проверяем прямое падение вниз
        target_tile = (obj_tile_x, obj_tile_y + 1)
        if self.can_object_move_to(obj_tile_x, obj_tile_y, target_tile[0], target_tile[1]):
            # Проверяем, не заблокирован ли путь игроком
            if target_tile in player_occupied_tiles:
                return None
            return 'down'
        
        # Проверяем скольжение (только для камней и кристаллов)
        if obj.object_type in ['stone', 'crystal']:
            # Что находится под объектом
            below_tile = self.get_tile(obj_tile_x, obj_tile_y + 1)
            below_obj = self.get_object_at(obj_tile_x, obj_tile_y + 1)
            
            # Объект может скользить с твердых поверхностей
            can_slide = (below_tile.startswith('stone_') or below_tile.startswith('wall_') or 
                        (below_obj and below_obj.object_type in ['stone', 'crystal']))
            
            if can_slide:
                # Приоритет скольжения: сначала вправо, потом влево
                for direction, dx in [('right', 1), ('left', -1)]:
                    new_x = obj_tile_x + dx
                    side_tile = (new_x, obj_tile_y)
                    fall_tile = (new_x, obj_tile_y + 1)
                    
                    # Проверяем, можно ли скользнуть в сторону и вниз
                    if (self.can_object_move_to(obj_tile_x, obj_tile_y, new_x, obj_tile_y) and
                        self.can_object_move_to(new_x, obj_tile_y, new_x, obj_tile_y + 1)):
                        
                        # Проверяем, не заблокированы ли пути игроком
                        if side_tile not in player_occupied_tiles and fall_tile not in player_occupied_tiles:
                            return direction
        
        return None
    
    def apply_gravity(self, player_occupied_tiles, player_is_moving):
        """Применение гравитации к объектам"""
        for obj in self.game_objects:
            if not obj.active or obj.is_moving:
                continue
            
            obj_tile = obj.get_tile_pos()
            
            # Если игрок движется и объект находится в зоне его движения, 
            # не применяем гравитацию к этому объекту
            if player_is_moving and obj_tile in player_occupied_tiles:
                continue
            
            direction = self.get_object_fall_direction(obj, player_occupied_tiles, player_is_moving)
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
    
    def update(self, dt, player_occupied_tiles=None, player_is_moving=False):
        """Обновление уровня"""
        # Обновляем анимацию объектов
        for obj in self.game_objects:
            if obj.active:
                obj.update(dt)
        
        # Применяем гравитацию только если есть информация об игроке
        self.gravity_timer += dt
        if self.gravity_timer >= self.gravity_interval:
            self.gravity_timer = 0
            if player_occupied_tiles is not None:
                self.apply_gravity(player_occupied_tiles, player_is_moving)
    
    def render(self, screen, camera_x, camera_y):
        """Отрисовка уровня"""
        # Отрисовываем тайлы
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.tiles[y][x]
                sprite = self.get_tile_sprite(tile_type)
                
                screen_x = x * self.tile_size - camera_x
                screen_y = y * self.tile_size - camera_y
                
                if sprite:
                    # Масштабируем спрайт до размера тайла
                    if sprite.get_width() != self.tile_size:
                        sprite = pygame.transform.scale(sprite, (self.tile_size, self.tile_size))
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
    
    def get_tile_sprite(self, tile_type):
        """Получение спрайта для тайла"""
        if tile_type == 'empty':
            return None  # Пустые тайлы не рисуем
        
        # Пытаемся получить спрайт напрямую
        sprite = self.sprite_loader.get_sprite(tile_type)
        if sprite:
            return sprite
        
        # Если не найден, пытаемся найти по частям имени
        if tile_type.startswith('earth_'):
            # Пытаемся найти любую землю
            for color in ['brown', 'blue', 'red', 'green', 'gray']:
                alt_sprite = self.sprite_loader.get_sprite(f'earth_{color}')
                if alt_sprite:
                    return alt_sprite
            # Если не найдено, используем базовую землю
            return self.sprite_loader.get_sprite('earth')
        
        elif tile_type.startswith('stone_'):
            # Пытаемся найти любой камень
            for color in ['gray', 'blue', 'red', 'green']:
                alt_sprite = self.sprite_loader.get_sprite(f'stone_{color}')
                if alt_sprite:
                    return alt_sprite
            # Если не найдено, используем базовый камень
            return self.sprite_loader.get_sprite('stone')
        
        elif tile_type.startswith('wall_'):
            # Пытаемся найти любую стену
            for wall_type in ['brick_red', 'brick_purple', 'concrete_gray']:
                alt_sprite = self.sprite_loader.get_sprite(f'wall_{wall_type}')
                if alt_sprite:
                    return alt_sprite
            # Если не найдено, используем базовую стену
            return self.sprite_loader.get_sprite('brick_wall')
        
        elif tile_type.startswith('door_'):
            # Пытаемся найти любую дверь
            for color in ['yellow', 'blue', 'red', 'green']:
                alt_sprite = self.sprite_loader.get_sprite(f'door_{color}')
                if alt_sprite:
                    return alt_sprite
            # Если не найдено, используем базовый выход
            return self.sprite_loader.get_sprite('exit')
        
        print(f"Спрайт не найден для тайла: {tile_type}")
        return None
    
    def get_tile_color(self, tile_type):
        """Получение цвета тайла для заглушки"""
        colors = {
            'empty': (0, 0, 0),
            'earth_brown': (139, 69, 19),
            'earth_blue': (0, 0, 139),
            'earth_red': (139, 0, 0),
            'earth_green': (0, 139, 0),
            'earth_gray': (105, 105, 105),
            'stone_gray': (128, 128, 128),
            'stone_blue': (0, 0, 255),
            'stone_red': (255, 0, 0),
            'stone_green': (0, 255, 0),
            'wall_brick_red': (165, 42, 42),
            'wall_brick_purple': (128, 0, 128),
            'wall_concrete_gray': (128, 128, 128),
            'door_yellow': (255, 215, 0),
            'door_blue': (0, 0, 255),
            'door_red': (255, 0, 0),
            'door_green': (0, 255, 0),
            'fire': (255, 100, 0),
        }
        
        # Если точный цвет не найден, пытаемся найти по префиксу
        if tile_type not in colors:
            for key in colors:
                if tile_type.startswith(key.split('_')[0]):
                    return colors[key]
        
        return colors.get(tile_type, (255, 0, 255))  # Пурпурный для неизвестных
    
    def can_player_move_to(self, tile_x, tile_y):
        """Проверка, может ли игрок переместиться в указанную позицию"""
        # Проверяем границы
        if tile_x < 0 or tile_x >= self.width or tile_y < 0 or tile_y >= self.height:
            return False
        
        # Проверяем тип тайла
        tile_type = self.get_tile(tile_x, tile_y)
        
        # Можно ходить по пустым местам и земле
        if tile_type == 'empty' or tile_type.startswith('earth_'):
            # Проверяем, нет ли блокирующих объектов
            obj = self.get_object_at(tile_x, tile_y)
            if obj and obj.active and obj.object_type in ['stone', 'bubble']:
                return False  # Камни и пузыри блокируют движение
            return True
        
        # Можно войти в выход (дверь)
        if tile_type.startswith('door_'):
            return True
        
        # Нельзя проходить через стены и камни-тайлы
        return False
