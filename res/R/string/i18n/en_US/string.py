import sys
from R.string.utils import Namespace

string_dict = {
    "language": {
        "example_string_of_lang": "{}".format(__package__.split('.')[-1]),
        "language_loaded_no_switch": "Language {lang} loaded, no switch required.",
        "language_changed_to_str1": "Language changed to {lang}, module: {module}.",
        "language_changed_to_str2": "Language changed from {last_lang} to {lang}, module_name: {module_name}.",
        "notices": {
            "preferred_lang_not_same_as_system_lang": "Notice: preferred language is not the same as system language."
        },
        "warnings": {
            "system_lang_not_recognized": "Warning: system language is not recognized, using default language."
        }
    },
    "config": {
        "ini": {
            "warnings": {
                "no_file_and_prompt_default": "Warning: no .ini format config file is loaded. The default config file is {default_ini_config_file}"
            }
        }
    },
    "cli": {
        "parser": {
            "description": "Update Cloudflare DNS record IP",
            "options_help": {
                "cli_mode": "Run in CLI mode",
                "cli_automated": "Run in CLI automated mode",
                "read_config_ini": "Read .ini format config file",
                "ip_version": "IP version, should be v4 or v6",
                "ip": "IP address to update",
                "api_token": "Cloudflare API token",
                "zone_id": "Cloudflare zone ID",
                "record_id": "Cloudflare DNS record ID",
                "domain_name": "DNS record's domain name to update",
                "generate_config_ini": "Generate config.ini file",
                "proxy_mode": "Proxy mode, should be auto, system, manual, or off",
                "proxy_url": "Proxy URL, should be like http://127.0.0.1:8888",
                "override_list": "Override list, should be like 192.168.1.1;192.168.1.2. May not work very well.",
                "program_info": "Show program information and exit"
            }
        }
    },
    "gui": {
        "configure_dialog": {
            "window_title": "Configuration",
            "record_info_settings_tab": {
                "tab_title": "Record Info",
                "record_info_group": {
                    "labels": {
                        "api_token": "API Token: ",
                        "zone_id": "Zone ID: ",
                        "record_id": "Record ID: ",
                        "domain_name": "Domain Name: "
                    },
                    "edits_help_texts": {
                        "api_token": "Please enter API Token",
                        "zone_id": "Please enter Zone ID",
                        "record_id": "Please enter Record ID",
                        "domain_name": "Please enter Domain Name"
                    }
                }
            },
            "misc_settings_tab": {
                "tab_title": "Misc",
                "proxy_group": {
                    "proxy_settings": "Network Proxy Settings",
                    "proxy_mode": "Proxy Mode",
                    "proxy_mode_off": "No Proxy",
                    "proxy_mode_auto": "Auto Proxy",
                    "proxy_mode_system": "System Proxy",
                    "proxy_mode_manual": "Manual Proxy",
                    "manual_proxy_settings": "Manual Proxy Settings",
                    "proxy_url": "Proxy URL: ",
                    "proxy_override": "Proxy Override: "
                }
            },
            "about_tab": {
                "tab_title": "About",
                "check_update": {
                    "check_update": "Check for updates",
                    "is_latest": "You are using the latest version.",
                    "check_failed": "Failed to check for updates: {error_message}",
                    "found_update": "Found new version: {new_version}"
                }
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
# language_loaded_no_switch = "Language {lang} loaded, no switch required."
# language_changed_to_str1 = "Language changed to {lang}, module: {module}."
# language_changed_to_str2 = "Language changed from {last_lang} to {lang}, module_name: {module_name}."

# Warnings
# warning_no_file_and_prompt_default = "Warning: no .ini format config file is loaded. The default config file is {default_ini_config_file}"

# Errors
