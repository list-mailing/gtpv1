'''
Created on 20 Nov 2017

@author: lia
'''
import sys
#sys.path.append('..')
from gtp_v1_core.commons.gtp_v1_msg_base import GTPV1MessageBase
from gtp_v1_core.commons.gtp_v1_commons import GTPmessageTypeDigit
from gtp_v1_core.commons.gtp_v1_information_element_base import Recovery

class EchoRequest(GTPV1MessageBase):
    '''
    classdocs
    '''


    def __init__(self, seq_num = 0x00):
        '''
        Constructor
        '''
        GTPV1MessageBase.__init__(self, 
                                msg_type = GTPmessageTypeDigit['echo-request'],
                                sequence = seq_num
                                )

                  
        
        
class EchoResponse(GTPV1MessageBase):
    '''
    classdocs
    '''


    def __init__(self, seq_num):
        '''
        Constructor
        '''
        GTPV1MessageBase.__init__(self, 
                                msg_type = GTPmessageTypeDigit['echo-response'],
                                sequence = seq_num
                                ) 
     
        
   