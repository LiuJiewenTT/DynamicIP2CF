import sys
from R.string.utils import Namespace

string_dict = {
    "language": {
        "example_string_of_lang": "{}".format(__package__.split('.')[-1]),
        "language_loaded_no_switch_str": "语言 {lang} 已加载，无需切换。",
        "language_changed_to_str1": "语言切换为 {lang}, 模块: {module}。",
        "language_changed_to_str2": "语言从 {last_lang} 切换为 {lang}, 模块名称: {module_name}。"
    },
    "config": {
        "ini": {
            "warnings": {
                "no_ini_config_file_and_prompt_default_str": "警告: 未找到配置文件。提示：默认配置文件是 {default_ini_config_file}。"
            }
        }
    }
}
# Languages
# example_string_of_lang = "{}".format(__package__.split('.')[-1])

# language_loaded_no_switch_str = "语言 {lang} 已加载，无需切换。"
# language_changed_to_str1 = "语言切换为 {lang}, 模块: {module}。"
# language_changed_to_str2 = "语言从 {last_lang} 切换为 {lang}, 模块名称: {module_name}。"

# Warnings
# warning_no_ini_config_file_and_prompt_default_str = "警告: 未找到配置文件。提示：默认配置文件是 {default_ini_config_file}。"

namespace: Namespace
if not getattr(sys.modules[__name__], "namespace", None):
    namespace = Namespace(**string_dict)
# namespace = Namespace(**string_dict)
# Errors
