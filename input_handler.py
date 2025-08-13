import pygame

class InputHandler:
    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()
        
    def handle_event(self, event):
        """Обработка событий ввода"""
        if event.type == pygame.KEYDOWN:
            self.keys_just_pressed.add(event.key)
            self.keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            self.keys_just_released.add(event.key)
            self.keys_pressed.discard(event.key)
    
    def is_key_pressed(self, key):
        """Проверка, нажата ли клавиша в данный момент"""
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key):
        """Проверка, была ли клавиша только что нажата"""
        return key in self.keys_just_pressed
    
    def is_key_just_released(self, key):
        """Проверка, была ли клавиша только что отпущена"""
        return key in self.keys_just_released
    
    def update(self):
        """Обновление состояния ввода (вызывается каждый кадр)"""
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
    
    def get_movement_input(self):
        """Получение направления движения"""
        dx, dy = 0, 0
        
        if self.is_key_just_pressed(pygame.K_LEFT) or self.is_key_just_pressed(pygame.K_a):
            dx = -1
        elif self.is_key_just_pressed(pygame.K_RIGHT) or self.is_key_just_pressed(pygame.K_d):
            dx = 1
        elif self.is_key_just_pressed(pygame.K_UP) or self.is_key_just_pressed(pygame.K_w):
            dy = -1
        elif self.is_key_just_pressed(pygame.K_DOWN) or self.is_key_just_pressed(pygame.K_s):
            dy = 1
        
        return dx, dy