import pygame

class InputHandler:
    def __init__(self):
        # Состояние клавиш
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()
        
        # Маппинг клавиш для управления
        self.key_mapping = {
            pygame.K_UP: 'UP',
            pygame.K_DOWN: 'DOWN',
            pygame.K_LEFT: 'LEFT',
            pygame.K_RIGHT: 'RIGHT',
            pygame.K_w: 'UP',
            pygame.K_s: 'DOWN',
            pygame.K_a: 'LEFT',
            pygame.K_d: 'RIGHT',
            pygame.K_SPACE: 'ACTION',
            pygame.K_RETURN: 'START',
            pygame.K_ESCAPE: 'MENU'
        }
    
    def handle_event(self, event):
        """Обработка событий клавиатуры"""
        if event.type == pygame.KEYDOWN:
            self.keys_just_pressed.add(event.key)
            self.keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            self.keys_just_released.add(event.key)
            self.keys_pressed.discard(event.key)
    
    def update(self):
        """Очистка временных состояний клавиш"""
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
    
    def is_key_pressed(self, key):
        """Проверка, нажата ли клавиша в данный момент"""
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key):
        """Проверка, была ли клавиша только что нажата"""
        return key in self.keys_just_pressed
    
    def is_action_pressed(self, action):
        """Проверка действия по названию"""
        for key, mapped_action in self.key_mapping.items():
            if mapped_action == action and self.is_key_pressed(key):
                return True
        return False
    
    def is_action_just_pressed(self, action):
        """Проверка, было ли действие только что выполнено"""
        for key, mapped_action in self.key_mapping.items():
            if mapped_action == action and self.is_key_just_pressed(key):
                return True
        return False