import pygame

class AnimatedSprite:
    def __init__(self, sprites, animation_speed=0.25):
        self.sprites = sprites if sprites else []
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.animation_timer = 0
        self.is_playing = True
        
    def update(self, dt):
        """Обновление анимации"""
        if self.is_playing and len(self.sprites) > 1:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.sprites)
    
    def get_current_sprite(self):
        """Получение текущего кадра анимации"""
        if self.sprites and len(self.sprites) > 0:
            return self.sprites[self.current_frame]
        return None
    
    def reset(self):
        """Сброс анимации"""
        self.current_frame = 0
        self.animation_timer = 0
    
    def set_frame(self, frame):
        """Установка конкретного кадра"""
        if 0 <= frame < len(self.sprites):
            self.current_frame = frame