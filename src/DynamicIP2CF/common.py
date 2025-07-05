# share with all at runtime with no concern
import configparser
from DynamicIP2CF.config_manager import IniConfigManager


config_ini_path: str = "config.ini"
config_ini: configparser.ConfigParser
iniConfigManager: IniConfigManager


program_package_name: str = __package__
program_name: str = program_package_name
