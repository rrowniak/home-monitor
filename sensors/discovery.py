import utils

class MacDiscovery:
    ''' This class contains logic which allows figuring out an IP address based on a MAC address.'''
    
    def __init__(self):
        self.cache = {}
        MacDiscovery._buildArpCache()

    def invalidateCache(self):
        self.cache = {}

    def getIpFromMac(self, mac):
        # check internal cache first
        if mac in self.cache.keys():
            return self.cache[mac]
        
        # check if there is corresponsing entry in the arp cache
        ip = MacDiscovery._getIPfromArp(mac)
        if ip is None:
            # try rebuilding cache
            MacDiscovery._buildArpCache()
            ip = MacDiscovery._getIPfromArp(mac)
            if ip is None:
                # an atomic option, will take a few seconds
                MacDiscovery._buildArpCache(hard_way=True)
                ip = MacDiscovery._getIPfromArp(mac)
        if ip is not None:
            self.cache[mac] = ip
            return ip
        return None

    @staticmethod
    def _getPhysLinks():
        """ Returns a list of physical network interfaces"""
        """ E.g. ['enx9cebe843ba09', 'wlp2s0']"""
        """"""
        cmd = "ls -l /sys/class/net/ | tail -n +2 | grep -v virtual | awk '{print $9}'"
        # example output:
        # enx9cebe843ba09
        # wlp2s0
        return utils.getListFromShellCmd(cmd)

    @staticmethod
    def _getLinkDetails(link):
        """ Returns details related to a given physical interface"""
        """ E.g. ['3: wlp2s0    inet 192.170.8.101/24 brd 192.170.8.255 scope global dynamic noprefixroute wlp2s0\\       valid_lft 85849sec preferred_lft 85849sec']"""
        cmd = f"ip -o addr show dev {link} | grep 'inet '"
        # example output:
        # 3: wlp2s0    inet 192.170.8.101/24 brd 192.170.8.255 scope global dynamic noprefixroute wlp2s0\       valid_lft 85915sec preferred_lft 85915sec
        return utils.getListFromShellCmd(cmd)

    @staticmethod
    def _discoverDeviceBrdIp():
        ''' Returns a list of available subnets and broadcast addresses'''
        brds = []
        links = MacDiscovery._getPhysLinks()
        for link in links:
            details = MacDiscovery._getLinkDetails(link)
            for det in details:
                tokens = det.split()

                if len(tokens) > 5 and tokens[4] == 'brd':
                    brds.append((tokens[3], tokens[5]))
        return brds

    @staticmethod
    def _buildUpArpCacheForDev(brdAddr):
        ''' Ping a broadcast address to build up the arp cache'''
        ''' ping <allow broadcast> <brdAddr> <count 1> <timeout 1s>'''
        utils.callCmd(['ping', '-b', brdAddr, '-c', '1', '-W', '1'])

    @staticmethod
    def _buildUpArpCacheForDevHardWay(inet):
        ''' F-Ping every address in the subnet to build up the arp cache'''
        ''' fping <generate addr list> <repear once> <cidr>'''
        utils.callCmd(['fping', '-g', '-r', '2', inet])

    @staticmethod
    def _buildUpArpCacheForDevHardestWay(inet):
        ''' http-ping every address in the subnet to build up the arp cache'''
        raise NotImplementedError()

    @staticmethod
    def _buildArpCache(hard_way=False):
        brds = MacDiscovery._discoverDeviceBrdIp()
        for brd in brds:
            if hard_way:
                MacDiscovery._buildUpArpCacheForDevHardWay(brd[0])
            else:
                MacDiscovery._buildUpArpCacheForDev(brd[1])

    @staticmethod
    def _getIPfromArp(mac):
        cmd = f"arp -a | grep '{mac}' | awk '{{ print substr($2, 2, length($2)-2) }}'"
        out = utils.getListFromShellCmd(cmd)
        if len(out) != 1:
            return None
        else:
            return out[0]