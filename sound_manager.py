import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.7
        self.sound_volume = 0.8
        
        # Инициализируем микшер если еще не инициализирован
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.load_sounds()
    
    def load_sounds(self):
        """Загрузка звуковых файлов"""
        sound_files = {
            'collect_crystal': 'collect_crystal.wav',
            'collect_worm': 'collect_worm.wav',
            'player_death': 'player_death.wav',
            'level_complete': 'level_complete.wav',
            'stone_fall': 'stone_fall.wav'
        }
        
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join("assets", "sounds", filename)
            if os.path.exists(sound_path):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                    print(f"Загружен звук: {sound_path}")
                except pygame.error as e:
                    print(f"Ошибка загрузки звука {sound_path}: {e}")
            else:
                print(f"Звуковой файл не найден: {sound_path}")
    
    def play_sound(self, sound_name):
        """Воспроизведение звука"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(self.sound_volume)
            sound.play()
        else:
            print(f"Звук не найден: {sound_name}")
    
    def play_music(self, filename):
        """Воспроизведение фоновой музыки"""
        music_path = os.path.join("assets", "music", filename)
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Зацикливаем
                print(f"Воспроизводится музыка: {music_path}")
            except pygame.error as e:
                print(f"Ошибка воспроизведения музыки {music_path}: {e}")
        else:
            print(f"Музыкальный файл не найден: {music_path}")
    
    def stop_music(self):
        """Остановка фоновой музыки"""
        pygame.mixer.music.stop()
    
    def set_sound_volume(self, volume):
        """Установка громкости звуков"""
        self.sound_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """Установка громкости музыки"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
