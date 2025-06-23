import pygame
from menu_screen import MenuScreen
from level_select_screen import LevelSelectScreen
from game_screen import GameScreen
from settings_screen import SettingsScreen
from sprite_loader import SpriteLoader
from sound_manager import SoundManager
from input_handler import InputHandler
from game_settings import GameSettings

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Инициализация подсистем
        pygame.mixer.init()
        
        # Настройки игры
        self.game_settings = GameSettings()
        
        # Загрузчики ресурсов
        self.sprite_loader = SpriteLoader()
        self.sound_manager = SoundManager()
        
        # Обработчик ввода
        self.input_handler = InputHandler()
        
        # Экраны игры
        self.screens = {
            'MENU': MenuScreen(width, height),
            'LEVEL_SELECT': LevelSelectScreen(width, height),
            'GAME': GameScreen(width, height, self.sprite_loader, self.game_settings),
            'SETTINGS': SettingsScreen(width, height, self.sound_manager, self.game_settings)
        }
        
        # Текущий экран
        self.current_screen = 'MENU'
        
        print("Игра инициализирована")
    
    def handle_event(self, event):
        """Обработка событий"""
        # Передаем события в обработчик ввода
        self.input_handler.handle_event(event)
        
        # Передаем события в текущий экран
        current_screen_obj = self.screens[self.current_screen]
        result = current_screen_obj.handle_event(event)
        
        # Обрабатываем результат
        if result:
            return self.handle_screen_result(result)
        
        return None
    
    def handle_screen_result(self, result):
        """Обработка результатов экранов"""
        if result == "START_GAME":
            self.current_screen = 'GAME'
            # Создаем новый экран игры с уровнем 1
            self.screens['GAME'] = GameScreen(self.width, self.height, self.sprite_loader, self.game_settings, level_number=1)
            self.sound_manager.play_music("game_music.ogg")
        elif result == "SELECT_LEVEL":
            self.current_screen = 'LEVEL_SELECT'
        elif result.startswith("START_LEVEL_"):
            level_number = int(result.split("_")[-1])
            self.current_screen = 'GAME'
            # Создаем новый экран игры с выбранным уровнем
            self.screens['GAME'] = GameScreen(self.width, self.height, self.sprite_loader, self.game_settings, level_number=level_number)
            self.sound_manager.play_music("game_music.ogg")
        elif result == "LEVEL_COMPLETE":
            # Переходим к следующему уровню или показываем экран победы
            current_level = getattr(self.screens['GAME'], 'level_number', 1)
            next_level = current_level + 1
            
            if next_level <= 4:  # Максимум 4 уровня
                print(f"Moving to level {next_level}")
                self.screens['GAME'] = GameScreen(self.width, self.height, self.sprite_loader, self.game_settings, level_number=next_level)
            else:
                print("Game completed!")
                self.current_screen = 'MENU'
                self.sound_manager.stop_music()
        elif result == "SETTINGS":
            self.current_screen = 'SETTINGS'
        elif result == "MAIN_MENU":
            self.current_screen = 'MENU'
            self.sound_manager.stop_music()
        elif result == "BACK_TO_MENU":
            self.current_screen = 'MENU'
            self.sound_manager.stop_music()
        elif result == "QUIT":
            return "QUIT"
        
        return None
    
    def update(self, dt):
        """Обновление игры"""
        current_screen_obj = self.screens[self.current_screen]
        
        # Получаем результат обновления экрана
        if hasattr(current_screen_obj, 'update'):
            result = current_screen_obj.update(dt, self.input_handler)
            
            # Обрабатываем результат
            if result:
                return self.handle_screen_result(result)
        else:
            current_screen_obj.update(dt, self.input_handler)
        
        return None
    
    def render(self):
        """Отрисовка игры"""
        current_screen_obj = self.screens[self.current_screen]
        current_screen_obj.render(self.screen)
