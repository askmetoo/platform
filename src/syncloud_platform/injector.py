import logging
from os import environ
from os.path import join

from syncloud_platform.auth.ldapauth import LdapAuth
from syncloud_platform.config.config import PlatformConfig
from syncloud_platform.config.user_config import PlatformUserConfig
from syncloud_platform.control.nginx import Nginx
from syncloud_platform.disks.hardware import Hardware
from syncloud_platform.disks.path_checker import PathChecker
from syncloud_platform.insider.device_info import DeviceInfo
from syncloudlib import logger

default_injector = None


def get_injector(debug=False):
    global default_injector
    if default_injector is None:
        config_dir = join(environ['SNAP'], 'config')
        default_injector = Injector(config_dir=config_dir, debug=debug)
    return default_injector


class Injector:
    def __init__(self, debug=False, config_dir=None):
        self.platform_config = PlatformConfig(config_dir=config_dir)

        if not logger.factory_instance:
            console = True if debug else False
            level = logging.DEBUG if debug else logging.INFO
            logger.init(level, console, join(self.platform_config.get_platform_log()))

        self.user_platform_config = PlatformUserConfig()

        self.device_info = DeviceInfo(self.user_platform_config)
        self.ldap_auth = LdapAuth(self.platform_config)
        self.nginx = Nginx(self.platform_config, self.device_info)

        self.path_checker = PathChecker(self.platform_config)
        self.hardware = Hardware(self.platform_config, self.path_checker)
