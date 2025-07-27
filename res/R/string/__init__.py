import sys
from . import i18n
from .default import *
from .utils import use_lang


current_used_lang: str
if not getattr(sys.modules[__name__], "current_used_lang", None):
    current_used_lang = default_lang


