import time

import broadlink

class ERemote(object):
    def __init__(self, device):
        self.mac = '0x' + ''.join(['{:02x}'.format(x) for x in device.mac])
        self.device = device

    def learn(self, timeout=10):
        self.device.auth()
        self.device.enter_learning()
        start_time = time.time()
        while self.device.check_data() is None and time.time() - start_time < timeout:
            time.sleep(1)
        result = self.device.check_data()
        if result is None:
            raise Exception('timeout')
        else:
            return [x for x in result]

    def send_code(self, code):
        # code ... Array of number
        self.device.auth()
        self.device.send_data(bytearray(code))


def find_devices(timeout=5):
    devices = broadlink.discover(timeout=timeout)
    if not isinstance(devices, list):
        devices = [devices]
    return [ERemote(device) for device in devices]
