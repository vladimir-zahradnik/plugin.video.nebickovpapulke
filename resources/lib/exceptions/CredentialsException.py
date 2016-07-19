__author__ = 'bromix'

import ProviderException

class CredentialsException(ProviderException):
    def __int__(self, message):
        ProviderException.__init__(self, message)
        pass
    pass
