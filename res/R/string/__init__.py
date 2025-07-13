import sys
from . import i18n
from .default import *

current_used_lang: str
if not getattr(sys.modules[__name__], "current_used_lang", None):
    current_used_lang = default_lang


def use_lang(lang, force_load=False):
    global current_used_lang
    switched = False
    module_name = "{}.i18n.{}".format(__package__, lang)
    if module_name not in sys.modules or force_load is True:
        module = __import__(module_name, fromlist=['*'])
        sys.modules[module_name] = module
        switched = True
    else:
        module = sys.modules[module_name]
    globals().update({
        k: getattr(module, k)
        for k in dir(module)
        if not k.startswith('_')
    })
    if switched:
        last_lang = current_used_lang
        current_used_lang = lang
        # print(language_changed_to_str1.format(lang=lang, module=module))
        print(language_changed_to_str2.format(last_lang=last_lang, lang=lang, module_name=module_name))
    else:
        print(language_loaded_no_switch_str.format(lang=lang))


