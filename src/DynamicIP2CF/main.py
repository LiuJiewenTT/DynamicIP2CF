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
    args = parser.parse_args()

    flag_cli_mode = args.cli_mode
    flag_cli_automated = args.cli_automated
    flag_read_config_ini = args.read_config_ini

    record_info: Union[argparse.Namespace, None] = None
    record_info_dict: Dict[str, str] = {}
    record_info_list = []

    if flag_cli_mode:
        retv: SupportsInt = 0

        if flag_cli_automated:
            # cli自动模式

            required_args = ["ip_version", "ip", "api_token", "zone_id", "record_id", "dns_name"]

            if flag_read_config_ini:
                common.iniConfigManager = common.IniConfigManager(common.config_ini_path)
                common.iniConfigManager.read_config_file()
                record_info_dict = common.iniConfigManager.get_record_info()
                record_info_list = record_info.values()
                record_info = argparse.Namespace(**record_info_dict)

            # 检查必要参数是否存在
            for arg in required_args:
                if not getattr(args, arg):
                    print(f"Error: {arg} is required in CLI automated mode.")
                    exit(1)
                else:
                    record_info.update({arg: args.get(arg)})

            retv = cf_update_ip(record_info.ip_version, record_info.ip, record_info.api_token, record_info.zone_id, record_info.record_id, record_info.dns_name)
            exit(0 if retv else 1)
        else:
            # cli交互模式
            record_info_list = input_info_from_console()
            print(f'record_info_list: ', *record_info_list)
            retv = 1
            # retv = cf_update_ip(*record_info_list)
            if retv:
                print("Update IP success.")
                exit(0)
            else:
                print("Update IP failed.")
                exit(1)
    else:
        # GUI模式
        import DynamicIP2CF.GUI.main as gui_main
        gui_main.main()
        pass
