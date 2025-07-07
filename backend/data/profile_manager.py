# data/profile_manager.py

import json
from .profile import Profile


class ProfileManager:

    @staticmethod
    def load_profile(file_path: str) -> Profile:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Profile(**data)

    @staticmethod
    def save_profile(profile: Profile, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(profile.__dict__, f, ensure_ascii=False, indent=4)
