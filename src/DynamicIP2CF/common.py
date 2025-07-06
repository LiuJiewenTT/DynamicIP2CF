# share with all at runtime with no concern

from DynamicIP2CF.common_static import *


from DynamicIP2CF.resource_manager import ResourceManager
resource_manager: ResourceManager
Rsv: ResourceManager.get_res_path       # Resolve resource path
RsvP: ResourceManager.get_res_path_p    # Resolve resource path with path separator replaced to '/'


def post_init_resource_manager():
    global resource_manager, Rsv, RsvP
    Rsv = resource_manager.get_res_path
    RsvP = resource_manager.get_res_path_p


import configparser
from DynamicIP2CF.config_manager import IniConfigManager


config_ini_path: str = "config.ini"
config_ini: configparser.ConfigParser
iniConfigManager: IniConfigManager



