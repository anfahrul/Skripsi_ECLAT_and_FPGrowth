import random
import string

def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # Menggunakan huruf besar, huruf kecil, dan angka
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def bytes_to_mb(bytes_value):
    mb_value = bytes_value / (1024 ** 2)
    return mb_value


def formatting_execution_time(time_in_seconds):
    seconds = time_in_seconds % 60
    minutes = (time_in_seconds // 60) % 60
    hours = time_in_seconds // 3600

    formatted_time = ""

    if hours > 0:
        formatted_time += f"{hours:.0f} Jam "

    if minutes > 0 or hours > 0:
        formatted_time += f"{minutes:.0f} Menit "

    if seconds > 0 or (minutes == 0 and hours == 0):
        formatted_time += f"{seconds:.0f} Detik"

    return formatted_time.strip()