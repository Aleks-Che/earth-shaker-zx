import pygame
from animated_sprite import AnimatedSprite

class GameObject:
    def __init__(self, x, y, sprite_loader, sprite_name, game_settings=None):
        self.x = x
        self.y = y
        self.sprite_loader = sprite_loader
        self.sprite_name = sprite_name
        self.game_settings = game_settings
        self.tile_size = 64
        
        # Создаем анимированный спрайт
        sprites = sprite_loader.get_sprite(sprite_name)
        if isinstance(sprites, list):
            self.animated_sprite = AnimatedSprite(sprites)
        else:
            self.animated_sprite = AnimatedSprite([sprites] if sprites else [])
        
        self.active = True
        
        # Движение
        self.is_moving = False
        self.move_timer = 0
        self.move_duration = 0.15
        self.start_pos = (x, y)
        self.target_pos = (x, y)
        
        # Физические свойства
        self.can_fall = False
        self.fall_state = 'stable'
        self.object_type = 'unknown'
        
    def start_movement(self, target_x, target_y):
        """Начало движения к цели"""
        if self.is_moving:
            return False
            
        self.is_moving = True
        self.move_timer = 0
        self.start_pos = (self.x, self.y)
        self.target_pos = (target_x, target_y)
        
        # Если плавная анимация выключена, сразу перемещаемся
        if self.game_settings and not self.game_settings.smooth_movement:
            self.x, self.y = self.target_pos
            self.is_moving = False
        
        return True
        
    def update(self, dt):
        """Обновление объекта"""
        if self.active:
            self.animated_sprite.update(dt)
            
            # Обновляем движение только если включена плавная анимация
            if self.is_moving and self.game_settings and self.game_settings.smooth_movement:
                self.update_movement(dt)
    
    def update_movement(self, dt):
        """Обновление плавного движения"""
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
    
    def render(self, screen, camera_x, camera_y):
        """Отрисовка объекта"""
        if not self.active:
            return
            
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        sprite = self.animated_sprite.get_current_sprite()
        if sprite:
            screen.blit(sprite, (screen_x, screen_y))
        else:
            # Заглушка если спрайт не найден
            color = self.get_object_color()
            pygame.draw.rect(screen, color,
                           (screen_x, screen_y, self.tile_size, self.tile_size))
            pygame.draw.rect(screen, (255, 255, 255),
                           (screen_x, screen_y, self.tile_size, self.tile_size), 2)
    
    def get_object_color(self):
        """Получение цвета объекта для заглушки"""
        colors = {
            'crystal': (255, 0, 255),
            'stone': (128, 128, 128),
            'worm': (255, 100, 100),
            'bubble': (0, 255, 255)
        }
        return colors.get(self.object_type, (255, 255, 255))
    
    def get_tile_pos(self):
        """Получение позиции в тайлах"""
        return (int(self.x // self.tile_size), int(self.y // self.tile_size))
