import netaddr
from tkinter import messagebox


class Ip_checker:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.ip_version = None
        self._ip_address = None
        self.check_ip_version()

    def check_ip_version(self):
        try:
            self._ip_address = (str(self.ip_address).split('/'))[0]
            self.ip_version = netaddr.IPAddress(self._ip_address).version
        except netaddr.core.AddrFormatError:
            messagebox.showerror("Error", "Invalid IP address format")

    def compress_ip(self) -> str:
        if self.ip_version == 4:
            return str(netaddr.IPNetwork(self.ip_address).cidr)
        elif self.ip_version == 6:
            return str(netaddr.IPNetwork(self.ip_address).cidr)
        else:
            return "Invalid IP version"

    def compress_ip_without_mask(self) -> str:
        if self.ip_version == 4:
            return str(netaddr.IPNetwork(self.ip_address).ip).split('/')[0]
        elif self.ip_version == 6:
            return str(netaddr.IPNetwork(self.ip_address).ip).split('/')[0]
        else:
            return "Invalid IP version"