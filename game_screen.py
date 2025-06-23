import pygame
from player import Player
from level import Level

class GameScreen:
    def __init__(self, width, height, sprite_loader, game_settings, level_number=1):
        self.width = width
        self.height = height
        self.sprite_loader = sprite_loader
        self.game_settings = game_settings
        self.level_number = level_number
        
        # Создаем уровень и игрока
        self.level = Level(sprite_loader, game_settings, level_number)
        
        # Получаем стартовую позицию игрока из данных уровня
        player_start = self.level.get_player_start_position()
        self.player = Player(player_start[0] * 64, player_start[1] * 64, sprite_loader, game_settings)
        
        # Камера
        self.camera_x = 0
        self.camera_y = 0
        
        # Размер тайла
        self.tile_size = 64
        
        # UI
        self.font = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        
    def handle_event(self, event):
        """Обработка событий экрана"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "BACK_TO_MENU"
        return None
    
    def update(self, dt, input_handler):
        """Обновление игрового экрана"""
        # Обновляем игрока
        result = self.player.update(dt, input_handler, self.level)
        
        # Проверяем завершение уровня
        if result == "LEVEL_COMPLETE":
            return "LEVEL_COMPLETE"
        
        # Получаем информацию о позиции игрока
        player_occupied_tiles = self.player.get_occupied_tiles()
        player_is_moving = self.player.is_moving
        
        # Обновляем уровень с информацией о игроке
        self.level.update(dt, player_occupied_tiles, player_is_moving)
        
        # Обновляем камеру (следим за игроком)
        self.update_camera()
        
        # Очищаем временные состояния ввода
        if input_handler:
            input_handler.update()
        
        return None
    
    def update_camera(self):
        """Обновление позиции камеры"""
        # Центрируем камеру на игроке
        self.camera_x = self.player.x - self.width // 2
        self.camera_y = self.player.y - self.height // 2
        
        # Ограничиваем камеру границами уровня
        max_camera_x = self.level.width * self.tile_size - self.width
        max_camera_y = self.level.height * self.tile_size - self.height
        
        self.camera_x = max(0, min(self.camera_x, max_camera_x))
        self.camera_y = max(0, min(self.camera_y, max_camera_y))
    
    def render(self, screen):
        """Отрисовка игрового экрана"""
        # Заливаем фон
        screen.fill((0, 0, 0))
        
        # Отрисовываем уровень
        self.level.render(screen, self.camera_x, self.camera_y)
        
        # Отрисовываем игрока
        self.player.render(screen, self.camera_x, self.camera_y)
        
        # Отрисовываем UI
        self.render_ui(screen)
    
    def render_ui(self, screen):
        """Отрисовка пользовательского интерфейса"""
        # Полупрозрачный фон для UI
        ui_height = 140
        ui_surface = pygame.Surface((self.width, ui_height))
        ui_surface.set_alpha(180)
        ui_surface.fill((0, 0, 0))
        screen.blit(ui_surface, (0, 0))
        
        # Статистика игры
        crystals_left = self.level.get_crystals_count()
        movement_mode = "Smooth" if self.game_settings.smooth_movement else "Grid"
        stats = [
            f"Level: {self.level_number}",
            f"Crystals: {self.player.crystals_collected}/{self.level.total_crystals}",
            f"Crystals left: {crystals_left}",
            f"Movement: {movement_mode}",
            f"Position: ({self.player.x // self.tile_size}, {self.player.y // self.tile_size})"
        ]
        
        for i, stat in enumerate(stats):
            text_surface = self.font.render(stat, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 20))
        
        # Управление
        controls = [
            "WASD/Arrows - Move",
            "ESC - Menu"
        ]
        
        for i, control in enumerate(controls):
            text_surface = self.font.render(control, True, (200, 200, 200))
            screen.blit(text_surface, (10, 110 + i * 15))
        
        # Заголовок игры в правом верхнем углу
        title = self.font_large.render("EARTHSHAKER", True, (255, 255, 0))
        title_rect = title.get_rect()
        title_rect.topright = (self.width - 10, 10)
        screen.blit(title, title_rect)
