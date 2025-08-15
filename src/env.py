import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
if os.path.exists(".env.local"):
    load_dotenv(dotenv_path=".env.local", override=True)

def get_env_str(key):
    return os.getenv(key)

def get_env_int(key):
    return int(get_env_str(key))

def get_env_bool(key):
    env = get_env_str(key)
    return env.lower() in ['true', '1', 't', 'y', 'yes']
