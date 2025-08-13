import random
from level import Level
from level_data import LevelData

class LevelManager:
    def __init__(self, sprite_loader):
        self.sprite_loader = sprite_loader
        self.current_level = 1
        self.max_level = 4  # У нас есть 4 уровня в данных
        
    def create_level(self, level_number):
        """Создание уровня по номеру"""
        print(f"LevelManager: создаем уровень {level_number}")
        
        # Проверяем, есть ли данные для этого уровня
        level_data = LevelData.get_level(level_number)
        if level_data:
            print(f"LevelManager: найдены данные для уровня {level_number}")
            level = Level(self.sprite_loader, level_number=level_number)
        else:
            print(f"LevelManager: данные для уровня {level_number} не найдены, создаем случайный")
            # Устанавливаем seed для воспроизводимости
            random.seed(level_number * 12345)
            level = Level(self.sprite_loader, level_number=level_number)
            
            # Настраиваем сложность случайного уровня
            self.adjust_level_difficulty(level, level_number)
        
        return level
    
    def adjust_level_difficulty(self, level, level_number):
        """Настройка сложности случайного уровня"""
        print(f"LevelManager: настраиваем сложность уровня {level_number}")
        
        # Увеличиваем количество камней на более высоких уровнях
        stone_probability = min(0.2 + level_number * 0.05, 0.5)
        
        # Пересоздаем части уровня с новой сложностью
        for y in range(1, level.height - 1):
            for x in range(3, level.width - 1):  # Оставляем стартовую зону свободной
                if level.tiles[y][x] == 'empty':
                    rand = random.random()
                    if rand < stone_probability:
                        level.tiles[y][x] = 'stone_gray'
        
        # Добавляем дополнительные объекты на высоких уровнях
        if level_number > 2:
            self.add_extra_objects(level, level_number)
    
    def add_extra_objects(self, level, level_number):
        """Добавление дополнительных объектов на сложных уровнях"""
        from game_object import GameObject
        
        # Добавляем больше кристаллов
        extra_crystals = min(level_number - 2, 5)
        added = 0
        attempts = 0
        max_attempts = 50
        
        while added < extra_crystals and attempts < max_attempts:
            x = random.randint(1, level.width - 2)
            y = random.randint(1, level.height - 2)
            
            # Не размещаем в стартовой зоне
            if x <= 2 and y <= 2:
                attempts += 1
                continue
            
            if level.tiles[y][x] == 'empty' and not level.get_object_at(x, y):
                crystal = GameObject(x * level.tile_size, y * level.tile_size, 
                                   level.sprite_loader, 'crystal', level.game_settings)
                crystal.object_type = 'crystal'
                crystal.can_fall = True
                crystal.fall_state = 'stable'
                level.game_objects.append(crystal)
                added += 1
            
            attempts += 1
        
        print(f"LevelManager: добавлено {added} дополнительных кристаллов")
    
    def add_enemies(self, level, count):
        """Добавление врагов на уровень"""
        added = 0
        attempts = 0
        max_attempts = 100
        
        while added < count and attempts < max_attempts:
            x = random.randint(5, level.width - 2)
            y = random.randint(1, level.height - 2)
            
            if level.tiles[y][x] == 'empty' and not level.get_object_at(x, y):
                enemy_type = random.choice(['worm', 'fire'])
                enemy = level.create_enemy(x, y, enemy_type)
                if enemy:
                    level.game_objects.append(enemy)
                    added += 1
            
            attempts += 1
    
    def add_crystals(self, level, count):
        """Добавление кристаллов на уровень"""
        # Очищаем существующие кристаллы
        level.game_objects = [obj for obj in level.game_objects if obj.sprite_name != 'crystal']
        
        added = 0
        attempts = 0
        max_attempts = 200
        
        while added < count and attempts < max_attempts:
            x = random.randint(1, level.width - 2)
            y = random.randint(1, level.height - 2)
            
            # Не размещаем в стартовой зоне
            if x <= 2 and y <= 2:
                attempts += 1
                continue
            
            if level.tiles[y][x] == 'empty' and not level.get_object_at(x, y):
                crystal = level.create_crystal(x, y)
                if crystal:
                    level.game_objects.append(crystal)
                    added += 1
            
            attempts += 1
    
    def get_next_level(self):
        """Переход к следующему уровню"""
        if self.current_level < self.max_level:
            self.current_level += 1
            return self.create_level(self.current_level)
        return None
    
    def reset_to_first_level(self):
        """Сброс к первому уровню"""
        self.current_level = 1
        return self.create_level(self.current_level)
    
    def get_level_info(self, level_number):
        """Получение информации об уровне"""
        level_data = LevelData.get_level(level_number)
        if level_data:
            return {
                'number': level_number,
                'width': level_data['width'],
                'height': level_data['height'],
                'crystals': level_data['crystals_total'],
                'has_data': True
            }
        else:
            return {
                'number': level_number,
                'width': 15,
                'height': 12,
                'crystals': 8,
                'has_data': False
            }