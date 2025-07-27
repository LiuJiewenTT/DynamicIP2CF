import sys
from R.string.utils import Namespace

string_dict = {
    "language": {
        "example_string_of_lang": "{}".format(__package__.split('.')[-1]),
        "language_loaded_no_switch_str": "Language {lang} loaded, no switch required.",
        "language_changed_to_str1": "Language changed to {lang}, module: {module}.",
        "language_changed_to_str2": "Language changed from {last_lang} to {lang}, module_name: {module_name}."
    },
    "config": {
        "ini": {
            "warnings": {
                "no_ini_config_file_and_prompt_default_str": "Warning: no .ini format config file is loaded. The default config file is {default_ini_config_file}"
            }
        }
    }
}

namespace: Namespace
if not getattr(sys.modules[__name__], "namespace", None):
    namespace = Namespace(**string_dict)

# Languages
# example_string_of_lang = "{}".format(__package__.split('.')[-1])
#
# language_loaded_no_switch_str = "Language {lang} loaded, no switch required."
# language_changed_to_str1 = "Language changed to {lang}, module: {module}."
# language_changed_to_str2 = "Language changed from {last_lang} to {lang}, module_name: {module_name}."

# Warnings
# warning_no_ini_config_file_and_prompt_default_str = "Warning: no .ini format config file is loaded. The default config file is {default_ini_config_file}"

# Errors
