"""Publish a metric to graphite DB."""
import sys
import traceback
import logging

from kick.misc.docker import __get_host_hostname

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

GRAPHITE_SERVER_DEFAULT = 'sbg-stats.cisco.com'
GRAPHITE_PORT_DEFAULT = 2003
PREFIX = 'kick'

def publish_kick_metric(
        metric_name,
        value,
        moment=None,
        user=None,
        host_name=None,
        graphite_server=GRAPHITE_SERVER_DEFAULT,
        graphite_port=GRAPHITE_PORT_DEFAULT,
        prefix=PREFIX,
        protocol='tcp',
        log_errors=False):
    """Publish a KICK!

    metric based on its name and value. If moment is not set, use the
    current time. If user is not set, determine it with _get_username().
    If host_name is not set, determine it with __get_host_hostname().
    The structure of the resulting metric:
    kick.<user>.<host_name>.<metric_name>

    """
    
    try:
        import graphyte
        if not user:
            user = _get_username()
        if not host_name:
            host_name = __get_host_hostname()
        sender = graphyte.Sender(graphite_server, graphite_port, prefix=prefix, protocol=protocol)
        metric = '.'.join([user, host_name, metric_name])
        if moment:
            sender.send(metric, value, moment)
        else:
            sender.send(metric, value)
    except:
        if log_errors:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            LOGGER.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

def _get_username():
    """Get USER."""
    import getpass
    return getpass.getuser().replace('.', '_')
