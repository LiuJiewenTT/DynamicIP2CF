from typing import Dict, Union, SupportsInt

import requests
import json
import argparse

import DynamicIP2CF.common as common
from DynamicIP2CF.utils_toplevel import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Cloudflare DNS record IP")
    parser.add_argument("--cli-mode", action="store_true", help="Run in CLI mode")
    parser.add_argument("--cli-automated", action="store_true", help="Run in CLI automated mode")
    parser.add_argument("--read-config-ini", action="store_true", help="Read config.ini file")
    parser.add_argument("--ip-version", type=str, help="IP version, should be v4 or v6")
    parser.add_argument("--ip", type=str, help="IP address to update")
    parser.add_argument("--api-token", type=str, help="Cloudflare API token")
    parser.add_argument("--zone-id", type=str, help="Cloudflare zone ID")
    parser.add_argument("--record-id", type=str, help="Cloudflare DNS record ID")
    parser.add_argument("--dns-name", type=str, help="DNS name to update")
    parser.add_argument("--generate-config-ini", action="store_true", help="Generate config.ini file")
    parser.add_argument("--proxy-mode", type=str, action="store_value", help="Proxy mode, should be auto, system, manual, or off")
    parser.add_argument("--proxy-url", type=str, action="store_value", help="Proxy URL, should be like http://127.0.0.1:8888")
    parser.add_argument("--override-list", type=str, action="store_value", help="Override list, should be like 192.168.1.1,192.168.1.2")
    args = parser.parse_args()

    flag_cli_mode = args.cli_mode
    flag_cli_automated = args.cli_automated
    flag_read_config_ini = args.read_config_ini
    flag_generate_config_ini = args.generate_config_ini

    record_info: Dict[str, str] = {}
    record_info_list = []

    if flag_generate_config_ini:
        common.iniConfigManager = common.IniConfigManager(common.config_ini_path)
        common.iniConfigManager.generate_config_file()
        exit(0)

    # 准备解析代理
    proxy_mode = args.proxy_mode
    proxy_url = args.proxy_url
    override_list = args.override_list
    # more...

    if flag_cli_mode:
        retv: Union[bool, SupportsInt] = 0

        if flag_cli_automated:
            # cli自动模式

            required_args = cf_required_info

            if flag_read_config_ini:
                common.iniConfigManager = common.IniConfigManager(common.config_ini_path)
                common.iniConfigManager.read_config_file()
                record_info = common.iniConfigManager.get_record_info()
            else:
                for arg in required_args:
                    record_info[arg] = getattr(args, arg)

            # 检查必要参数是否存在
            for arg in required_args:
                if record_info.get(arg) is None:
                    print(f"Error: {arg} is required in CLI automated mode.")
                    exit(1)

            record_info_list = record_info.values()

            # print(f'record_info_list: ', *record_info_list)
            # retv = True

            retv, status_code, result_text = cf_update_ip(*record_info_list)

            exit(0 if retv else 1)
        else:
            # cli交互模式
            record_info_list = input_info_from_console()
            # print(f'record_info_list: ', *record_info_list)
            # retv = True
            retv, status_code, result_text = cf_update_ip(*record_info_list)
            if retv:
                print("Update IP success.")
                exit(0)
            else:
                print("Update IP failed. Status code: {status_code}, result text: {result_text}".format(status_code=status_code, result_text=result_text))
                exit(1)
    else:
        # GUI模式
        import DynamicIP2CF.GUI.main as gui_main
        gui_main.main()
        pass
