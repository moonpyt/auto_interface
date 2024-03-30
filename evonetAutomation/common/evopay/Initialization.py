import json

class initialization(object):
    def __init__(self,common_params_conf,common_params_body):
        self.common_params_conf = common_params_conf     # read common_params
        self.common_params_body = common_params_body



    def init_body(self,csv_body):
        self.csv_body = csv_body
        if self.csv_body:
            self.csv_data = json.loads(csv_body)
            csv_data_solo = {}
            self.csv_data_solo = self.extract(self.csv_data,csv_data_solo)
            # extract csv body
            common_params_data_solo = {}
            common_params_data_solo = self.extract(self.common_params_body, common_params_data_solo)
            # extract common body


            for item in csv_data_solo:
                common_params_data_solo[item] = csv_data_solo[item]
            # customize body
            self.common_params_body = self.recombination(common_params_data_solo)

        return self.common_params_body

    def ini_conf(self,csv_conf):
        if csv_conf:
            self.csv_conf = json.loads(csv_conf,encoding='utf-8')
            for item in self.csv_conf:
                if self.csv_conf[item]  == 'delete':
                    del self.common_params_conf[item]
                else:
                    self.common_params_conf[item] = self.csv_conf[item]
        return self.common_params_conf


    def extract(self,dict_in, dict_out):
        for key, value in dict_in.items():

            if isinstance(value, dict):  # If value itself is dictionary
                if key == "mopToken":
                    value["valuecopy"] = value.pop("value")
                self.extract(value, dict_out)
            elif isinstance(value, str):
                # Write to dict_out
                dict_out[key] = value
        return dict_out

    def recombination(self,dict_in):
        # combine request body
        dict_out = {}
        if 'userData' in self.common_params_body and self.csv_data.get('userData')!='delete' :

            if 'wopUserReference' in dict_in:
                   if self.csv_data.get('userData'):
                        if self.csv_data.get('userData').get('wopUserReference') != 'delete':
                            dict_out.setdefault('userData',{})['wopUserReference'] = dict_in['wopUserReference']

            if 'evonetUserReference' in dict_in :
                    if self.csv_data.get('userData'):
                        if self.csv_data.get('userData').get('evonetUserReference')!='delete':
                            dict_out.setdefault('userData', {})['evonetUserReference'] = dict_in['evonetUserReference']

            if ('wopUserReference' in dict_in) and ('evonetUserReference' in dict_in) :
                    if self.csv_data.get('userData'):
                        if (self.csv_data.get('userData').get('wopUserReference')=='delete') and (self.csv_data['userData']['evonetUserReference']=='delete'):
                            dict_out['userData']={}
                    else:
                        dict_out.setdefault('userData', {})['wopUserReference'] = dict_in['wopUserReference']
                        dict_out.setdefault('userData', {})['evonetUserReference'] = dict_in['evonetUserReference']


            if 'wopToken' in dict_in :
                dict_out.setdefault('userData', {})['wopToken'] = dict_in['wopToken']



        if 'mopToken' in self.common_params_body:
            if "valuecopy" in dict_in:
                dict_out.setdefault('mopToken', {})['value'] = dict_in['valuecopy']
        if 'transAmount' in self.common_params_body:
            if 'currency' in dict_in:
                dict_out.setdefault('transAmount', {})['currency'] = dict_in['currency']
            if 'value' in dict_in:
                dict_out.setdefault('transAmount', {})['value'] = dict_in['value']
        if 'storeInfo' in self.common_params_body:
            if 'id' in dict_in:
                dict_out.setdefault('storeInfo',{})['id'] = dict_in['id']
            if 'localName' in dict_in:
                dict_out.setdefault('storeInfo',{})['localName'] = dict_in['localName']
            if 'mcc' in dict_in:
                dict_out.setdefault('storeInfo',{})['mcc'] = dict_in['mcc']
        if 'brandID' in dict_in:
            dict_out['brandID'] = dict_in['brandID']
        if 'mopOrderNumber' in dict_in:
            dict_out['mopOrderNumber'] = dict_in['mopOrderNumber']
        if 'mopTransTime' in dict_in:
            dict_out['mopTransTime'] = dict_in['mopTransTime']
        if 'qrPayload' in dict_in:
            dict_out['qrPayload'] = dict_in['qrPayload']
        if 'location' in dict_in:
            dict_out['location'] = dict_in['location']
        if 'deviceID' in dict_in:
            dict_out['deviceID'] = dict_in['deviceID']
        if 'evonetReference' in dict_in:
            dict_out['evonetReference'] = dict_in['evonetReference']
        if 'wopOrderNumber' in dict_in:
            dict_out['wopOrderNumber'] = dict_in['wopOrderNumber']
        if 'wopTransTime' in dict_in:
            dict_out['wopTransTime'] = dict_in['wopTransTime']
        if 'evonetOrderNumber' in dict_in:
            dict_out['evonetOrderNumber'] = dict_in['evonetOrderNumber']
        if 'evonetOrderCreateTime' in dict_in:
            dict_out['evonetOrderCreateTime'] = dict_in['evonetOrderCreateTime']
        if 'userPayTime' in dict_in:
            dict_out['userPayTime'] = dict_in['userPayTime']
        if 'originalEvonetOrderNumber' in dict_in:
            dict_out['originalEvonetOrderNumber'] = dict_in['originalEvonetOrderNumber']
        if 'transResult' in self.common_params_body:
            if 'status' in dict_in:
                dict_out.setdefault('transResult',{})['status'] = dict_in['status']
            if 'message' in dict_in:
                dict_out.setdefault('transResult',{})['message'] = dict_in['message']

        if 'sendCurrency' in dict_in:
            dict_out['sendCurrency'] = dict_in['sendCurrency']
        if 'receiveCurrency' in dict_in:
            dict_out['receiveCurrency'] = dict_in['receiveCurrency']
        if 'participantID' in dict_in:
            dict_out['participantID'] = dict_in['participantID']
        return dict_out



if __name__ == '__main__':
    init = initialization()
    a = init.init_body()
    print(a)

