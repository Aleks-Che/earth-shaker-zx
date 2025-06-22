import pygame
from player import Player
from level import Level

class GameScreen:
    def __init__(self, width, height, sprite_loader, level_number=1):
        self.width = width
        self.height = height
        self.sprite_loader = sprite_loader
        self.level_number = level_number
        
        # Создаем уровень и игрока
        self.level = Level(sprite_loader, level_number)
        
        # Получаем стартовую позицию игрока из данных уровня
        player_start = self.level.get_player_start_position()
        self.player = Player(player_start[0] * 64, player_start[1] * 64, sprite_loader)
        
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
        self.player.update(dt, input_handler, self.level)
        
        # Получаем позицию игрока в тайлах
        player_tile_x = self.player.x // self.tile_size
        player_tile_y = self.player.y // self.tile_size
        
        # Обновляем уровень с позицией игрока
        self.level.update(dt, player_tile_x, player_tile_y)
        
        # Обновляем камеру (следим за игроком)
        self.update_camera()
        
        # Очищаем временные состояния ввода
        if input_handler:
            input_handler.update()
    
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
        ui_height = 120
        ui_surface = pygame.Surface((self.width, ui_height))
        ui_surface.set_alpha(180)
        ui_surface.fill((0, 0, 0))
        screen.blit(ui_surface, (0, 0))
        
        # Статистика игры
        crystals_left = self.level.get_crystals_count()
        total_crystals = self.level.get_total_crystals()
        stats = [
            f"Level: {self.level_number}",
            f"Crystals: {self.player.crystals_collected}/{total_crystals}",
            f"Crystals left: {crystals_left}",
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
            screen.blit(text_surface, (10, 90 + i * 15))
        
        # Заголовок игры в правом верхнем углу
        title = self.font_large.render("EARTHSHAKER", True, (255, 255, 0))
        title_rect = title.get_rect()
        title_rect.topright = (self.width - 10, 10)
        screen.blit(title, title_rect)
