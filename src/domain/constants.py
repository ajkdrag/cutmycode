import enum


@enum.unique
class Language(str, enum.Enum):
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    HTML = "HTML"
    CSS = "CSS"

    @classmethod
    def choices(cls):
        return [(item.name, item.value) for item in cls]
