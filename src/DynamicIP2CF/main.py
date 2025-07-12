from typing import Dict, Union, SupportsInt

import requests
import json
import argparse

import DynamicIP2CF.common as common
from DynamicIP2CF import programinfo
from DynamicIP2CF.utils_toplevel import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Cloudflare DNS record IP")
    parser.add_argument("--cli-mode", action="store_true", help="Run in CLI mode")
    parser.add_argument("--cli-automated", action="store_true", help="Run in CLI automated mode")
    parser.add_argument("--read-config-ini", type=str, action="store", help="Read .ini format config file")
    parser.add_argument("--ip-version", type=str, help="IP version, should be v4 or v6")
    parser.add_argument("--ip", type=str, help="IP address to update")
    parser.add_argument("--api-token", type=str, help="Cloudflare API token")
    parser.add_argument("--zone-id", type=str, help="Cloudflare zone ID")
    parser.add_argument("--record-id", type=str, help="Cloudflare DNS record ID")
    parser.add_argument("--dns-name", type=str, help="DNS name to update")
    parser.add_argument("--generate-config-ini", action="store_true", help="Generate config.ini file")
    parser.add_argument("--proxy-mode", type=str, action="store", help="Proxy mode, should be auto, system, manual, or off", default="auto")
    parser.add_argument("--proxy-url", type=str, action="store", help="Proxy URL, should be like http://127.0.0.1:8888")
    parser.add_argument("--override-list", type=str, action="store", help="Override list, should be like 192.168.1.1;192.168.1.2. May not work very well.")
    args = parser.parse_args()

    flag_cli_mode = args.cli_mode
    flag_cli_automated = args.cli_automated
    flag_generate_config_ini = args.generate_config_ini

    read_config_ini_str = args.read_config_ini

    programinfo.init_program_info()
    print(programinfo.programinfo_str1)

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
            print("Warning: no .ini format config file is loaded.")

    if config_ini_path:
        common.iniConfigManager = common.IniConfigManager(config_ini_path)
        common.iniConfigManager.read_config_file()
        record_info = common.iniConfigManager.get_record_info()

    common.resource_manager = common.ResourceManager()
    common.post_init_resource_manager()

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
                    print(f"Error: {arg} is required in CLI automated mode.")
                    exit(1)

            record_info_list = record_info.values()

            # print(f'record_info_list: ', *record_info_list)
            # retv = True

            retv, status_code, result_text = cf_update_ip(*record_info_list, proxies=used_proxies, override_list=override_list)

            exit(0 if retv else 1)
        else:
            # cli交互模式
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
        import DynamicIP2CF.GUI.main as gui_main
        # gui_main.main()

        app = gui_main.QApplication([])
        window = gui_main.MainWindow()
        window.show()
        app.exec()
