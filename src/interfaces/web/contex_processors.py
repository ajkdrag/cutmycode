from src.domain.constants import Language


def language_choices(request):
    return {
        "language_choices": [("", "All Languages")] + Language.choices(),
    }
