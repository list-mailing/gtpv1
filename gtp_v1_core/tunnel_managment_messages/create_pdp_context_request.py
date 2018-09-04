'''
Created on Jul 14, 2018

@author: rosalia
'''
import sys
#sys.path.append('..')
from gtp_v1_core.commons.gtp_v1_msg_base import GTPV1MessageBase
from gtp_v1_core.commons.gtp_v1_commons import GTPmessageTypeDigit
from gtp_v1_core.commons.gtp_v1_information_element_base import *
##
## @brief  Class implementing a PDPCreateContextRequest message
##


class CreatePDPContextRequest(GTPV1MessageBase):
    '''
    classdocs
    '''

    ##
    ## @brief      Init method
    ##
    ## @param      self refers to the class itself
    ## @param      imsi victim IMSI   
    ## @param      mcc  mobile country code 
    ## @param      mnc  mobile network code 
    ## @param      lac  location area code
    ## @param      rac  routing area code         
    ## @param      tac  Type allocation Code       
    ## @param      apn  Access Point Name 
    ## @param      gsn  GGSN IP address   
    ## @param      IMEI International Mobile Equipment Identity  
    ## @param      msisdn MSISDN
    ##
    def __init__(self, imsi = "322885500003199", mcc = "322", mnc="89", 
                        lac = 2788, rac = 1, apn="umts",
                        dns1='127.0.0.1', dns2="127.0.0.2",
                        gsn="127.0.0.1", msisdn="393282270202",
                        geo_type = 0, imei="3518280450609004"):
        '''
        Constructor
        '''
   
        GTPV1MessageBase.__init__(self,
                    msg_type = GTPmessageTypeDigit['create-pdp-context-request'])
        
     
 
        self.add_ie(Imsi(imsi))
        self.add_ie(RatType(rat_type))
        fteid = FTeid(source_ip, interface)
        self.__fteid = fteid.get_teid()
        self.add_ie(fteid)
        self.add_ie(AccessPointName(apn))
        self.add_ie(UserLocationInformation(mcc = mcc, mnc = mnc, lac = lac, 
               rac = rac, tac = tac, ecgi = ecgi, 
               sac = sac, cgi = cgi))          
        self.add_ie(SelectionMode(selection_mode = sm))          
        self.add_ie(PDNAddressAllocation())
        self.add_ie(Msisdn(msisdn=phone))
        self.add_ie(MEIdentity(imei))
        self.add_ie(ProtocolConfigurationOptions(p_dns=p_dns, s_dns=s_dns))
        self.add_ie(Recovery())    
       
class CreatePDPContextResponse(GTPV1MessageBase):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
          