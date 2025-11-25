from enum import Enum


class Theme(str, Enum):
    classic = "classic"
    light = "light"
    dark = "dark"
    dark_high_contrast = "dark_high_contrast"


class ZodiacType(str, Enum):
    tropic = "Tropic"
    sidereal = "Sidereal"


class SiderealMode(str, Enum):
    lahiri = "LAHIRI"
    fagan_bradley = "FAGAN_BRADLEY"
    de_luce = "DE_LUCE"
    krishnamurti = "KRISHNAMURTI"
    raman = "RAMAN"
    sunda = "SUNDA"
    bd_lahiri = "BD_LAHIRI"
    yukteshwar = "YUKTESHWAR"
    djwhal_khul = "DJWHAL_KHUL"
    huber = "HUBER"
    sunita = "SUNITA"
    true_citra = "TRUE_CITRA"
    galactic = "GALACTIC_CENTER"
    aryan = "ARYANA"
    hiraj = "HIRAJ"
    custom = "CUSTOM"


class HouseSystem(str, Enum):
    placidus = "P"
    whole_sign = "W"
    koch = "K"
    equal = "E"
    campanus = "C"
    regimontanus = "R"
    meridian = "X"
    morinus = "M"
    topocentric = "T"
    krusinski = "H"


class Language(str, Enum):
    en = "en"
    es = "es"
    fr = "fr"
    it = "it"
    de = "de"
    pt = "pt"
    ru = "ru"
    hi = "hi"
    zh = "zh"
    jp = "jp"
