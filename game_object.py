import pygame
from animated_sprite import AnimatedSprite

class GameObject:
    def __init__(self, x, y, sprite_loader, sprite_name, game_settings):
        self.x = x
        self.y = y
        self.sprite_loader = sprite_loader  # Возвращаем обратно sprite_loader
        self.sprite_name = sprite_name
        self.game_settings = game_settings
        
        # Размер тайла
        self.tile_size = 64
        
        # Состояние
        self.active = True
        
        # Анимация
        self.setup_sprite()
        
        # Движение
        self.is_moving = False
        self.move_start_x = x
        self.move_start_y = y
        self.move_target_x = x
        self.move_target_y = y
        self.move_progress = 0.0
        self.move_speed = 1.0 / 0.15  # Движение за 0.15 секунды
        
        # Физические свойства
        self.can_fall = False
        self.fall_state = 'stable'  # 'stable', 'falling', 'sliding'
        
        # Тип объекта (устанавливается извне)
        self.object_type = 'unknown'
    
    def setup_sprite(self):
        """Настройка спрайта/анимации"""
        # Пытаемся получить анимацию
        animation = self.sprite_loader.get_animation(self.sprite_name)
        if animation:
            self.sprite = AnimatedSprite(animation, 0.3)
        else:
            # Пытаемся получить статичный спрайт
            static_sprite = self.sprite_loader.get_sprite(self.sprite_name)
            if static_sprite:
                self.sprite = AnimatedSprite([static_sprite], 1.0)
            else:
                # Создаем заглушку
                placeholder = pygame.Surface((self.tile_size, self.tile_size))
                placeholder.fill((255, 0, 255))  # Пурпурный для неизвестных объектов
                self.sprite = AnimatedSprite([placeholder], 1.0)
    
    def update(self, dt):
        """Обновление объекта"""
        if not self.active:
            return
        
        # Обновляем анимацию
        self.sprite.update(dt)
        
        # Обновляем движение
        if self.is_moving:
            self.update_movement(dt)
    
    def start_movement(self, target_x, target_y):
        """Начало движения к цели"""
        if self.is_moving:
            return False  # Уже движемся
        
        self.is_moving = True
        self.move_start_x = self.x
        self.move_start_y = self.y
        self.move_target_x = target_x
        self.move_target_y = target_y
        self.move_progress = 0.0
        return True
    
    def update_movement(self, dt):
        """Обновление движения"""
        if not self.is_moving:
            return
        
        self.move_progress += self.move_speed * dt
        
        if self.move_progress >= 1.0:
            # Движение завершено
            self.move_progress = 1.0
            self.x = self.move_target_x
            self.y = self.move_target_y
            self.is_moving = False
            self.fall_state = 'stable'
        else:
            # Интерполяция позиции
            self.x = self.move_start_x + (self.move_target_x - self.move_start_x) * self.move_progress
            self.y = self.move_start_y + (self.move_target_y - self.move_start_y) * self.move_progress
    
    def get_tile_pos(self):
        """Получение позиции в тайлах"""
        return (int(self.x // self.tile_size), int(self.y // self.tile_size))
    
    def render(self, screen, camera_x, camera_y):
        """Отрисовка объекта"""
        if not self.active:
            return
        
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
            color = self.get_object_color()
            pygame.draw.rect(screen, color, (screen_x, screen_y, self.tile_size, self.tile_size))
    
    def get_object_color(self):
        """Получение цвета объекта для заглушки"""
        colors = {
            'crystal': (255, 0, 255),
            'stone': (128, 128, 128),
            'worm': (255, 100, 100),
            'bubble': (0, 255, 255),
            'fire': (255, 100, 0)
        }
        return colors.get(self.object_type, (255, 0, 255))
