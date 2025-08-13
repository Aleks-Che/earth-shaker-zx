import pygame

class AnimatedSprite:
    def __init__(self, sprites, frame_duration):
        """
        sprites: список спрайтов для анимации
        frame_duration: длительность одного кадра в секундах
        """
        self.sprites = sprites if sprites else []
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_since_last_frame = 0.0
        self.playing = True
        self.loop = True
    
    def update(self, dt):
        """Обновление анимации"""
        if not self.playing or len(self.sprites) <= 1:
            return
        
        self.time_since_last_frame += dt
        
        if self.time_since_last_frame >= self.frame_duration:
            self.time_since_last_frame = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.sprites):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.sprites) - 1
                    self.playing = False
    
    def get_current_sprite(self):
        """Получение текущего спрайта"""
        if not self.sprites:
            return None
        
        frame_index = min(self.current_frame, len(self.sprites) - 1)
        return self.sprites[frame_index]
    
    def reset(self):
        """Сброс анимации к первому кадру"""
        self.current_frame = 0
        self.time_since_last_frame = 0.0
        self.playing = True
    
    def set_frame(self, frame):
        """Установка конкретного кадра"""
        if 0 <= frame < len(self.sprites):
            self.current_frame = frame
    
    def pause(self):
        """Пауза анимации"""
        self.playing = False
    
    def resume(self):
        """Возобновление анимации"""
        self.playing = True
    
    def set_loop(self, loop):
        """Установка зацикливания"""
        self.loop = loop