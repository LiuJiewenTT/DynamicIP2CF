import sys
from . import i18n
from .default import *


def use_lang(lang, force=False):
    module_name = "{}.i18n.{}".format(__package__, lang)
    if module_name not in sys.modules or force is True:
        module = __import__(module_name, fromlist=['*'])
        sys.modules[module_name] = module
    else:
        module = sys.modules[module_name]
    globals().update({
        k: getattr(module, k)
        for k in dir(module)
        if not k.startswith('_')
    })
    print(language_changed_to_str1.format(lang=lang, module=module))
    print(language_changed_to_str2.format(lang=lang, module_name=module_name))

