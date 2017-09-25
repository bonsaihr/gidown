import datetime


class QuerySetting:

    def __init__(self, setting_str: str):
        self._setting = setting_str

    def __str__(self):
        return  self._setting

    def urlencode(self):
        return self._setting


    def __add__(self, other):
        if isinstance(other, QuerySettings):
            return other + self
        if isinstance(other, self.__class__):
            return QuerySettings(self, other)


class QuerySettings:

    def __init__(self, *settings: QuerySetting):
        self._settings = list(*settings)

    def __str__(self):
        return " and ".join(str(setting) for setting in self._settings)

    def urlencode(self):
        return ",".join(setting.urlencode() for setting in self._settings)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            ret = QuerySettings()
            ret._settings = self._settings + other._settings
            return ret
        if isinstance(other, QuerySetting):
            ret = QuerySettings()
            ret._settings = self._settings[:]
            ret._settings.append(other)
            return ret


class Size:

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    LARGE = QuerySetting("isz:l")
    MEDIUM = QuerySetting("isz:m")
    ICON = QuerySetting("isz:i")

    @staticmethod
    def exactly(w: int, h: int) -> QuerySetting:
        return QuerySetting("isz:ex,iszw:{},iszh:{}".format(w, h))

    class LargerThen:

        def __init__(self):
            raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

        S_400x300 = QuerySetting("isz:lt,islt:qsvga")
        S_640x480 = QuerySetting("isz:lt,islt:vga")
        S_800x600 = QuerySetting("isz:lt,islt:svg")
        S_1024x768 = QuerySetting("isz:lt,islt:xga")

        QSVGA = S_400x300
        VGA = S_640x480
        SVG = S_800x600
        XGA = S_1024x768

        MP_2 = QuerySetting("isz:lt,islt:2mp")
        MP_4 = QuerySetting("isz:lt,islt:4mp")
        MP_6 = QuerySetting("isz:lt,islt:6mp")
        MP_8 = QuerySetting("isz:lt,islt:8mp")
        MP_10 = QuerySetting("isz:lt,islt:10mp")
        MP_12 = QuerySetting("isz:lt,islt:12mp")
        MP_15 = QuerySetting("isz:lt,islt:15mp")
        MP_20 = QuerySetting("isz:lt,islt:20mp")
        MP_40 = QuerySetting("isz:lt,islt:40mp")
        MP_70 = QuerySetting("isz:lt,islt:70mp")


class Color:

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    FULL = QuerySetting("ic:color")
    GRAY_SCALE = QuerySetting("ic:gray")
    TRANSPARENT = QuerySetting("ic:trans")

    RED = QuerySetting("ic:specific,isc:red")
    ORANGE = QuerySetting("ic:specific,isc:orange")
    YELLOW = QuerySetting("ic:specific,isc:yellow")
    GREEN = QuerySetting("ic:specific,isc:green")
    TEAL = QuerySetting("ic:specific,isc:teal")
    BLUE = QuerySetting("ic:specific,isc:blue")
    PURPLE = QuerySetting("ic:specific,isc:purple")
    PINK = QuerySetting("ic:specific,isc:pink")
    WHITE = QuerySetting("ic:specific,isc:white")
    GRAY = QuerySetting("ic:specific,isc:gray")
    BLACK = QuerySetting("ic:specific,isc:black")
    BROWN = QuerySetting("ic:specific,isc:brown")


class Type:

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    FACE = QuerySetting("itp:face")
    PHOTO = QuerySetting("itp:photo")
    CLIP_ART = QuerySetting("itp:clipart")
    LINE_DRAWING = QuerySetting("itp:lineart")


class Time:

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    PAST_SECOND = QuerySetting("qdr:d")
    PAST_24H = QuerySetting("qdr:d")
    PAST_WEEK = QuerySetting("qdr:w")

    _valid_measures = "nhdwm"

    @staticmethod
    def past(self, value, measure="h"):
        if measure not in Time._valid_measures:
            raise ValueError("Unknown measure {}, must be one of: {}".format(measure, Time._valid_measures))
        return "tbs=qdr:{}{}".format(measure, "" if value <= 1 else value)

    @staticmethod
    def range(date_from: datetime.date, date_to: datetime.date) ->QuerySetting:
        return QuerySetting("cdr=1,cd_min={}.{}.{},cd_max={}.{}.{}".format(
            date_from.day, date_from.month, date_from.year, date_to.day, date_to.month, date_to.year))


class FileFormat:

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    JPG = QuerySetting("ift:jpg")
    GIF = QuerySetting("ift:gif")
    PNG = QuerySetting("ift:png")
    BMP = QuerySetting("ift:mbp")
    SVG = QuerySetting("ift:svg")
    WEBP = QuerySetting("ift:webp")
    ICO = QuerySetting("ift:ico")


class AspectRatio:

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    TALL = QuerySetting("iar:t")
    SQUARE = QuerySetting("iar:s")
    WIDE = QuerySetting("iar:w")
    PANORAMIC = QuerySetting("iar:xw")


class UsageRights:

    def __init__(self):
        raise NotImplementedError()

    ANY = QuerySetting("")
    REUSE_WITH_MODIFICATION = QuerySetting("sur:fc")
    REUSE = QuerySetting("sur:fmc")
    NONCOMMERCIAL_REUSE_WITH_MODIFICATION = QuerySetting("sur:fm")
    NONCOMMERCIAL_REUSE = QuerySetting("sur:f")


class Sorting:

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    BY_DATE = QuerySetting("sbd:1")
    BY_RELEVANCE = QuerySetting("sbd:0")

