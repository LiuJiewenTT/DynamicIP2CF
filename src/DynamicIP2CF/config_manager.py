from typing import Union, Tuple, List, Dict
import os.path as osp
import configparser

import NetToolKit.local_info


class ConfigManager:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_config_file(self):
        if self.file_path is None:
            raise ValueError("Config file path is not provided")
        if not osp.exists(self.file_path):
            raise FileNotFoundError(f"Config file \"{self.file_path}\" not found")

    def update_config_file(self):
        if self.file_path is None:
            raise ValueError("Config file path is not provided")


class IniConfigManager(ConfigManager):

    def __init__(self, file_path: Union[str, None], config: Union[configparser.ConfigParser, None] = None):
        super().__init__(file_path)
        if config is None:
            self.config = configparser.ConfigParser()
        else:
            self.config = config

    def read_config_file(self):
        super().read_config_file()
        self.config.read(self.file_path)
        return self.config

    def generate_config_file(self):
        self.generate_record_info()

        with open(self.file_path, "w") as f:
            self.config.write(f)

    def update_config_file(self):
        super().update_config_file()
        with open(self.file_path, "w") as f:
            self.config.write(f)

    def get_record_info(self):
        config = self.config
        if config is None:
            raise ValueError("Config is not provided")

        ip_version = config.get("Cloudflare", "ip_version")
        ip = config.get("Cloudflare", "ip")
        API_TOKEN = config.get("Cloudflare", "api_token")
        ZONE_ID = config.get("Cloudflare", "zone_id")
        RECORD_ID = config.get("Cloudflare", "record_id")
        DNS_NAME = config.get("Cloudflare", "dns_name")
        return {"ip_version": ip_version, "ip": ip, "api_token": API_TOKEN, "zone_id": ZONE_ID, "record_id": RECORD_ID, "dns_name": DNS_NAME}

    def generate_record_info(self) -> None:
        config = self.config
        config.add_section("Cloudflare")
        config.set("Cloudflare", "ip_version", "v6")
        config.set("Cloudflare", "ip", "your_ip_address")
        config.set("Cloudflare", "api_token", "your_api_token")
        config.set("Cloudflare", "zone_id", "your_zone_id")
        config.set("Cloudflare", "record_id", "your_record_id")
        config.set("Cloudflare", "dns_name", "your_dns_name")

    def update_record_info(self, ip_version: str, ip: str, API_TOKEN: str, ZONE_ID: str, RECORD_ID: str, DNS_NAME: str):
        config = self.config
        config.set("Cloudflare", "ip_version", ip_version)
        config.set("Cloudflare", "ip", ip)
        config.set("Cloudflare", "api_token", API_TOKEN)
        config.set("Cloudflare", "zone_id", ZONE_ID)
        config.set("Cloudflare", "record_id", RECORD_ID)
        config.set("Cloudflare", "dns_name", DNS_NAME)

    def get_proxy_info(self) -> Dict[str, Union[str, None]]:
        config = self.config
        if config is None:
            raise ValueError("Config is not provided")

        proxy_mode: str
        proxy_url: str
        proxy_override: str

        proxy_mode = config.get("Proxy", "mode", fallback="auto")
        proxy_url = config.get("Proxy", "url", fallback=None)
        proxy_override = config.get("Proxy", "override", fallback=None)
        return {"proxy_mode": proxy_mode, "proxy_url": proxy_url, "proxy_override": proxy_override}

    def resolve_proxy_info(self, proxy_mode: str, proxy_url: str, proxy_override: str) -> Tuple[Union[Dict[str, str], None], Union[List[str], None]]:
        if proxy_mode is None:
            proxy_mode = "off"
        if proxy_mode == "auto":
            proxy_mode = "system"
        if proxy_mode == "off":
            return None, None
        elif proxy_mode == "system":
            proxy_url, proxy_override = NetToolKit.local_info.get_windows_proxy_settings()
            if proxy_url is None:
                proxy_override = None
            return proxy_url, proxy_override
        elif proxy_mode == "manual":
            return NetToolKit.local_info.resolve_proxies_dict_from_string(proxy_url), proxy_override.split(";") if proxy_override else None
        else:
            raise ValueError(f"Invalid proxy mode: {proxy_mode}")

    def get_resolved_proxy_info(self):
        return self.resolve_proxy_info(**self.get_proxy_info())

