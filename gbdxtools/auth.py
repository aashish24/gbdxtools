from gbdx_auth import gbdx_auth
from traitlets.config.configurable import SingletonConfigurable
import logging

class Interface(SingletonConfigurable):
    gbdx_connection = None
    root_url = 'https://geobigdata.io'

    def __init__(self, **kwargs):
        self.logger = logging.getLogger('gbdxtools')
        self.logger.setLevel(logging.ERROR)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.ERROR)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        self.logger.info('Logger initialized')
       
        
    def __call__(self, **kwargs):
        if 'host' in kwargs:
            self.root_url = 'https://%s' % kwargs.get('host')

        try:  
            if (kwargs.get('username') and kwargs.get('password') and
                    kwargs.get('client_id') and kwargs.get('client_secret')):
                self.gbdx_connection = gbdx_auth.session_from_kwargs(**kwargs)
            elif kwargs.get('gbdx_connection'):
                self.gbdx_connection = kwargs.get('gbdx_connection')
            elif self.gbdx_connection is None:
                # This will throw an exception if your .ini file is not set properly
                self.gbdx_connection = gbdx_auth.get_session(kwargs.get('config_file'))
            return self
        except Exception as err: 
            print(err)