from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
class H256():
    def __gen_hash(self,text):
        return generate_password_hash(text)
    def __verify_hash(self,hash,text):
        return check_password_hash(hash,text)
class securityOwn():
    __ownKey='noseClave'
    def verify_own(self,hash):
        return check_password_hash(hash,self.__ownKey)
class securityUsr(securityOwn):
    __usrKey='31416CLAVE'
    def verify_usr(self,hash):
        return check_password_hash(hash,self.__usrKey)
class Keys():
    generalKey='lACLAVE'
    
    