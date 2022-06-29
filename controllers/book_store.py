# -*- coding: utf-8 -*-
# try something like
def index():
    demo= db(db.demo).select(orderby=db.demo.id)   #extraxt data from database and view to the user
    return locals()
@auth.requires_login()
def view():
    rows= db(db.books).select(orderby=db.books.id)   #extraxt data from database and view to the user
    return locals()
@auth.requires_membership('book_post')
def post():
    form =SQLFORM(db.books).process()     # take the user entry and post on the form
    return locals()
