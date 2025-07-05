import requests
import json
import configparser


cf_required_info = ["ip_version", "ip", "api_token", "zone_id", "record_id", "dns_name"]


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


def input_info_from_console():
    ip_version = input("IP version (v4/v6): ")
    ip = input("IP address: ")
    API_TOKEN = input("Cloudflare API token: ")
    ZONE_ID = input("Cloudflare zone ID: ")
    RECORD_ID = input("Cloudflare DNS record ID: ")
    DNS_NAME = input("DNS name to update: ")
    return ip_version, ip, API_TOKEN, ZONE_ID, RECORD_ID, DNS_NAME

