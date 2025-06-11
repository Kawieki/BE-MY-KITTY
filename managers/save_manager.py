import os
from datetime import datetime
from utils.parser import parse_value

class SaveManager:
    def __init__(self):
        self.save_dir = "saves"
        self.max_saves = 5
        self._ensure_save_directory()

    def _ensure_save_directory(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def _get_save_files(self):
        try:
            save_files = [f for f in os.listdir(self.save_dir) if f.endswith('.meow')]
            save_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.save_dir, x)), reverse=True)
            return save_files
        except Exception as e:
            print(f"Error getting save files: {e}")
            return []

    def _remove_oldest_save(self):
        save_files = self._get_save_files()
        if len(save_files) >= self.max_saves:
            oldest_save = save_files[-1]
            try:
                os.remove(os.path.join(self.save_dir, oldest_save))
            except Exception as e:
                print(f"Error removing oldest save: {e}")

    def save_game(self, animal, food_manager, game_logic):
        save_name = animal.name.replace(" ", "_")
        filename = f"{save_name}.meow"
        filepath = os.path.join(self.save_dir, filename)
        save_files = self._get_save_files()
        if not os.path.exists(filepath):
            if len(save_files) >= self.max_saves:
                self._remove_oldest_save()

        try:
            with open(filepath, 'w') as f:
                f.write(f"name={animal.name}\n")
                f.write(f"age={animal.age}\n")
                f.write(f"hunger_level={animal.hunger_level}\n")
                f.write(f"boredom_level={animal.boredom_level}\n")
                f.write(f"quantity={food_manager.food_quantity}\n")
                f.write(f"remaining={food_manager.remaining_food}\n")
                f.write(f"cooldown={food_manager.feed_cooldown}\n")
                f.write(f"playtime={game_logic.playtime}\n")
                f.write(f"playtime_remaining={game_logic.playtime_remaining}\n")
                f.write(f"in_cooldown={int(game_logic.in_cooldown)}\n")
                f.write(f"cooldown_timer={game_logic.cooldown_timer}\n")
                f.write(f"\ntimestamp={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"static_asset_path={animal.static_asset.path}\n")
                f.write(f"static_asset_size={animal.static_asset.size[0]},{animal.static_asset.size[1]}\n")
                f.write(f"static_asset_position={animal.static_asset.position[0]},{animal.static_asset.position[1]}\n")
                f.write(f"animated_asset_path={animal.animated_asset.folder}\n")
                f.write(f"animated_asset_size={animal.animated_asset.size[0]},{animal.animated_asset.size[1]}\n")
                f.write(f"animated_asset_position={animal.animated_asset.pos[0]},{animal.animated_asset.pos[1]}\n")
                f.write(f"label={animal.static_asset.label}\n")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, save_file):
        data = {}
        try:
            with open(os.path.join(self.save_dir, save_file), 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith("["):
                        continue
                    if '=' in line:
                        key, val = line.split("=", 1)
                        key, val = key.strip(), parse_value(val)
                        data[key] = val
            return data
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def get_recent_saves(self):
        return self._get_save_files()[:self.max_saves]
