import time
from py_openshowvar import openshowvar

class RemoteControlKUKA:

    def __init__(self, address="192.168.1.15", port=7000, debug=False):
        self.debug = debug
        self._client = openshowvar(address, port)
        if (not self._client.can_connect):
            raise RuntimeError("Unable to connect.")
            
    def __del__(self):
        self._client.close()

    def _read(self, identifier, debug=False):
        return self._client.read(identifier, debug=debug)
        
    def _write(self, identifier, value, debug=False):
        return self._client.write(identifier, value, debug=self.debug or debug)
        
    def get_pos(self):
        return self._read("$POS_ACT")
        
    def get_axis(self):
        return self._read("$AXIS_ACT")
        
    def is_idle(self):
        return b'0' == self._read("COM_ACTION")
        
    def _set_e6pos(self, e6pos):
        self._write("COM_E6POS",e6pos)
        
    def _set_e6axis(self, e6axis):
        self._write("COM_E6AXIS",e6axis)
        
    def _set_action(self, s_action):
        if (s_action == "PTP_E6POS"):
            a = 11
        elif (s_action == "LIN_E6POS"):
            a = 12
        elif (s_action == "PTP_E6AXIS"):
            a = 13
        else:
            raise NotImplementedError("Unknown action string.")
        self._write("COM_ACTION", str(a))

    def _wait(self, wait=True):
        while (wait and not self.is_idle()):
            time.sleep(0.1)

    def move_lin_e6pos(self, e6pos, block=True):
        self._set_e6pos(e6pos)
        self._set_action("LIN_E6POS")
        self._wait(block)

    def move_ptp_e6pos(self, e6pos, block=True):
        self._set_e6pos(e6pos)
        self._set_action("PTP_E6POS")
        self._wait(block)
    
    def move_ptp_e6axis(self, e6axis, block=False):
        self._set_e6axis(e6axis)
        self._set_action("PTP_E6AXIS")
        self._wait(block)
        
    def moveTo(self,axis, flag=False):
        self.move_ptp_e6axis(axis,flag)
        

    # if __name__ == '__main__':
    # rck = RemoteControlKUKA()
    # y = 135.903534
    # z = 691.804626