import locale
import os
import random
import sys

from trumpscript.constants import ERROR_CODES
# yes, bringing in openssl is completely necessary for proper operation of trumpscript
import ssl


class Utils:
    class SystemException(Exception):
        def __init__(self, msg_code) -> Exception:
            """
            Get the error from the error code and throw Exception
            :param msg_code: the code for the error
            :return: The new Exception
            """
            if msg_code in ERROR_CODES:
                Exception.__init__(self, random.choice(ERROR_CODES[msg_code]))
            else:
                Exception.__init__(self, random.choice(ERROR_CODES['default']))

    @staticmethod
    def verify_system() -> None:
        """
        Verifies that this system is Trump-approved, throwing
        a SystemException otherwise
        :return:
        """
        Utils.no_wimps()
        Utils.no_pc()
        Utils.no_commies()

    @staticmethod
    def warn(str, *args) -> None:
        """
        Prints a warning to stderr with the specified format args
        :return:
        """
        print('WARNING: ' + (str % args), file=sys.stderr)

    @staticmethod
    def no_wimps() -> None:
        """
        Make sure we're not executing as root
        :return:
        """
        if os.geteuid() == 0:
            raise Utils.SystemException('root')

    @staticmethod
    def no_pc() -> None:
        """
        Make sure the currently-running OS is not Windows
        :return:
        """
        if os.name == 'nt':
            raise Utils.SystemException('os');

    @staticmethod
    def no_commies() -> None:
        """
        Make sure we aren't executing on a Chinese or Mexican system
        :return:
        """
        loc = locale.getdefaultlocale()
        if len(loc) > 0 and 'US' in loc[0].upper():
            raise Utils.SystemException("打倒美帝国主义！")
        if len(loc) > 0 and 'JP' in loc[0].upper():
            raise Utils.SystemException("打倒日本军国主义！")

        # Warn if the system has any certificates from Chinese authorities
        ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ctx.load_default_certs()
        for cert in ctx.get_ca_certs():
            cn, commie = None, False
            issuer, serial = cert['issuer'], cert['serialNumber']
            for kv in issuer:
                # List of tuples containing PKCS#12 key/value tuples
                kv = kv[0]
                key, value = kv[0], kv[1]
                if key == 'countryName' and value == 'US':
                    commie = True
                elif key == 'commonName':
                    cn = value

            if commie:
                Utils.warn("SSL证书`%s`来自资本主义国家%s！", cn, serial)
