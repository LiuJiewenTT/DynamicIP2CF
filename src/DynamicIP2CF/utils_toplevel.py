# 顶层utils，主要包含业务类代码
from typing import Dict, List, Union

import requests
from urllib.parse import urlparse
from NetToolKit.local_info import get_windows_proxy_settings, host_matches_override, resolve_proxies_dict_from_string
import json


cf_required_info = ["ip_version", "ip", "api_token", "zone_id", "record_id", "domain_name"]


def cf_update_ip(ip_version: str, ip: str, API_TOKEN: str, ZONE_ID: str, RECORD_ID: str, DOMAIN_NAME: str, proxies: Union[Dict[str, str], None]=None, override_list: Union[List[str], None]=None):
    # 数值检查
    if not ip_version:
        raise ValueError("ip_version should only be \"v4\" or \"v6\".")
    if not API_TOKEN:
        raise ValueError("API_TOKEN invalid value")
    if not ZONE_ID:
        raise ValueError("ZONE_ID invalid value")
    # if not RECORD_ID:
    #     raise ValueError("RECORD_ID invalid value")
    # if not DOMAIN_NAME:
    #     raise ValueError("DOMAIN_NAME invalid value")
    if not RECORD_ID and not DOMAIN_NAME:
        raise ValueError("RECORD_ID and DOMAIN_NAME cannot be both empty.")

    record_type = "AAAA" if ip_version == "v6" else ("A" if ip_version == "v4" else "")
    if record_type == "":
        raise ValueError("ip_version should only be \"v4\" or \"v6\".")

    # 构造Cloudflare API请求
    modify_url = "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"
    query_url = "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    query_params = {
        "type": record_type,
        "name": DOMAIN_NAME
    }
    modify_data = {
        "type": record_type,
        "name": DOMAIN_NAME,
        "content": ip,
        "ttl": 1,
        "proxied": False
    }

    used_proxies = {}

    dns_session = requests.Session()
    dns_session.headers.update(headers)

    if not proxies:
        dns_session.trust_env = False  # 禁用从环境变量读取代理
        used_proxies = None
        override_list = None
    else:
        parsed = urlparse("https://api.cloudflare.com/")
        host = parsed.hostname.lower()
        if proxies and not host_matches_override(host, override_list):
            used_proxies = proxies
        else:
            used_proxies = None  # 禁止用代理
            dns_session.trust_env = False

    query_url_filled = query_url.format(ZONE_ID=ZONE_ID)

    if RECORD_ID == "":
        print("Query URL for DNS records: {}".format(query_url_filled))
        response = dns_session.get(query_url_filled, params=query_params, proxies=used_proxies)
        if response.status_code == 200:
            records = response.json().get("result", [])
            if len(records) == 0:
                raise ValueError("No DNS record found.")
            elif len(records) > 1:
                raise ValueError("More than one DNS record found.")
            else:
                RECORD_ID = records[0]["id"]
                print("Found DNS record, {record_name} -> {record_content}, ID: {RECORD_ID}"
                      .format(record_name=records[0]['name'], record_content=records[0]['content'], RECORD_ID=RECORD_ID))
        else:
            raise ValueError(f"Failed to query DNS records: {response.status_code} {response.text}")

    # 发送更新请求
    modify_url_filled = modify_url.format(ZONE_ID=ZONE_ID, RECORD_ID=RECORD_ID)
    print("Modify URL for DNS record: {}".format(modify_url_filled))
    response = dns_session.put(modify_url_filled,
                               data=json.dumps(modify_data), proxies=used_proxies)

    # 输出结果
    print("Update IP {DOMAIN_NAME} -> {ip}".format(DOMAIN_NAME=DOMAIN_NAME, ip=ip))
    print(response.status_code, response.text)
    return response.status_code == 200, response.status_code, response.text


def input_info_from_console():
    ip_version = input("IP version (v4/v6): ")
    ip = input("IP address: ")
    API_TOKEN = input("Cloudflare API token: ")
    ZONE_ID = input("Cloudflare zone ID: ")
    RECORD_ID = input("Cloudflare DNS record ID: ")
    DOMAIN_NAME = input("DNS name to update: ")
    return ip_version, ip, API_TOKEN, ZONE_ID, RECORD_ID, DOMAIN_NAME

