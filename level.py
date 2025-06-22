import pygame
import random
from game_object import GameObject

class Level:
    def __init__(self, sprite_loader, level_number=1):
        self.sprite_loader = sprite_loader
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
                else:
                    # Случайное заполнение
                    rand = random.random()
                    if rand < 0.3:
                        row.append('earth')
                    elif rand < 0.4:
                        row.append('stone')
                    else:
                        row.append('empty')
            tiles.append(row)
        
        return tiles
    
    def create_objects(self):
        """Создание объектов на уровне"""
        # Создаем кристаллы
        self.create_crystals()
        # Создаем камни
        self.create_stones()
        # Создаем червяков
        self.create_worms()
        # Создаем пузыри
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
                                   self.sprite_loader, 'crystal')
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
                                 self.sprite_loader, 'stone')
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
                                self.sprite_loader, 'worm')
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
                                  self.sprite_loader, 'bubble')
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
        if obj and obj.object_type in ['crystal', 'worm']:
            obj.active = False
            return True
        return False
    
    def get_crystals_count(self):
        """Получение количества оставшихся кристаллов"""
        return len([obj for obj in self.game_objects 
                   if obj.active and obj.object_type == 'crystal'])
    
    def can_object_fall_down(self, obj, player_tile_x, player_tile_y):
        """Проверка, может ли объект упасть прямо вниз"""
        # Используем целевую позицию если объект движется
        tile_x, tile_y = obj.get_tile_pos()
        below_tile_y = tile_y + 1
        
        # Если внизу граница уровня - не падаем
        if below_tile_y >= self.height:
            return False
        
        # Проверяем тайл под объектом
        below_tile = self.get_tile(tile_x, below_tile_y)
        
        # Если под объектом пустота
        if below_tile == 'empty':
            # Проверяем, нет ли игрока под объектом
            if tile_x == player_tile_x and below_tile_y == player_tile_y:
                return False
            
            # Проверяем, нет ли другого объекта
            below_object = self.get_object_at(tile_x, below_tile_y)
            if below_object and below_object.active and below_object != obj:
                return False
            
            return True
        
        # Если под объектом земля или стена - не падаем
        return False

    def can_object_slide(self, obj, direction, player_tile_x, player_tile_y):
        """Проверка, может ли объект соскользнуть в сторону
        direction: -1 для левого направления, 1 для правого"""
        
        tile_x, tile_y = obj.get_tile_pos()
        below_tile_y = tile_y + 1
        side_tile_x = tile_x + direction
        
        # Проверяем границы
        if side_tile_x < 0 or side_tile_x >= self.width or below_tile_y >= self.height:
            return False
        
        # Проверяем, что сбоку от объекта пусто
        side_tile = self.get_tile(side_tile_x, tile_y)
        if side_tile != 'empty':
            return False
        
        # Проверяем, что нет объекта сбоку от текущего объекта
        side_object = self.get_object_at(side_tile_x, tile_y)
        if side_object and side_object.active and side_object != obj:
            return False
        
        # Проверяем, что нет игрока сбоку от объекта
        if side_tile_x == player_tile_x and tile_y == player_tile_y:
            return False
        
        # Проверяем, что под боковой позицией пусто
        side_below_tile = self.get_tile(side_tile_x, below_tile_y)
        if side_below_tile != 'empty':
            return False
        
        # Проверяем, что нет объекта под боковой позицией
        side_below_object = self.get_object_at(side_tile_x, below_tile_y)
        if side_below_object and side_below_object.active and side_below_object != obj:
            return False
        
        # Проверяем, что нет игрока под боковой позицией
        if side_tile_x == player_tile_x and below_tile_y == player_tile_y:
            return False
        
        return True

    def is_object_slippery(self, obj_type, tile_type):
        """Проверка, является ли объект/тайл скользким"""
        slippery_objects = ['stone', 'crystal', 'worm', 'bubble']
        slippery_tiles = ['brick_wall', 'stone']
        
        if obj_type:
            return obj_type in slippery_objects
        if tile_type:
            return tile_type in slippery_tiles
        
        return False

    def get_object_fall_direction(self, obj, player_tile_x, player_tile_y):
        """Определение направления падения объекта
        Возвращает: 'down', 'left', 'right' или None"""
        
        # Сначала проверяем, может ли объект упасть прямо вниз
        if self.can_object_fall_down(obj, player_tile_x, player_tile_y):
            return 'down'
        
        # Если не может упасть вниз, проверяем, стоит ли он на скользком объекте
        tile_x, tile_y = obj.get_tile_pos()
        below_tile_y = tile_y + 1
        
        if below_tile_y >= self.height:
            return None
        
        # Проверяем тайл под объектом
        below_tile = self.get_tile(tile_x, below_tile_y)
        below_object = self.get_object_at(tile_x, below_tile_y)
        
        # Определяем, скользкий ли объект/тайл под нами
        is_slippery = False
        if below_object and below_object.active and below_object != obj:
            is_slippery = self.is_object_slippery(below_object.object_type, None)
        else:
            is_slippery = self.is_object_slippery(None, below_tile)
        
        # Если под нами игрок или земля - не скользим
        if (tile_x == player_tile_x and below_tile_y == player_tile_y) or below_tile == 'earth':
            return None
        
        if not is_slippery:
            return None
        
        # Проверяем возможность соскальзывания
        can_slide_left = self.can_object_slide(obj, -1, player_tile_x, player_tile_y)
        can_slide_right = self.can_object_slide(obj, 1, player_tile_x, player_tile_y)
        
        # Если можем соскользнуть в обе стороны, выбираем правую (как в оригинале)
        if can_slide_right:
            return 'right'
        elif can_slide_left:
            return 'left'
        
        return None
    
    def apply_gravity(self, player_tile_x, player_tile_y):
        """Применение гравитации к объектам"""
        # Собираем объекты, которые должны упасть или соскользнуть
        for obj in self.game_objects:
            if not obj.active or not obj.can_fall or obj.is_moving:
                continue
            
            # Если объект уже скользит, продолжаем его движение вниз
            if hasattr(obj, 'fall_state') and obj.fall_state == 'sliding':
                # Проверяем, может ли он упасть вниз после соскальзывания
                if self.can_object_fall_down(obj, player_tile_x, player_tile_y):
                    target_y = obj.y + self.tile_size
                    if obj.start_movement(obj.x, target_y):
                        obj.fall_state = 'falling'
                else:
                    obj.fall_state = 'stable'
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

    def get_player_start_position(self):
        """Получение стартовой позиции игрока"""
        # Возвращаем стандартную стартовую позицию (в тайлах)
        return (1, 1)

    def get_total_crystals(self):
        """Получение общего количества кристаллов на уровне"""
        return len([obj for obj in self.game_objects 
                   if obj.object_type == 'crystal'])
