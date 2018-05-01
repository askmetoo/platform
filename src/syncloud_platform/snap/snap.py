from syncloud_app import logger
import json
import requests_unixsocket
from syncloud_platform.sam.models import AppVersions, App

SOCKET = "http+unix://%2Fvar%2Frun%2Fsnapd.socket"


class Snap:

    def __init__(self, platform_config, info):
        self.info = info
        self.platform_config = platform_config
        self.logger = logger.get_logger('Snap')

    def update(self, release=None):
        return None
        
    def install(self, app_id):
        self.logger.info('snap install')
        session = requests_unixsocket.Session()
        response = session.post('{0}/v2/snaps/{1}'.format(SOCKET, app_id), json={'action': 'install'})
        self.logger.info("install response: {0}".format(response.text))
        

    def upgrade(self, app_id):
        self.logger.info('snap upgrade')
        session = requests_unixsocket.Session()
        response = session.post('{0}/v2/snaps/{1}'.format(SOCKET, app_id), data={'action': 'install'})
        self.logger.info("install response: {0}".format(response.text))
        
    def status(self):
        self.logger.info('snap changes')
        session = requests_unixsocket.Session()
        response = session.get('{0}/v2/changes?select=all'.format(SOCKET))
        self.logger.info("changes response: {0}".format(response.text))
        snapd_response = json.loads(response.text)
       
        if (snapd_response['status']) != 'OK':
            raise Exception(snapd_response['result']['message'])
            
        return len([change for change in snapd_response['result'] if not change['ready']]) > 0

    def remove(self, app_id):
        self.logger.info('snap remove')
        session = requests_unixsocket.Session()
        session.post('{0}/v2/snaps/{1}'.format(SOCKET, app_id), data={'action': 'remove'})

    def list(self):
        self.logger.info('snap list')
        session = requests_unixsocket.Session()
        response = session.get('{0}/v2/find?name=*'.format(SOCKET))
        self.logger.info("find response: {0}".format(response.text))
        return self.parse_response(response.text, lambda app: True)

    def user_apps(self):
        self.logger.info('snap user apps')
        session = requests_unixsocket.Session()
        response = session.get('{0}/v2/find?name=*'.format(SOCKET))
        self.logger.info("find response: {0}".format(response.text))
        return self.parse_response(response.text, lambda app: app['type'] == 'app')

    def installed_user_apps(self):
        session = requests_unixsocket.Session()
        response = session.get('{0}/v2/snaps'.format(SOCKET))
        self.logger.info("snaps response: {0}".format(response.text))
        return self.parse_response(response.text, lambda app: app['type'] == 'app')

    def installed_all_apps(self):
        session = requests_unixsocket.Session()
        response = session.get('{0}/v2/snaps'.format(SOCKET))
        self.logger.info("snaps response: {0}".format(response.text))
        return self.parse_response(response.text, lambda app: True)

    def get_app(self, app_id):
        session = requests_unixsocket.Session()
        response = session.get('{0}/v2/snaps/{1}'.format(SOCKET, app_id))
        self.logger.info("snap response: {0}".format(response.text))
        return response

    def parse_response(self, response_json, result_filter):
        response = json.loads(response_json)
        return [self.to_app(app) for app in response['result'] if result_filter(app)]

    def to_app(self, app):
    
        newapp = App()
        newapp.id = app['name']
        newapp.name = app['summary']
        newapp.url = self.info.url(newapp.id)
        newapp.icon = "http://apps.syncloud.org/releases/{0}/images/{1}-128.png".format(app['channel'], newapp.id)
        
        app_version = AppVersions()
        app_version.installed_version = app['version']
        app_version.current_version = app['version']
        app_version.app = newapp
        
        return app_version
