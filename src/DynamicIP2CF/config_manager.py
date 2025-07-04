from typing import Union
import os.path as osp
import configparser


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
        ip_version = config.get("Cloudflare", "ip_version")
        ip = config.get("Cloudflare", "ip")
        API_TOKEN = config.get("Cloudflare", "API_TOKEN")
        ZONE_ID = config.get("Cloudflare", "ZONE_ID")
        RECORD_ID = config.get("Cloudflare", "RECORD_ID")
        DNS_NAME = config.get("Cloudflare", "DNS_NAME")
        return {"ip_version": ip_version, "ip": ip, "API_TOKEN": API_TOKEN, "ZONE_ID": ZONE_ID, "RECORD_ID": RECORD_ID, "DNS_NAME": DNS_NAME}

    def generate_record_info(self) -> None:
        config = self.config
        config.add_section("Cloudflare")
        config.set("Cloudflare", "ip_version", "v6")
        config.set("Cloudflare", "ip", "your_ip_address")
        config.set("Cloudflare", "API_TOKEN", "your_api_token")
        config.set("Cloudflare", "ZONE_ID", "your_zone_id")
        config.set("Cloudflare", "RECORD_ID", "your_record_id")
        config.set("Cloudflare", "DNS_NAME", "your_dns_name")

    def update_record_info(self, ip_version: str, ip: str, API_TOKEN: str, ZONE_ID: str, RECORD_ID: str, DNS_NAME: str):
        config = self.config
        config.set("Cloudflare", "ip_version", ip_version)
        config.set("Cloudflare", "ip", ip)
        config.set("Cloudflare", "API_TOKEN", API_TOKEN)
        config.set("Cloudflare", "ZONE_ID", ZONE_ID)
        config.set("Cloudflare", "RECORD_ID", RECORD_ID)
        config.set("Cloudflare", "DNS_NAME", DNS_NAME)

