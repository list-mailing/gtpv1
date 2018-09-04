#       gtp_v1_base_msg.py
#       
#       Copyright 2017 Rosalia d'Alessandro <rosalia.dalessandro@telecomitalia.it>
#

#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import random
import struct
#from gtp_v1_core.commons.gtp_v1_information_element_base import *
from gtp_v1_commons import GTPmessageTypeStr

'''
    8     7     6     5     4     3     2     1    Octets
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Version     | PT  | (*) | E   | E   | PN  |   1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                  Message Type                 |   2
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Message Length                |  3-4
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 TEID                          |  5-8
|                                               |
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Sequence Number               |  9-10
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   N-PDU Number                |   11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Next Extension Header Type                  |   12
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

class GTPV1MessageBase(object):
    '''
    classdocs
    '''


    def __init__(self, msg_type, sequence = 0x00, npdu = 0x00, neht = 0x00):
        '''
        Constructor
        '''
        if not GTPmessageTypeStr.has_key(msg_type) :
            raise Exception("invalid mesg_type: %s"%(msg_type))
        
        self.__p_flag = 0x01
        if sequence == 0x00 :
            self.__sequence_number = 0x01
        else :
            self.__sequence_number = sequence
        self.__teid = 0x00
        self.__hdr_len = 10
        self.npdu = npdu 
        if  npdu :
            self.__hdr_len += 1
        self.neht = neht
        if  neht :     
            self.__hdr_len += 1   
                 
        self.__packed_ie_len = 0
        self.__msg_type = int(msg_type)
        self.__version = 0x01
        
        self.__packed_ie= 0x00 # packed data containing all information elements
        self.__ie_array = []   # array containing all the information elements
 
    def get_msg_type(self):
        return self.__msg_type 
         
    def __get_packed_ies(self):
        self.__packed_ie = ''
        for ie in self.__ie_array:
            self.__packed_ie += ie.get_packed_ie()
        self.__packed_ie_len = len(self.__packed_ie)
   

    def add_ie(self, ie):
        if ie:
            self.__ie_array.append(ie)
        
    def get_length(self):
        return (self.__packed_ie_len + self.__hdr_len - 6)
              
    def get_hdr_length(self):
        return self.__hdr_len
    
    def get_packed_ie_length(self):
        return self.__packed_ie_len     

    def get_packed_ie(self):
        if self.__packed_ie == 0x00:
            self.__get_packed_ies()
        return self.__packed_ie
    
    def get_packed_header(self):
        msg_type = struct.pack("!B", self.__msg_type)
        flags = struct.pack("!B", (self.__version << 5) + 
                                (self.__p_flag << 4) + 2)
        msg_len = struct.pack("!H", self.get_length())
        sqn = struct.pack("!H", self.__sequence_number)

        out = flags + msg_type + msg_len
        out += struct.pack("!L",self.__teid)
        out += sqn 
        
        if self.npdu :
            npdu = struct.pack("!B", self.npdu)
            out += npdu
        if self.neht :
            neht = struct.pack("!B", self.neht)
            out += neht       
       
        return out    
    
    def get_message(self):
        # DO NOT CHANGE THIS ORDER
        # IT IS IMPORTANT FOR CORRECT MSG LEN CALCULATION
        payload = self.get_packed_ie()
        hdr = self.get_packed_header()
        return (hdr + payload)
    
    def get_teid(self):
        return self.__teid
    
    def set_packed_ie(self, packed_ie):
        self.__packed_ie = packed_ie
        self.__packed_ie_len = len(packed_ie)
    
    def set_teid(self, teid = bytearray(random.getrandbits(8) for i in range(3))):
        self.__teid = teid   
                 
    def set_sequence_number(self, sqn):
        self.__sequence_number = sqn

    

    