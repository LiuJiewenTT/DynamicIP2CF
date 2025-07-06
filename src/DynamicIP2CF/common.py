# share with all at runtime with no concern

from DynamicIP2CF.common_static import *


from DynamicIP2CF.resource_manager import ResourceManager
resource_manager: ResourceManager
Rsv: ResourceManager.get_res_path


import configparser
from DynamicIP2CF.config_manager import IniConfigManager


config_ini_path: str = "config.ini"
config_ini: configparser.ConfigParser
iniConfigManager: IniConfigManager



