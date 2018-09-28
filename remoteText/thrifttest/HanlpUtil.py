from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from participle import HanlpUtilService
import threading

class HanlpUtil(object):

    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(HanlpUtil,"_instance"):
            with HanlpUtil._instance_lock:
                if not hasattr(HanlpUtil,"_instance"):
                    HanlpUtil._instance = object.__new__(cls)
                    transport = TSocket.TSocket('10.116.19.195',7099)
                    transport = TTransport.TBufferedTransport(transport)
                    protocol = TBinaryProtocol.TBinaryProtocol(transport)
                    transport.open()
                    HanlpUtil._client = HanlpUtilService.Client(protocol)
        return HanlpUtil._instance

    def seg(self,text):
        return self._client.seg(text)