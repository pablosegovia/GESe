def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Bienvenido al Sistema")
    return dict(message=T('Esto es GESe'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def alta_alumno():

    form = SQLFORM.factory(
        Field('tipo_doc',default='DNI',label=T('Tipo de Documento'),
              requires=IS_IN_SET(('DNI','CI','LC','LD'))),
        Field('nro_doc',label=T('Numero de Documento'),
             requires=IS_INT_IN_RANGE(10000000, 100000001, error_message=('Falta ingresar el Numero de Documento o lo ingreso mal'))),
        Field('estado_doc',default='Bueno',label=T('Estado del Documento'),
             requires=IS_IN_SET(('Bueno','Malo','En trámite','No posee'))),
#        Field('cuil',label=T('CUIL')),
        Field('apellido',length=15,default='',label=T('Apellido')),
        Field('apellido_materno',label=T('Apellido Materno')),
        Field('nombre',length=15,default='', label=T('Nombre')),
        Field('segundo_nombre',length=30,default='',label=T('Segundo Nombre')),
        Field('sexo',label=T('Sexo'),
              requires=IS_IN_SET(('Masculino','Femenino'))),
        submit_button='Registrar alumno')

    if form.accepts(request.vars, session):
        session.flash = 'Alumno registrado con exito!'
        db.alumno.insert(
        tipo_doc=form.vars.tipo_doc,
        nro_doc=form.vars.nro_doc,
        estado_doc=form.vars.estado_doc,
        apellido=form.vars.apellido,
        apellido_materno=form.vars.apellido_materno,
        nombre=form.vars.nombre,
        segundo_nombre=form.vars.segundo_nombre,
        sexo=form.vars.sexo,
        )
        #Busca el usuario registrado para obtener su ID
        lista_doc= db((db.alumno.id>0)&(db.alumno.nro_doc==form.vars.nro_doc)).select()
        for nro_doc in lista_doc:
            id_alumno=nro_doc.id
        redirect(URL("index"))

    elif form.errors:
        response.flash = 'Hay errores, por favor corrijalos.'
    return dict(form=form)

def alumnos():
    lista_alumnos = db(db.alumno.id>0).select(
        db.alumno.id,
        db.alumno.tipo_doc,
        db.umno.nro_doc,
        db.alumno.apellido,
        db.alumno.apellido_materno,
        db.alumno.nombre,
        db.alumno.segundo_nombre,al
        orderby=db.alumno.nro_doc,)
    
    return {'lista_alumnos' : lista_alumnos}

def modificar_alumno():
    if not request.args:
        session.flash="No informo alumno a editar"
        redirect(URL("alumnos"))

    alu = db(db.alumno.id==request.args[0]).select()
    if not alu:
        session.flash="El alumno no existe"
        redirect(URL("alumnos"))
        
    alumno = alu[0]
    
    db.alumno.id.readable = False
    db.alumno.id.writable = False
    
    form = SQLFORM(db.alumno, alumno,
                    deletable=True,
                    fields=[
                    'id',
                    'tipo_doc',
                    'nro_doc',
                    'estado_doc',
                    'apellido',
                    'apellido_materno',
                    'nombre',
                    'segundo_nombre',
                    'sexo',
                    ],
                    labels={
                    'id': 'ID',
                    'tipo_doc': 'Tipo de Doc.',
                    'nro_doc': 'Nro de Doc.',
                    'estado_doc': 'Estado del Doc.',
                    'apellido': 'Apellido',
                    'apellido_materno': 'Apellido Materno',
                    'nombre': 'Nombre',
                    'segundo_nombre': 'Segundo Nombre',
                    'sexo': 'Sexo',
                    },
                    submit_button='Modificar')

    if form.accepts(request.vars, session):
            session.flash = "Alumno modificado"
            redirect(URL('alumnos'))
    elif form.errors:
            response.flash = "Hubo errores"
    else:
            response.flash = "Modifique el alumno"
            
    return {'form': form,'Alumnos': alumnos}
	
################################################################################################################### ADULTOS #########################	
def alta_adulto():

    form = SQLFORM.factory(
        Field('tipo_doc',default='DNI',label=T('Tipo de Documento'),
              requires=IS_IN_SET(('DNI','CI','LC','LD'))),
        Field('nro_doc',label=T('Numero de Documento'),
             requires=IS_INT_IN_RANGE(10000000, 100000001, error_message=('Falta ingresar el Numero de Documento o lo ingreso mal'))),
        Field('estado_doc',default='Bueno',label=T('Estado del Documento'),
             requires=IS_IN_SET(('Bueno','Malo','En trámite','No posee'))),
#        Field('cuil',label=T('CUIL')),
        Field('apellido',length=15,default='',label=T('Apellido')),
        Field('nombre',length=15,default='', label=T('Nombre')),
		Field('nacionalidad',label=T('Nacionalidad')),
		Field('profesion',label=T('Profesion')), 
        Field('cond_act',label=T('Condicion de Actividad')), 
        Field('nivel_inst',label=T('Nivel de instruccion')), 
        Field('completo'), 
        Field('grado'), 
        Field('vive'),
        Field('calle'), 
        Field('nro_calle'), 
        Field('piso'), 
        Field('torre'), 
        Field('dpto'), 
        Field('localidad'), 
        Field('codigo_postal'),
        submit_button='Registrar adulto')

    if form.accepts(request.vars, session):
        session.flash = 'adulto registrado con exito!'
        db.adulto.insert(
        tipo_doc=form.vars.tipo_doc,
        nro_doc=form.vars.nro_doc,
        estado_doc=form.vars.estado_doc,
        apellido=form.vars.apellido,
        nombre=form.vars.nombre,
		nacionalidad=form.vars.nacionalidad,
		profesion=form.vars.profesion,
		cond_act=form.vars.cond_act,
		nivel_inst=form.vars.nivel_inst,
		completo=form.vars.completo,
		grado=form.vars.grado,
		vive=form.vars.vive,
		calle=form.vars.calle,
		nro_calle=form.vars.nro_calle,
		piso=form.vars.piso,
		torre=form.vars.torre,
		dpto=form.vars.dpto,
		localidad=form.vars.localidad,
		codigo_postal=form.vars.codigo_postal,
		)
        #Busca el usuario registrado para obtener su ID
        lista_doc= db((db.adulto.id>0)&(db.adulto.nro_doc==form.vars.nro_doc)).select()
        for nro_doc in lista_doc:
            id_adulto=nro_doc.id
        redirect(URL("index"))

    elif form.errors:
        response.flash = 'Hay errores, por favor corrijalos.'
    return dict(form=form)

def adultos():
    lista_adultos = db(db.adulto.id>0).select(
    db.adulto.id,
    db.adulto.tipo_doc,
    db.adulto.nro_doc,
    db.adulto.apellido,
    db.adulto.nombre,
    orderby=db.adulto.nro_doc,)
        
    return {'lista_adultos' : lista_adultos}

def modificar_adulto():
    if not request.args:
        session.flash="No informo adulto a editar"
        redirect(URL("adultos"))

    adu = db(db.adulto.id==request.args[0]).select()
    if not adu:
        session.flash="El adulto no existe"
        redirect(URL("adultos"))
        
    adulto = adu[0]
    
    db.adulto.id.readable = False
    db.adulto.id.writable = False
    
    form = SQLFORM(db.adulto, adulto,
                    deletable=True,
                    fields=[
                    'id',
                    'tipo_doc',
                    'nro_doc',
                    'estado_doc',
                    'apellido',
                    'nombre',
					'nacionalidad',
					'profesion',
					'cond_act',
					'nivel_inst',
					'completo',
					'grado',
					'vive',
					'tipo_doc',
					'nro_doc',
					'estado_doc',
					'calle',
					'nro_calle',
					'piso',
					'torre',
					'dpto',
					'localidad',
					'codigo_postal',
                    ],
                    labels={
                    'id': 'ID',
                    'tipo_doc': 'Tipo de Doc.',
                    'nro_doc': 'Nro de Doc.',
                    'estado_doc': 'Estado del Doc.',
                    'apellido': 'Apellido.',                
                    'nombre': 'Nombre.',
                    'nacionalidad': 'Nacionalidad.',
					'profesion': 'Profesion.',
					'cond_act': 'Condicion de actividad.',
					'nivel_inst':'Nivel de instruccion.',
					'completo': 'Completo', 
					'grado': 'Grado',
					'vive': 'Vive',
					'tipo_doc': 'Tipo de Documento',
					'nro_doc': 'Numero de Documento ' ,
					'estado_doc': 'Estado de Documento',
					'calle': 'Calle', 
					'nro_calle': 'Numero de Calle',
					'piso': 'Piso',
					'torre': 'Torre',
					'dpto': 'Departamento',
					'localidad': 'Localidad',
					'codigo_postal': 'Codigo Postal',
                    },
                    submit_button='Modificar')

    if form.accepts(request.vars, session):
            session.flash = "adulto modificado"
            redirect(URL('adultos'))
    elif form.errors:
            response.flash = "Hubo errores"
    else:
            response.flash = "Modifique el adulto"
            
    return {'form': form,'Adultos': adultos}
