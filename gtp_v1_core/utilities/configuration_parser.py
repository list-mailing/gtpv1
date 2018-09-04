#       configuration_parser.py
#       
#       Copyright 2018 Rosalia d'Alessandro
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
# -*- coding: utf-8 -*-a

from configobj import ConfigObj, ConfigObjError

from gtp_v1_core.path_mgmt_messages.echo import EchoRequest, EchoResponse

from gtp_v1_core.commons.gtp_v1_commons import GTPmessageTypeDigit
from gtp_v1_core.utilities.utilities import logNormal, logErr, logOk, logWarn

##
## @brief  Class implementing a Configuration Parser
##
class parseConfigs(object):
    '''
    classdocs
    '''


    def __init__(self, config_file, verbose = True):
        '''
        Constructor
        '''
        self.__msgs = []
        if config_file is None or config_file is "":
            raise Exception("No config file provided")
        self.__cfg = config_file
        self.__configs = {'interface': None,
                   'base_message_list': [],
                   '3gpp_messages_list': [],
                   'IES': []}
        self.__gtp_port = 2152
        self.__verbose = verbose
        self.__parseConfigs()
        
    def __parseConfigs(self):
        confobj = ConfigObj(self.__cfg)
        
        if 'GENERIC' not in confobj.sections:
            raise ConfigObjError('Section GENERIC is required')
                
        if 'port' in confobj['GENERIC']:
            self.__gtp_port = int(confobj['GENERIC']['port']) 
        
       
        if 'num_msg' in confobj['GENERIC'] :
            self.__num_msg = int(confobj['GENERIC']['num_msg'])
        else :
            self.__num_msg = 1
            
        if 'sqn' in confobj['GENERIC'] :
            self.__sqn = int(confobj['GENERIC']['sqn'], 16)
        else:
            self.__sqn = 0x0000  
        self.__msgs = self.__create_messages(confobj)
              
    
    def __format_base_messages(self, confobj):
        if 'base_message_list' not in confobj['GENERIC']:
            logWarn("Base message list empty",
                    verbose = self.__verbose, 
                    TAG = "parseConfig")
            return []       
        self.__configs['base_message_list'] = confobj['GENERIC']['base_message_list']        
        msgs = []
        for msg_type in self.__configs['base_message_list']:
            if int(msg_type) == GTPmessageTypeDigit["echo-request"] :
                i = 0
                while i < self.__num_msg :                
                    msgs.append(EchoRequest(self.__sqn))
                    i += 1
            elif int(msg_type) == GTPmessageTypeDigit["echo-response"]  :
                i = 0
                while i < self.__num_msg :                 
                    msgs.append(EchoResponse(1))
                    i += 1                    
            else: 
                raise Exception("%s:%s - Invalid base msg type "
                                "%d"%(self.__class__.__name__, 
                                      "__format_base_messages",
                                      int(msg_type)))
        return msgs
    
    
    def __format_interface_msg(self, confobj):
        msgs = []
        if confobj is None:
            raise Exception("%s:%s - Configuration Object is None. "
                            %(self.__class__.__name__, "__format_interface_msg"))

        if '3gpp_messages_list' not in confobj['GENERIC']:
            logWarn("3gpp message list empty",
                    verbose = self.__verbose, 
                    TAG = "parseConfig")            
            return  [] 
        self.__configs['3gpp_messages_list'] = confobj['GENERIC']['3gpp_messages_list']
                 
        if 'IES' not in confobj.sections:
            raise ConfigObjError('Section IES is required')
        
        if 'interface' not in confobj['GENERIC']:
            raise ConfigObjError('Value "GENERIC.interface" is required')
        self.__configs['interface'] = confobj['GENERIC']['interface']

        for msg_type in self.__configs['3gpp_messages_list']:
            pass
        return msgs

    def __create_messages(self, confobj):
        msgs = []
        msgs.extend(self.__format_base_messages(confobj))
        msgs.extend(self.__format_interface_msg(confobj))
        return msgs
    
    def get_unpacked_messages(self):   
        return self.__msgs
    
    def get_gtp_port(self):
        return self.__gtp_port