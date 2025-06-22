import random
from level import Level

class LevelManager:
    def __init__(self, sprite_loader):
        self.sprite_loader = sprite_loader
        self.current_level = 1
        self.max_level = 10
        
    def create_level(self, level_number):
        """Создание уровня по номеру"""
        # Устанавливаем seed для воспроизводимости
        random.seed(level_number * 12345)
        
        level = Level(self.sprite_loader)
        
        # Настраиваем сложность в зависимости от номера уровня
        self.adjust_level_difficulty(level, level_number)
        
        return level
    
    def adjust_level_difficulty(self, level, level_number):
        """Настройка сложности уровня"""
        # Увеличиваем количество камней на более высоких уровнях
        stone_probability = min(0.3 + level_number * 0.05, 0.6)
        
        # Пересоздаем уровень с новой сложностью
        for y in range(1, level.height - 1):
            for x in range(3, level.width - 1):  # Оставляем стартовую зону свободной
                if level.tiles[y][x] == 'empty':
                    rand = random.random()
                    if rand < stone_probability:
                        level.tiles[y][x] = 'stone'
        
        # Добавляем больше врагов на высоких уровнях
        enemy_count = min(2 + level_number // 2, 8)
        self.add_enemies(level, enemy_count)
        
        # Добавляем больше кристаллов
        crystal_count = min(5 + level_number, 15)
        self.add_crystals(level, crystal_count)
    
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