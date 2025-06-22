import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.7
        self.sound_volume = 0.8
        
        # Создаем папки для звуков если их нет
        self.create_sound_folders()
        self.load_sounds()
    
    def create_sound_folders(self):
        """Создание папок для звуков"""
        sound_dirs = ["assets/sounds", "assets/music"]
        for dir_path in sound_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"Создана папка: {dir_path}")
    
    def load_sounds(self):
        """Загрузка звуков"""
        sound_files = {
            'move': 'move.wav',
            'collect': 'collect.wav',
            'dig': 'dig.wav',
            'death': 'death.wav',
            'level_complete': 'complete.wav'
        }
        
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join("assets", "sounds", filename)
            if os.path.exists(sound_path):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                    self.sounds[sound_name].set_volume(self.sound_volume)
                    print(f"Загружен звук: {sound_name}")
                except pygame.error as e:
                    print(f"Ошибка загрузки звука {sound_name}: {e}")
            # Убираем сообщения об отсутствующих файлах для чистоты вывода
    
    def play_sound(self, sound_name):
        """Воспроизведение звука"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_file):
        """Воспроизведение фоновой музыки"""
        music_path = os.path.join("assets", "music", music_file)
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Зацикливание
                print(f"Воспроизводится музыка: {music_file}")
            except pygame.error as e:
                print(f"Ошибка воспроизведения музыки: {e}")
    
    def stop_music(self):
        """Остановка музыки"""
        pygame.mixer.music.stop()
    
    def set_sound_volume(self, volume):
        """Установка громкости звуков"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """Установка громкости музыки"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
