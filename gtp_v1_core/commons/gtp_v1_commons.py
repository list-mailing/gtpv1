'''
Created on 14 Sep 2017

@author: lia
'''

import struct
import IPy


RESERVED_IE_TYPES = [0, 98, 101, 102, 122, 130, 161]
RESERVED_IE_TYPES.extend(range(4,51))
RESERVED_IE_TYPES.extend(range(52,71))
RESERVED_IE_TYPES.extend(range(187,255))

DEBUG = 0

RATTypeStr = {
    1 :"UTRAN",
    2 : "GERAN",
    3 : "WLAN",
    4 : "GAN",
    5 : "HSPA Evolution",  
    6: "E-UTRAN", 
}

RATTypeDigit = {
    "UTRAN" : 1,
    "GERAN" : 2,
    "WLAN" : 3,
    "GAN" : 4,
    "HSPA Evolution" : 5,
    "E-UTRAN" : 6,  
}

#TS 29.274 Table 6.1-1
GTPmessageTypeStr = {
    1: "echo-request",
    2: "echo-response",
    16: "create-pdp-context-request",
    17: "create-pdp-context-response"     
}


GTPmessageTypeDigit = {
    "echo-request" : 1,
    "echo-response" : 2,
    "create-pdp-context-request" : 16,
    "create-pdp-context-response" : 17,    

}
        
class MobileNetworkIdentifier:
    def __init__(self, mcc = '222', mnc = '01'):
        self.__mcc = mcc
        if len(mnc) == 2 :
            mnc += "f"
        self.__mnc = mnc
                    
    def get_packed_val(self):
        hex_val =  self.__mcc[1]
        hex_val += self.__mcc[0]
        hex_val += self.__mnc[2]
        hex_val += self.__mcc[2]
        hex_val += self.__mnc[1]
        hex_val += self.__mnc[0]
        return bytearray.fromhex(hex_val)   
          
VERSION="0.1"

GTP_PORT = 2152

PADDING = 0x0000 #2 bytes        
COMMON_FLAGS = 0X94000160 # 4 BYTES
EVOLVED_ALLOCATION = 0Xbf000149 # 4 bytes       