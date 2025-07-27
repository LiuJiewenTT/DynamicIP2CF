default_lang = "zh_CN"
from .i18n.zh_CN import *

globals().update({
        k: getattr(namespace, k)
        for k in namespace.__dict__
    })

