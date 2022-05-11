from ast import Return
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from security import securityOwn, securityUsr
import datetime
db = SQLAlchemy()

class User(db.Model,securityUsr):
    __tablename__ = "User"
    __id = db.Column(db.Integer, primary_key=True)
    __username = db.Column(db.String(50),unique = True,nullable=False)#Encriptar
    __email = db.Column(db.String(30),nullable=False)#Encriptar
    __password = db.Column(db.String(25),nullable=False)#Encriptar
    _create_date=db.Column(db.DateTime,default=datetime.datetime.now)#para guardar la fecha de creación
    __owners=relationship("Owner")
    def __init__(self, username,password,email):
        self.__username=username
        self.__password=password
        self.__email=email

    def checkPass(self,password):
        return self.__password==password
    def verify_sessionKey(self, sessionKey):
        self.getSession==sessionKey
        
    def setUsername(self,username):
        self.__username=username
    def setEmail(self,email):
        self.__email=email

    def newPassword(self,password,newPassword):
        if self.checkPass(password):
            self.__password=newPassword

    def getName(self):
        return self.__username
    def getEmail(self):
        return self.__email
    def getDate(self):
        return self._create_date

    def getSession(self,password):
        if self.__checkPass(password):
            return self.__gen_hash(str(self.__id)+self.__username+self.__usrKey)
    def getID(self,password):
        if self.__checkPass(password):
            return self.__id

    def delOwners(self,password):
        if self.checkPass(password):
            for owner in self.__owners:
                db.session.delete(owner)
                db.session.commit()

    def delPub(self):
        pass
    def delComent(self):
        pass
    def delLike(self):
        pass
    

#Tabla de Comentarios
class Comentario(db.Model):
    __tablename__ = "Comentario"
    __id=db.Column(db.Integer, primary_key=True)
    __pubID=db.Column(db.Integer,ForeignKey('Publicacion._Publicacion__id'))
    __ownID=db.Column(db.Integer,ForeignKey('Owner._Owner__id'),unique = True,nullable=False)
    __data= db.Column(db.String(125),nullable=False)    

    def __init__(self,key,pubID,ownID,data):
        if securityOwn.verify_own(key):
            self.__pubID=pubID
            self.__ownID=ownID
            self.__data=data

    def __repr__(self):
        return f'{self._data}'
#Tabla de Likes
class Like(db.Model):
    __tablename__ = "Like"
    __likeID=db.Column(db.Integer, primary_key=True)
    __pubID=db.Column(db.Integer,ForeignKey('Publicacion._Publicacion__id'))
    __ownID=db.Column(db.Integer,ForeignKey('Owner._Owner__id'),unique = True,nullable=False)
    
    def __init__(self,key,pubID,ownID,data):
        if securityOwn.verify_own(key):
            self.__pubID=pubID
            self.__ownID=ownID
            self.__data=data

#Tabla de publicacion    
class Publicacion(db.Model):
    __tablename__ = "Publicacion"
    __id=db.Column(db.Integer, primary_key=True)
    __ownID=db.Column(db.Integer,ForeignKey('Owner._Owner__id'),unique = True,nullable = False)
    __data= db.Column(db.String(250),nullable=False)
    __likes= relationship("Like")
    __comentarios= relationship("Comentario")

    def __init__(self,key,ownID,data):
        if securityOwn.verify_own(key):
            self.__ownID=ownID
            self.__data=data

    def getID(self):
        return self.__id

    def getData(self):
        return self.__data

    def getNumLikes(self):
        return len(self.__likes)

    def getComentarios(self):
        return self.__comentarios

    def __repr__(self):
        return f'{self.__data}'
        
class Owner(db.Model,securityOwn):
    __tablename__ = "Owner"
    __id=db.Column(db.Integer, primary_key=True)
    __usrID=db.Column(db.Integer,ForeignKey('User._User__id'))#Encriptar
    __autor = db.Column(db.String(50),default="Anónimo",nullable=False)#Encriptar
    _sessionKey=db.Column(db.String(66),nullable=False)#usrID+username+SecretKey Suma de datos "256"#Encriptar
    _create_date=db.Column(db.DateTime,default=datetime.datetime.now)#para guardar la fecha de creación
    __publicacion = relationship("Publicacion")
    __like = relationship("Like")
    __comentario = relationship("Comentario")
    #_propiedad_key = db.Column(db.String(66),nullable=True)#+SecretKey+tipo(Publicacion,Like,comentrio)+ID Suma de datos "256"
    
    def __init__(self,sessionKey,sessionID):
        user=User.query.filter_by(id=sessionID).first()
        if user is not None:
            self._sessionKey=sessionKey
            self.__usrID=sessionID

    def setAutor(self,autor):
        self.__autor=autor

    def getAutor(self):
        return self.__autor


    