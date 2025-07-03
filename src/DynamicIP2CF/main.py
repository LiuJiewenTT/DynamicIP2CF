import requests
import json
import argparse


def cf_update_ip(ip_version: str, ip: str, API_TOKEN: str, ZONE_ID: str, RECORD_ID: str, DNS_NAME: str):
    # 数值检查
    if not ip_version:
        raise ValueError("ip_version should only be \"v4\" or \"v6\".")
    if not API_TOKEN:
        raise ValueError("API_TOKEN invalid value")
    if not ZONE_ID:
        raise ValueError("ZONE_ID invalid value")
    if not RECORD_ID:
        raise ValueError("RECORD_ID invalid value")
    if not DNS_NAME:
        raise ValueError("DNS_NAME invalid value")

    record_type = "AAAA" if ip_version == "v6" else ("A" if ip_version == "v4" else "")
    if record_type == "":
        raise ValueError("ip_version should only be \"v4\" or \"v6\".")

    # 构造Cloudflare API请求
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": record_type,
        "name": DNS_NAME,
        "content": ip,
        "ttl": 300,
        "proxied": False
    }

    # 发送更新请求
    response = requests.put(url, headers=headers, data=json.dumps(data))

    # 输出结果
    print(f"Update IP {DNS_NAME} -> {ip}")
    print(response.status_code, response.text)
    return response.status_code == 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Cloudflare DNS record IP")
    parser.add_argument("--cli-mode", action="store_true", help="Run in CLI mode")
    cli_mode = parser.parse_args().cli_mode
    if cli_mode:
        parser.add_argument("--cli-automated", action="store_true", help="Run in CLI automated mode")
        cli_automated = parser.parse_args().cli_automated
        if cli_automated:
            # cli自动模式
            parser.add_argument("--ip-version", type=str, required=True, help="IP version, should be v4 or v6")
            parser.add_argument("--ip", type=str, required=True, help="IP address to update")
            parser.add_argument("--api-token", type=str, required=True, help="Cloudflare API token")
            parser.add_argument("--zone-id", type=str, required=True, help="Cloudflare zone ID")
            parser.add_argument("--record-id", type=str, required=True, help="Cloudflare DNS record ID")
            parser.add_argument("--dns-name", type=str, required=True, help="DNS name to update")
            args = parser.parse_args()

            retv = cf_update_ip(args.ip_version, args.ip, args.api_token, args.zone_id, args.record_id, args.dns_name)
            exit(0 if retv else 1)
        else:
            # cli交互模式
            pass
    else:
        # GUI模式
        import DynamicIP2CF.GUI.main as gui_main
        gui_main.main()
        pass
