import unittest

import discovery

class TestUtilsFunctions(unittest.TestCase):
    def test_getPhysicalLinks(self):
        links = discovery.MacDiscovery._getPhysLinks()
        self.assertGreater(len(links), 0)
        #print(links)

    def test_showDetailsOfPhysLink(self):
        for l in discovery.MacDiscovery._getPhysLinks():
            details = discovery.MacDiscovery._getLinkDetails(l)
            for det in details:
                self.assertGreater(len(det), 0)
                #print(det)

    def test_discoverDeviceBrdIp(self):
        out = discovery.MacDiscovery._discoverDeviceBrdIp()
        self.assertGreater(len(out), 0)
        #print(out)

    def test_getIpFromMac(self):
        md = discovery.MacDiscovery()
        print(md.getIpFromMac('48:55:19:c9:f7:79'))

if __name__ == '__main__':
    unittest.main()