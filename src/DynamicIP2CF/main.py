from typing import Dict, Union, SupportsInt

import requests
import json
import locale
import os
import argparse

import DynamicIP2CF.common as common
import R
from DynamicIP2CF import programinfo
from DynamicIP2CF.utils_toplevel import *


class MultiLineVersionAction(argparse.Action):
    def __init__(self, option_strings, dest, version_text=None, **kwargs):
        self.version_text = version_text
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(self.version_text)
        parser.exit()


if __name__ == "__main__":
    common.resource_manager = common.ResourceManager()
    common.post_init_resource_manager()
    global Rsv, RsvP
    from DynamicIP2CF.common import Rsv, RsvP

    locale_lang, locale_encoding = locale.getdefaultlocale()
    env_lang = os.getenv("LANG", "").split(".")[0]
    preferred_lang: str
    flag_need_to_switch_lang: bool = False
    if env_lang:
        preferred_lang = env_lang
        flag_need_to_switch_lang = True
    elif not locale_lang:
        preferred_lang = R.string.default_lang
        flag_need_to_switch_lang = True
        print(R.string.language.warnings.system_lang_not_recognized)
    else:
        if locale_lang != R.string.default_lang:
            preferred_lang = locale_lang
            flag_need_to_switch_lang = True
        else:
            flag_need_to_switch_lang = False
            preferred_lang = R.string.default_lang

    # flag_need_to_switch_lang = True
    if flag_need_to_switch_lang:
        R.string.use_lang(locale_lang)
    if preferred_lang != locale_lang:
        print(R.string.language.notices.preferred_lang_not_same_as_system_lang)

    # R.string.use_lang('zh_CN')    # 测试用
    # print(R.string.config.ini.warnings.no_file_and_prompt_default.format(
    #     default_ini_config_file=common.config_ini_path))  # 测试用
    # R.string.use_lang('en_US')  # 测试用
    # print(R.string.config.ini.warnings.no_file_and_prompt_default.format(
    #     default_ini_config_file=common.config_ini_path))  # 测试用
    # R.string.use_lang('zh_CN')  # 测试用
    # print(R.string.config.ini.warnings.no_file_and_prompt_default.format(
    #     default_ini_config_file=common.config_ini_path))  # 测试用

    programinfo.init_program_info()

    parser = argparse.ArgumentParser(description=R.string.cli.parser.description)
    parser.add_argument("--cli-mode", action="store_true", help=R.string.cli.parser.options_help.cli_mode)
    parser.add_argument("--cli-automated", action="store_true", help=R.string.cli.parser.options_help.cli_automated)
    parser.add_argument("--read-config-ini", type=str, action="store", help=R.string.cli.parser.options_help.read_config_ini)
    parser.add_argument("--ip-version", type=str, help=R.string.cli.parser.options_help.ip_version)
    parser.add_argument("--ip", type=str, help=R.string.cli.parser.options_help.ip)
    parser.add_argument("--api-token", type=str, help=R.string.cli.parser.options_help.api_token)
    parser.add_argument("--zone-id", type=str, help=R.string.cli.parser.options_help.zone_id)
    parser.add_argument("--record-id", type=str, help=R.string.cli.parser.options_help.record_id)
    parser.add_argument("--domain-name", type=str, help=R.string.cli.parser.options_help.domain_name)
    parser.add_argument("--generate-config-ini", action="store_true", help=R.string.cli.parser.options_help.generate_config_ini)
    parser.add_argument("--proxy-mode", type=str, action="store", default="auto", help=R.string.cli.parser.options_help.proxy_mode)
    parser.add_argument("--proxy-url", type=str, action="store", help=R.string.cli.parser.options_help.proxy_url)
    parser.add_argument("--override-list", type=str, action="store", help=R.string.cli.parser.options_help.override_list)
    parser.add_argument("--version", action="version", version=programinfo.program_version_str)
    parser.add_argument("--program-info", action=MultiLineVersionAction, version_text=programinfo.programinfo_str1, help=R.string.cli.parser.options_help.program_info)
    args = parser.parse_args()

    flag_cli_mode = args.cli_mode
    flag_cli_automated = args.cli_automated
    flag_generate_config_ini = args.generate_config_ini

    read_config_ini_str = args.read_config_ini

    record_info: Dict[str, str] = {}
    record_info_list = []

    if flag_generate_config_ini:
        common.iniConfigManager = common.IniConfigManager(common.config_ini_path)
        common.iniConfigManager.generate_config_file()
        exit(0)

    config_ini_path: str = read_config_ini_str

    if not read_config_ini_str:
        # 为GUI模式启用缺省配置文件名
        if not flag_cli_mode:
            config_ini_path = common.config_ini_path
        else:
            print(R.string.config.ini.warnings.no_file_and_prompt_default.format(default_ini_config_file=common.config_ini_path))

    if config_ini_path:
        common.iniConfigManager = common.IniConfigManager(config_ini_path)
        common.iniConfigManager.read_config_file()
        record_info = common.iniConfigManager.get_record_info()

    if flag_cli_mode:
        retv: Union[bool, SupportsInt] = 0

        # 准备解析代理
        proxy_mode = args.proxy_mode
        proxy_url = args.proxy_url
        used_proxies = None
        override_list = args.override_list

        if proxy_mode == "auto":
            proxy_mode = "system"
        if proxy_mode == "manual":
            if proxy_url is None:
                raise ValueError("Error: proxy URL is required in manual proxy mode.")
            used_proxies = resolve_proxies_dict_from_string(proxy_url)
        elif proxy_mode == "system":
            used_proxies, override_list = get_windows_proxy_settings()
        elif proxy_mode == "off":
            used_proxies = None
            override_list = None
        else:
            raise ValueError("Error: invalid proxy mode.")

        print(f"proxy_mode: {proxy_mode}, used_proxies: {used_proxies}, override_list: {override_list}")

        if flag_cli_automated:
            # cli自动模式

            required_args = cf_required_info

            for arg in required_args:
                arg_value = getattr(args, arg)
                if arg_value is not None:
                    record_info[arg] = arg_value

            # 检查必要参数是否存在
            for arg in required_args:
                if record_info.get(arg) is None:
                    print("Error: {arg} is required in CLI automated mode.".format(arg=arg))
                    exit(1)

            record_info_list = record_info.values()

            # print(f'record_info_list: ', *record_info_list)
            # retv = True

            retv, status_code, result_text = cf_update_ip(*record_info_list, proxies=used_proxies, override_list=override_list)

            exit(0 if retv else 1)
        else:
            # cli交互模式
            print(programinfo.programinfo_str1)
            record_info_list = input_info_from_console()
            # print(f'record_info_list: ', *record_info_list)
            # retv = True
            retv, status_code, result_text = cf_update_ip(*record_info_list, proxies=used_proxies, override_list=override_list)
            if retv:
                print("Update IP success.")
                exit(0)
            else:
                print("Update IP failed. Status code: {status_code}, result text: {result_text}".format(status_code=status_code, result_text=result_text))
                exit(1)
    else:
        # GUI模式
        print(programinfo.programinfo_str1)
        import DynamicIP2CF.GUI.main as gui_main
        # gui_main.main()

        app = gui_main.QApplication([])
        window = gui_main.MainWindow()
        window.show()
        app.exec()
