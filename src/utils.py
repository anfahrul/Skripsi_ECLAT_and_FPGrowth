import random
import string

def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # Menggunakan huruf besar, huruf kecil, dan angka
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def bytes_to_mb(bytes_value):
    mb_value = bytes_value / (1024 ** 2)
    return mb_value