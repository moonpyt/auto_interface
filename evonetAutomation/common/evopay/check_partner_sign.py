import hashlib
class CheckSign(object):
    def check_sign_post(self,method,url,participantID,msgID,datetime,signkey,data):

        # 获取签名（'post'+'\n'+url+'\n+'datetime+'\n'+signkey+'\n'+body）
        signstring = method+'\n'+url+'\n'+participantID+'\n'+msgID+'\n'+datetime+'\n'+data+'\n'+signkey

        signature = hashlib.sha256(signstring.encode("utf-8")).hexdigest()
        # 请求头
        header = {"SignType":"SHA256"}
        header.update({"Signature": signature, "DateTime": datetime,"msgID":msgID,"participantID":participantID})
        return header
    def check_sign_get(self,method,url,participantID,msgID,datetime,signkey):
        signstring = method + '\n' + url + '\n' + participantID + '\n' + msgID + '\n' + datetime + '\n'+ '\n'+ signkey

        signature = hashlib.sha256(signstring.encode("utf-8")).hexdigest()
        # 请求头
        header = {"SignType": "SHA256"}
        header.update({"Signature": signature, "DateTime": datetime, "msgID": msgID, "participantID": participantID})
        return header