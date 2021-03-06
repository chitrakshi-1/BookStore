# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
#import json
def index():
    demo= db(db.books).select(orderby=db.books.id)   #extraxt data from database and view to the user
    return locals()
# ---- API (example) -----
def cart():
    cartrows= db(db.cartitems.user_id==session.auth.user.id).select(orderby=db.cartitems.id)   #extraxt data from database and view to the user
    return locals()
def newaddress():
    form =SQLFORM(db.address).process()     # take the user entry and post on the form
    return locals()

def addtocart():
    myitems=db(db.books.id==request.args[0]).select(db.books.ALL).as_list()[0]
    #myitems=myitems[int(request.args[0])]
    #db.cartitems.insert(**db.cartitems._filter_fields(session.auth.user.id,myitems.get('book_id'),myitems.get('book_name'),                                                                                        myitems.get('book_genere'),myitems.get('book_author'),myitems.get('book_price'),myitems.get('book_image'),'4'))
    db.cartitems.insert(user_id=session.auth.user.id,book_id=myitems.get('book_id'),book_name=myitems.get('book_name'),book_genere=myitems.get('book_genere'),book_author=myitems.get('book_author'),book_price=myitems.get('book_price'),book_image=myitems.get('book_image'),book_qty='4')
    #return dict(mes=myitems.get('book_name'))
    #db.cartitems.insert(**myitems)
    #return myitems
    #rows= db(db.books).select(orderby=db.books.id)   #extraxt data from database and view to the user
    redirect(URL('view'))
def address():
    addr= db(db.address.user_id==session.auth.user.id).select(orderby=db.address.id)   #extraxt data from database and view to the user
    return locals()
def saveaddress():
    aname= request.post_vars.name
    ahouse=request.post_vars.house
    aarea=request.post_vars.area
    acity=request.post_vars.city
    astate=request.post_vars.state
    acountry=request.post_vars.country
    apin=request.post_vars.pin
    aphone=request.post_vars.phone
    aemail=request.post_vars.email
    adtype=request.post_vars.atype
    db.address.insert(user_id=session.auth.user.id,address_name=aname,address_house=ahouse,address_area=aarea,address_city=acity,address_state=astate,address_country=acountry,address_pin=apin,address_phone=aphone,address_email=aemail,address_type=adtype)
    redirect(URL('address'))
def deleteaddress():
    if db.address[request.args(0)].user_id == session.auth.user.id:
        db(db.address.id == request.args(0)).delete()
    redirect(URL('address'))
def deleteitem():
    if db.cartitems[request.args(0)].user_id == session.auth.user.id:
        db(db.cartitems.id == request.args(0)).delete()
    #myitems=db(db.books.id==request.args(0)).delete()
    redirect(URL('cart'))

@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()
def view():
    rows= db(db.books).select(orderby=db.books.id)   #extraxt data from database and view to the user
    return locals()
@request.restful()
def api():
    def GET(*args,**vars):
        rows= db(db.books).select(orderby=db.books.id).as_dict()
        return rows
    def POST(*args,**vars):
        return db.books.insert(**vars)
        #return(args,vars)
        
    def PUT(*args,**vars):
        record_id=vars['book_id']
        del vars['book_id']
        return db(db.books.book_id==record_id).update(**vars)
        #return record_id
    return dict(GET=GET,POST=POST,PUT=PUT)
# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
