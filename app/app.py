#Se importa de flask los objetos que ocuparemos 
from flask import Flask
from flask import render_template
from flask import request
from flask import g
from flask import url_for
from flask import redirect
from flask import make_response
from flask import session 

#Se importa configoraciones de desarrollo 
from config import DevConfig 

#Se importa configoraciones de la base de datos 
from models import db
from models import User
from models import Owner
from models import Publicacion
from models import Like
from models import Comentario
#Se importa seguridad CSRF
from flask_wtf.csrf import CSRFProtect

#se inicializa una aplicación
app=Flask(__name__) 
app.config.from_object(DevConfig)
csrf = CSRFProtect()

"""@app.before_request#código para antes de la petición
def Antes_peticion():
    print("Antes de la petición")

@app.after_request#código para Despues de la petición
def Despues_peticion(response):
    print("Despues de la petición")
    return response"""

#Programación la ruta raíz 
@app.route('/')#indicamos que es la ruta raíz 
def index():
    if 'id' in session:
        log="out"
    else:
        log="in"
    #nueva actividad
    owners=Owner.query.group_by(
        Owner._propiedad
        ).having(
            Owner._propiedad == 'publicación'
            ).order_by(
                Owner._create_date.desc()
                ).all()
    
    publicaciones={}
    for owner in owners:
        print(owner.getPropiedad())
        pub=owner.getPropiedad()
        if log == "out":
            Autor=owner.getAutor()
            
        else:
            Autor="Anónimo"
        publicaciones[pub.getID()]=[
            Autor,
            pub.getData(),
            pub.getNumLikes()
        ]
    data={
        'titulo':'Lobby',
        'bienvenida':'Bienbenido!! ',
        'url':url_for('publicacion'),
        "log":log,
        'sizePub':len(publicaciones)
    }
    respuesta=make_response(
        render_template(
            'index.html',
            data=data,
            publicaciones=publicaciones
        )
    )
    respuesta.set_cookie('location_cookie',url_for('index'))
    return respuesta
"""Funcion retorna un template cuando 
ingreasamos a la pagina"""
"""return "<h1>hola mundo</h1>"
Funcion retorna un texto cuando 
ingreasamos a la pagina""" 

#direcciones programación de la direcciones de perfil 
@app.route('/perfil/<nombre>')#direcciones dinamicas/<int:IDpub>
def perfil(nombre):
    if 'id' in session:
        #publicaciones del usuario 
        pub =['publicación 1','publicación 3','publicación 4']
        likes=[2,5,6]
        #publicaciones a las que dio like 
        likePub = ['publicación 2','publicación 4']
        #publicaciones en las que comento y sus comentarios
        pubComent=['publicación 2','publicación 1']
        userComent = [['Buena data crack',':)'],['valla valla ta qu valla']]
        data={
            'titulo':'User',
            'nombre':nombre,
            'userPub':pub,
            'pubLikes':likes,
            'userLikes':likePub,
            'pubComent':pubComent,
            'userComents':userComent,
            'sizeComent':len(pubComent),
            'sizelike':len(likePub),
            'sizePub':len(pub)
        }
        respuesta=make_response( render_template('perfil.html',data=data))
    else:
        respuesta=make_response(redirect(url_for('login')))
        respuesta.set_cookie('location_cookie',url_for('perfil',nombre=nombre))
    return respuesta
    

#Bajas y Edicion
@app.route('/myperfil/')
def myperfil():
    host="http://127.0.0.1:5000"
    #IDuser= request.cookies.get('custome_cookie','Undefined')
    if 'id' in session:
        #se odtiene usuario de BD
        user=User.query.filter_by(id=session['id']).first()
        #publicaciones del Usr_IDH256 
        pub =['publicación 1','publicación 3','publicación 4']
        likes=[2,5,6]
        #publicaciones a las que Usr_IDH256 dio like 
        likePub = ['publicación 2','publicación 4']
        likepublikes=[1,6]
        #publicaciones en las que Usr_IDH256 comento y sus comentarios
        pubComent=['publicación 2','publicación 1']
        #Comentarios del usurario 
        userComent = [['Buena data crack',':)'],['valla valla ta qu valla']]
        #Largo de cada lista 
        sizeComents=[2,1]
        buttons={
            "Cambiar Nombre":host+url_for('edit',element="nombre"),
            "Cambiar Correo":host+url_for('edit',element="email"),
            "Cambiar Contraseña":host+url_for('edit',element="pass"),
            "Eliminar Perfil":host+url_for('delUser')
        }
        data={
            'titulo':'Home',
            'nombre':user.getName(),
            'userPub':pub,
            'likepublikes':likepublikes,
            'pubLikes':likes,
            'userLikes':likePub,
            'pubComent':pubComent,
            'userComents':userComent,
            'sizeComents':sizeComents,
            'sizeComent':len(pubComent),
            'sizelike':len(likePub),
            'sizePub':len(pub),
        }
        respuesta=make_response(render_template('myperfil.html',data=data,buttons=buttons))
    else:
        respuesta=make_response(redirect(url_for('login')))
    respuesta.set_cookie('location_cookie',url_for('myperfil'))
    return respuesta

@app.route('/users/')
def users():
    if 'id' in session:
        #Usuarios registrados
        NamePerfil=[]
        for data in User.query.all():
            NamePerfil.append(data)
            #host para el enlace
            host='127.0.0.1:5000'
            data={
                'host':host,
                'titulo':'usuarios',
                'Users':NamePerfil,
                'sizeUsers':len(NamePerfil)
            }
        respuesta=make_response( render_template('users.html',data=data))
    else:
        respuesta=make_response(redirect(url_for('login')))
    respuesta.set_cookie('location_cookie',url_for('users'))
    return respuesta
    

@app.route('/logout/')
def logout():
    if 'id' in session:
        session.pop('username')
        session.pop('key')
    
    return redirect(url_for('index'))

@app.route('/login/',methods=['GET','POST'])
def login():
    host='127.0.0.1:5000'
    location=request.cookies.get('location_cookie','index')
    data={
        'host':host,
        'titulo':'login'
    }
    if request.method=='GET':
        return render_template('login.html',data=data)
    if request.method=='POST':
        username=request.form['name']
        password=request.form['pass']
        user= User.query.filter_by(_User__username=username).first()
        #se realiza una pequeña autenticasion 
        if user is not None :
            #obtener ID de BD y guardarlo en sesion 
            session['id']=user.getID(password)
            session['key']=user.getSession(password)
            return redirect(location)
        else:
            return redirect(url_for("index"))
        
#               ====================Usuarios====================            

@app.route('/NewUser/', methods = ['GET','POST'])#            Alta
def NewUser():
    
    if request.method == 'GET':
        data={
        'titulo':'Registrarse'
        }
        respuesta=make_response(render_template('registro.html',data=data))

    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        user=User.query.filter_by(_User__username=name).first()

        if user is None:  
            respuesta=make_response( redirect(url_for('myperfil')))
            user = User(
                name,
                password,
                request.form['gmail']
                )
            db.session.add(user)
            db.session.commit()

            print('datos de session Debug')
            print('username:'+user.__username)
            print('id:'+str(user.__id))
            
            session['id']=user.__id
            session['key']=user.getSession(password)

            
        else:
           respuesta=make_response( redirect(url_for('logout'))) 

    return respuesta

@app.route('/edit/user/<element>',methods = ['GET','POST'])#     Actualizacon  
def edit(element):

    if 'id' in session:

        user=User.query.filter_by(_User__id=session['id']).first()
        if user is None and user.verify_sessionKey(session['key']):
            print("Sesion no Valida")
            return redirect(url_for('logout'))

        if request.method == 'GET':
            data={
            'titulo':'Editando',
            'msn':user.getName()+", quieres cambiar tu "+element+"?",
            'element':element
            }
            respuesta=make_response(render_template('actualizar.html',data=data))

        if request.method == 'POST': 
 
            respuesta=make_response( redirect(url_for('myperfil'))) 
            
            #selección de elemento a modificar
            if element=="nombre":
                newName=request.form['nuevo_Elemento']
                usrInUse=User.query.filter_by(_User__username=newName).first()
                if usrInUse is None:
                    user.setUsername(newName)
                    db.session.commit()
                    print("nombre actualizado")
                else:
                    print("nombre esta en uso por"+"ID sin acceso")#str(usrInUse.__id)

            elif element=="email":
                user.setEmail(request.form['nuevo_Elemento'])
                db.session.commit()
                print("correo actualizado")

            elif element=="pass":
                user.setPassword(
                    request.form['pass'],
                    request.form['nuevo_Elemento']
                )
                db.session.commit()
                print("contraseña actualizada")
            else:
                print("Algo Salio mal")   

    else:
        respuesta=make_response(redirect(url_for('login')))
    respuesta.set_cookie('location_cookie',url_for('edit',element=element))
    return respuesta

@app.route('/del/user',methods = ['GET','POST'])#            baja
def delUser():
    
    if 'id' in session:

        user=User.query.filter_by(_User__id=session['id']).first()
        if user is None and user.verify_sessionKey(session['key']):
            print("Sesion no Valida")
            return redirect(url_for('logout'))

        if request.method == 'GET':
            data={
                'host':"http://127.0.0.1:5000",
                'titulo':'Eliminar',
                'msn':user.getName()+", quieres eliminar tu cuenta?"
            }
            respuesta=make_response(render_template('eliminar.html',data=data))
        
        if request.method == 'POST':

            respuesta=make_response( redirect(url_for('myperfil')))

            if user.checkPass(request.form['pass']):
                respuesta=make_response(redirect(url_for('logout')))
                db.session.delete(user)
                db.session.commit()
                print("Datos eliminados")
            else:
                print("Contraseña no valida")

    else:
        respuesta=make_response(redirect(url_for('login')))
    respuesta.set_cookie('location_cookie',url_for('delUser'))
    return respuesta

#               ====================Publicación====================  
@app.route('/NewPub/',methods = ['GET','POST'])#            Alta
def NewPub():
    
    if 'id' in session:

        user=User.query.filter_by(_User__id=session['id']).first()
        if user is None and user.verify_sessionKey(session['key']):
            print("Sesion no Valida")
            return redirect(url_for('logout'))

        if request.method == 'GET':
            data={
            'titulo':'nueva publicación',
            'autor':user.getName()
            }
            respuesta=make_response( render_template('publicar.html',data=data))

        if request.method == 'POST':

            respuesta=make_response(redirect(url_for('index')))

            #Registro en tabla autores
            owner=Owner(
                session['key'],
                session['id'],
                "publicación"
            )
            db.session.add(owner)
            db.session.commit()
            print("Autor Registrado")

            #Registro en tabla Publicaciones
            pub=Publicacion(
                owner.getKey(),
                owner.__id,
                request.form['contenido']
            )
            db.session.add(pub)
            db.session.commit()
            print("publicación Registrada")  
    else:
        respuesta=make_response(redirect(url_for('login')))
    respuesta.set_cookie('location_cookie',url_for('NewPub'))
    return respuesta

@app.route('/delPub/<pos>',methods = ['GET','POST'])#            Baja
def delPub(pos):
    if 'id' in session:
        
        user=User.query.filter_by(_User__id=session['id']).first()
        if user is None and user.verify_sessionKey(session['key']):
            print("Sesion no Valida")
            return redirect(url_for('logout'))
        
        if request.method == 'GET':
            msn= session['username']+", quieres eliminar tu publicación?"
            data={
            'titulo':'Eliminar',
            'msn':msn
            }
            respuesta=make_response(render_template('eliminar.html',data=data))
        
        if request.method == 'POST':
            respuesta=make_response( redirect(url_for('myperfil')))
            if owner is not None:
                """#Eliminar permanente mente las publicaciones 
                pub=Publicacion.query.filter_by(id=owner.pub_ID).first()
                if pub is not None:
                    db.session.delete(pub)
                    db.session.commit()
                    print("publicación eliminada")
                else:
                    print("publicación no encontrada")"""
                db.session.delete(owner)
                db.session.commit()
            
            
            print("Datos eliminados")
            
    else:
        respuesta=make_response(redirect(url_for('login')))
    respuesta.set_cookie('location_cookie',url_for('dele',type=type))
    return respuesta
#               ====================comentario==================== 
@app.route('/pub/<ID>',methods = ['GET','POST'])#        alta
def Pub(ID):
    if 'id' in session:
        owner=OwnerPublicacion.query.having(OwnerPublicacion.verify_PubID(ID)).first()

        #owner='J0se'
        ownerComents=['Pamela Azul','Pamela Azul','Pamela Azul']
        coments= ['Buena data crack',':)','valla valla ta qu valla']
        contenido='publicacion x'
        likesTotal=3
        #host para el enlace
        host='127.0.0.1:5000'
        if request.method == 'GET':
            data={
                'titulo':'Post',
                'host':host,
                'pubID':ID,
                'userlog':'id' in session and 'username' in session,
                'Owner':owner.username,
                'Owners':ownerComents,
                'contenido':contenido,
                'comentarios':coments,
                'sizeComents':len(coments),
                'likes':likesTotal
            }
            respuesta=make_response(render_template('publicacion.html',data=data))

        if request.method == 'POST':
            user=User.query.filter_by(id=session['id']).first()
            if user is not None and user.verify_username(session['username']):
                coment=Comentario(
                    ID,
                    request.form['Comentario']
                )
                db.session.add(coment)
                db.session.commit()
                print("Comentario Registrado")
                owner=OwnerComentario(
                    user.getUsr_IDH256(),
                    coment.id,
                    session['username']
                )
                print("Autor Registrado")
            respuesta=make_response(redirect('http://'+host+'/pub?'+'ID='+ID))
    else:
        respuesta=make_response(redirect(url_for('login')))
    respuesta.set_cookie('location_cookie',url_for('Pub',ID=ID))
    return respuesta

def dele_coment():#             Baja
    pass

#               ====================Likes====================
def like(ID):#                  Alta y Baja
    user=User.query.filter_by(id=session['id']).first()
    if user is not None and user.verify_username(session['username']):
        gavelike=OwnerLike.query.filter_by(usr_IDH256=user.getUsr_IDH256()).first()
        if gavelike is None:
            like=Like(ID)
            db.session.add(like)
            db.session.commit()
            
            owner=OwnerLike(
                user.getUsr_IDH256(),
                like.id,
                session['username']
            )
            db.session.add(owner)
        else:
            likeRegister=Like.query.filter_by(id=gavelike.like_ID).first()
            db.session.dele(likeRegister)

            db.session.commit()
            db.session.dele(gavelike)
        db.session.commit()
    else:
        print("Sesion no valida")

def publicacion():
    location=request.cookies.get('location_cookie','/')
    respuesta=make_response(redirect(location))
    userlog='id' in session and 'username' in session#segun login
    operacion=request.args.get('OP')
    pub=Publicacion.query.filter_by(id=request.args.get('ID')).first()
    print(request)#control de petición
    print(request.args)#control parametros de petición 
    
    if pub is not None:
        if userlog:
            if operacion is None:
                respuesta=make_response(redirect(url_for('Pub',ID=pub.id)))   
            elif operacion=='like':
                like(pub)
            elif operacion=='coment':
                dele_coment(pub)
            else:
                print("operacion desconocida")
        else:
            coments= ['Buena data crack',':)','valla valla ta qu valla']
            contenido='publicacion x'
            likesTotal=3
            data={
            'titulo':'Post',
            'userlog':userlog,
            'contenido':contenido,
            'comentarios':coments,
            'sizeComents':len(coments),
            'likes':likesTotal
            }
            respuesta=make_response(render_template('publicacion.html',data=data))
    else:
        print("La publicacion no existe")
    return respuesta
"""
def query_string():#parametros variables
    print(request)#control de petición
    print(request.args)#control parametros de petición 
    print(request.args.get('P1'))#control parametro1 de petición 
    
    return "okey :)"""

if __name__=='__main__': 
    csrf.init_app(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    #app.add_url_rule('/Data',view_func=query_string)#enlace de ruta con la funcion query_string
    app.add_url_rule('/pub',view_func=publicacion)
    app.run(port=5000)#app.run(debug=True,port=puerto)#Depuración
""" si estamos desde el archivo 
inicial ejecutamos la aplicación """
