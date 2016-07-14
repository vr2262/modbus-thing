import logging

import pymodbus.client.sync


OUTLETS = {
    1: {'coil': 300, 'amps': 202, 'watts': 222, 'kWh': 242},
    2: {'coil': 301, 'amps': 204, 'watts': 224, 'kWh': 244},
    3: {'coil': 302, 'amps': 206, 'watts': 226, 'kWh': 246},
    4: {'coil': 303, 'amps': 208, 'watts': 228, 'kWh': 248},
    5: {'coil': 304, 'amps': 210, 'watts': 230, 'kWh': 250},
    6: {'coil': 305, 'amps': 212, 'watts': 232, 'kWh': 252},
    7: {'coil': 306, 'amps': 214, 'watts': 234, 'kWh': 254},
    8: {'coil': 307, 'amps': 216, 'watts': 236, 'kWh': 256},
    9: {'coil': 308, 'amps': 218, 'watts': 238, 'kWh': 258},
    10: {'coil': 309, 'amps': 220, 'watts': 240, 'kWh': 260}
}

pymodbus.constants.Defaults.Timeout = 0.5
pymodbus.constants.Defaults.Retries = 1


CLIENTS = dict()


def get_client(ip):
    if ip is None:
        raise ValueError('IP address is None')
    if ip not in CLIENTS:
        CLIENTS[ip] = pymodbus.client.sync.ModbusTcpClient(ip)
    return CLIENTS[ip]

def set_log_level(level=logging.DEBUG):
    logging.basicConfig()
    logging.getLogger().setLevel(level)


def read_register_bytes(client, address):
    """Read two 16-bit values starting at the given address.
    
    The modbus specification says that at an address is actually one less than
    its label (hence the address -= 1).
    Each register holds a 16-bit (2-byte) value, and for our purposes the data
    are stored in two adjacent registers.
    """
    address -= 1
    results = client.read_holding_registers(address=address, count=2, unit=1)
    return results.registers
