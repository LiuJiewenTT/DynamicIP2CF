import sys
from R.string.utils import Namespace

string_dict = {
    "language": {
        "example_string_of_lang": "{}".format(__package__.split('.')[-1]),
        "language_loaded_no_switch": "语言 {lang} 已加载，无需切换。",
        "language_changed_to_str1": "语言切换为 {lang}, 模块: {module}。",
        "language_changed_to_str2": "语言从 {last_lang} 切换为 {lang}, 模块名称: {module_name}。",
        "notices": {
            "preferred_lang_not_same_as_system_lang": "提示: 系统语言与首选语言不同。"
        },
        "warnings": {
            "system_lang_not_recognized": "警告: 系统语言无法识别，将使用默认语言。"
        }
    },
    "config": {
        "ini": {
            "warnings": {
                "no_file_and_prompt_default": "警告: 未找到配置文件。提示：默认配置文件是 {default_ini_config_file}。"
            }
        }
    },
    "cli": {
        "parser": {
            "description": "更新 Cloudflare DNS 记录中的 IP 地址。",
            "options_help": {
                "cli_mode": "运行于 CLI 模式",
                "cli_automated": "运行于 CLI 自动模式",
                "read_config_ini": "读取 .ini 格式的配置文件",
                "ip_version": "IP 版本，可选值: v4, v6",
                "ip": "用于更新的 IP 地址",
                "api_token": "Cloudflare API 口令",
                "zone_id": "Cloudflare 区域 ID",
                "record_id": "Cloudflare DNS 记录 ID",
                "domain_name": "要被更新的 DNS 记录的域名",
                "generate_config_ini": "生成 config.ini 配置文件",
                "proxy_mode": "网络代理模式, 可选值: auto, system, manual, off",
                "proxy_url": "网络代理URL, 应当是类似于: http://127.0.0.1:8888 的链接",
                "override_list": "网络代理覆写列表，用于跳过网络代理, 应当是类似于: 192.168.1.1;192.168.1.2 。此功能可能不是很完善。",
                "program_info": "展示程序信息并退出"
            }
        }
    },
    "gui": {
        "main_window": {
            "info_group": {
                "status_label": {
                    "title": "状态：",
                    "ready": "就绪",
                    "getting_ip": "获取IP中...",
                    "updating_ip_to_dns": "更新IP到DNS中...",
                },
                "result_label": {
                    "title": "结果信息：",
                    "success": "成功",
                    "failed": "失败",
                    "null": "空",
                    "no_ip_selected": "没有选择IP",
                    "invalid_ip": "IP错误：{error}",
                    "updating_ip_to_dns_success": "更新IP到DNS成功",
                    "updating_ip_to_dns_failed_1": "更新IP到DNS失败：{error}",
                    "updating_ip_to_dns_failed_2": "更新IP到DNS失败。\n状态码：{status_code}，详细：{result_text}",
                },
            },
            "configure_button": "配置",
            "refresh_ip_list_button": "刷新本机外部IP列表",
            "update_ip_button": "更新IP到DNS",
        },
        "configure_dialog": {
            "window_title": "配置界面",
            "record_info_settings_tab": {
                "tab_title": "记录信息设置",
                "record_info_group": {
                    "labels": {
                        "api_token": "API 口令: ",
                        "zone_id": "区域 ID: ",
                        "record_id": "记录 ID: ",
                        "domain_name": "域名: "
                    },
                    "edits_help_texts": {
                        "api_token": "请输入API Token",
                        "zone_id": "请输入区域 ID",
                        "record_id": "请输入记录 ID",
                        "domain_name": "请输入域名"
                    }
                }
            },
            "misc_settings_tab": {
                "tab_title": "其他设置",
                "proxy_group": {
                    "proxy_settings": "网络代理设置",
                    "proxy_mode": "代理模式",
                    "proxy_mode_off": "无代理",
                    "proxy_mode_auto": "自动代理",
                    "proxy_mode_system": "系统代理",
                    "proxy_mode_manual": "手动代理",
                    "manual_proxy_settings": "手动代理设置",
                    "proxy_url": "代理URL: ",
                    "proxy_override": "排除代理: "
                }
            },
            "about_tab": {
                "tab_title": "关于",
                "check_update": {
                    "check_update": "检查更新",
                    "is_latest": "当前已是最新版本",
                    "check_failed": "检查更新失败: {error_message}",
                    "found_update": "发现新版本: {new_version}"
                }
            }
        }
    }
}
# Languages
# example_string_of_lang = "{}".format(__package__.split('.')[-1])

# language_loaded_no_switch = "语言 {lang} 已加载，无需切换。"
# language_changed_to_str1 = "语言切换为 {lang}, 模块: {module}。"
# language_changed_to_str2 = "语言从 {last_lang} 切换为 {lang}, 模块名称: {module_name}。"

# Warnings
# warning_no_file_and_prompt_default = "警告: 未找到配置文件。提示：默认配置文件是 {default_ini_config_file}。"

namespace: Namespace
if not getattr(sys.modules[__name__], "namespace", None):
    namespace = Namespace(**string_dict)
# namespace = Namespace(**string_dict)
# Errors
