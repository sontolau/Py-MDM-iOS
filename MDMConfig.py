__author__ = 'sonto'

import ConfigParser

class MDMConfig:
    base_dir=''
    log='STDOUT'
    ca=''
    https_certificate=''
    https_private_key=''
    internal_server = ('localhost', 8888)
    max_packet_size = 1024
    db_info=('localhost', 8000, 'mdm')
    mobile_config='mdm_mobileconfig'
    identity_dir=None
    push_cert=None
    def __init__(self, path=''):
        config = ConfigParser.RawConfigParser()
        config.read(path)

        try:
            self.log = config.get('Server','log')
            self.ca  = config.get('Server','ca')
            self.base_dir = config.get('Server', 'basedir')
            self.internal_server = (config.get('Server', 'internal_host'),
                                config.getint('Server', 'internal_port'))

            self.https_certificate = config.get('Server', 'https_certificate')
            self.https_private_key = config.get('Server', 'https_private_key')
            self.max_packet_size   = config.getint('Server', 'max_packet_size')
            self.push_cert         = config.get('MDM', 'push_cert')
            self.db_info=(config.get('DB', 'host'),
                          config.getint('DB', 'port'),
                          config.get('DB', 'database'))

            self.mobile_config=config.get('MDM', 'mobile_config')
            self.identity_dir=config.get('MDM', 'identity_dir')
        except:
            pass