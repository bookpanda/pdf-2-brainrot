import os
import random


def get_random_file_path(folder_path: str) -> str:
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    if not files:
        raise FileNotFoundError("No files found in the folder.")

    random_file = random.choice(files)
    return os.path.join(folder_path, random_file)
