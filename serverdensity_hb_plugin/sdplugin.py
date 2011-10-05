import re
from pprint import pformat
from serverdensity.api import SDApi
from hippybot.hipchat import HipChatApi
from hippybot.decorators import directcmd

ip_re = re.compile('\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')

class Plugin(object):
    """Plugin to get alerts/stats for a server from serverdensity.com
    """

    _device_ids = {}
    _api = None
    @property
    def api(self):
        if self._api is None:
            config = self.bot._config['serverdensity']
            self._api = SDApi(
                config['account'],
                config['username'],
                config['password'],
                config['api_key'],
                api_version='1.3' # Pin it to version 1.3
            )
        return self._api

    @directcmd
    def alerts(self, mess, args):
        """Get the last 5 SD alerts
        """
        resp = self.api.alerts.getLast()
        if resp['status'] == 2:
            return resp['error']['message']
        return pformat(resp['data']['alerts'])

    @directcmd
    def metrics(self, mess, args):
        """Get latest SD metrics for an by IP, hostname or name
        """
        args = args.strip().split(' ')
        # Check for cached ID
        device = self._device_ids.get(args[0], None)
        if device is None and ip_re.search(args[0]) is not None:
            # Possibly an IP address
            resp = self.api.devices.getByIp({'ip': args[0]})
            if resp['status'] != 2:
                device = resp['data']['device']['device']['deviceId']
        if device is None:
            # Check if it's a hostname
            resp = self.api.devices.getByHostname({'hostName': args[0]})
            if resp['status'] != 2:
                device = resp['data']['device']['device']['deviceId']
            else:
                # Otherwise try a name
                resp = self.api.devices.getByName({'name': args[0]})
                if resp['status'] != 2:
                    device = resp['data']['device']['device']['deviceId']
        if device is None:
            # Nada, error
            return u'Unknown device "%s"' % (args[0],)
        else:
            if args[0] not in self._device_ids:
                # Cache the device ID if not already cached
                self._device_ids[args[0]] = device
            query = {'deviceId': device}
            if len(args) > 1:
                query['metricGroup'] = args[1]
            if len(args) > 2:
                query['metricName'] = args[2]
            return pformat(self.api.metrics.getLatest(query)['data']['latestMetrics']['metrics'])

    @directcmd
    def devices(self, mess, args):
        """Get a list of SD devices
        """
        resp = self.api.devices.list()
        if resp['status'] == 2:
            return resp['error']['message']
        return pformat(resp['data']['devices'])
