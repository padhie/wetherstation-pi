from dataclasses import dataclass
from src.env import get_env_str, get_env_int, get_env_bool

fontPath  =  get_env_str("FONT_PATH")

@dataclass
class Display:
    width: int
    height: int

@dataclass
class Eink:
    active: bool
    debugImg: str

@dataclass
class OpenWeather:
    apikey: str
    city: str

@dataclass
class HomeAssistant:
    url: str
    token: str

@dataclass
class Settings:
    display: Display
    eink: Eink
    homeAssistant: HomeAssistant
    openWeather: OpenWeather
    fontPath: str

def generate():
    return Settings(
        display = Display(
            height = get_env_int("HEIGHT"),
            width = get_env_int("WIDTH"),
        ),
        eink = Eink(
            active = get_env_bool("EINK_ACTIVE"),
            debugImg = get_env_str("EINK_DEBUG_IMG"),
        ),
        homeAssistant = HomeAssistant(
            url = get_env_str("HA_URL"),
            token = get_env_str("HA_TOKEN"),
        ),
        openWeather = OpenWeather(
            apikey = get_env_str("OW_APIKEY"),
            city = get_env_str("OW_CITY"),
        ),
        fontPath = fontPath,
    )