# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

#########################################################################
##   add_routes() function allows Admin to add new routes
#########################################################################

import networkx as nx

def add_routes():
    form_add_route=SQLFORM.factory(Field('source_pt',requires=IS_NOT_EMPTY()),
                                   Field('destination_pt',requires=IS_NOT_EMPTY()),
                                   Field('distance_between','double',requires=IS_NOT_EMPTY()),
                                   Field('traffic','double',requires=IS_NOT_EMPTY()))
    if form_add_route.process().accepted:
        ip_source_pt=form_add_route.vars.source_pt
        ip_destination_pt=form_add_route.vars.destination_pt
        ip_dist_btw=form_add_route.vars.distance_between
        ip_traffic=form_add_route.vars.traffic
        id1=db.routes.insert(source_pt=ip_source_pt,
                             destination_pt=ip_destination_pt,
                             dist_btw=ip_dist_btw,
                             traffic=ip_traffic)
    return locals()

#####################################################################
## share_a_cab() function allows a user to post details of cab to be shared
#####################################################################
def share_a_cab():
    rows=db().select(db.routes.ALL)
    g=nx.Graph()
    for row in rows:
        a=str(row.source_pt)
        b=str(row.destination_pt)
        c=float(row.dist_btw)
        g.add_edge(a,b,weight=c)
        
    form_share_a_cab=SQLFORM.factory(Field('user_id',requires=IS_NOT_EMPTY()),
                                     Field('source_pt',requires=IS_NOT_EMPTY()),
                                     Field('destination_pt',requires=IS_NOT_EMPTY()),
                                     Field('date_of_travel','date',requires=IS_NOT_EMPTY()),
                                     Field('time_of_travel','time',requires=IS_NOT_EMPTY()),
                                     Field('type_of_car',requires=IS_NOT_EMPTY()),
                                     Field('seats_available','integer',requires=IS_NOT_EMPTY()),
                                     Field('preference',requires=IS_NOT_EMPTY()))
    
    if form_share_a_cab.process().accepted:
        ip_user_id=form_share_a_cab.vars.user_id
        ip_source_pt=form_share_a_cab.vars.source_pt
        ip_destination_pt=form_share_a_cab.vars.destination_pt
        ip_date_of_travel=form_share_a_cab.vars.date_of_travel
        ip_time_of_travel=form_share_a_cab.vars.time_of_travel
        ip_type_of_car=form_share_a_cab.vars.type_of_car
        ip_seats_available=form_share_a_cab.vars.seats_available
        ip_preference=form_share_a_cab.vars.preference
        ip_shortest_path_btw=nx.shortest_path(g,ip_source_pt,ip_destination_pt,weight='weight')
        id1=db.share_cab_details.insert(user_id=ip_user_id,
                                        source_pt=ip_source_pt,
                                        destination_pt=ip_destination_pt,
                                        date_of_travel=ip_date_of_travel,
                                        time_of_travel=ip_time_of_travel,
                                        path_btw=ip_shortest_path_btw,type_of_car=ip_type_of_car,
                                        seats_available=ip_seats_available,preference=ip_preference)
    return locals()
##############################################################################################################
## 
##############################################################################################################
def search_cab():
    form_search_cab=SQLFORM.factory( Field('source_pt',requires=IS_NOT_EMPTY()),
                                     Field('destination_pt',requires=IS_NOT_EMPTY()),
                                     Field('seats_required','integer',requires=IS_NOT_EMPTY()),
                                     Field('date_of_travel','date',requires=IS_NOT_EMPTY()),
                                     Field('time_of_travel','time',requires=IS_NOT_EMPTY()))
    if form_search_cab.process().accepted:
        redirect(URL('search_cab_details',vars={'source_pt':form_search_cab.vars.source_pt,
                                               'destination_pt':form_search_cab.vars.destination_pt,
                                               'seats_required':form_search_cab.vars.seats_required,
                                               'date_of_travel':form_search_cab.vars.date_of_travel,
                                               'time_of_travel':form_search_cab.vars.time_of_travel}))
        
    return locals()
def search_cab_details():
    source_pt=request.vars.source_pt
    destination_pt=request.vars.destination_pt
    seats_required=int(request.vars.seats_required)
    date_of_travel=request.vars.date_of_travel
    time_of_travel=request.vars.time_of_travel
    rows=db(db.share_cab_details).select()
    cab_list=[]
    for row in rows:
        c=list(row.path_btw)
        if date_of_travel==str(row.date_of_travel):
            if seats_required<=row.seats_available:
                if source_pt in c and destination_pt in c:
                    if c.index(source_pt) < c.index(destination_pt):
                        cab_list.append(row)
                    else:
                        print 'False'
    return locals()

def book_cab():
    travel_id=request.vars.travel_id
    source_pt=request.vars.source_pt
    destination_pt=request.vars.destination_pt
    seats_required=request.vars.seats_required
    date_of_travel=request.vars.date_of_travel
    time_of_travel=request.vars.time_of_travel
    id1=db.shared_cab_details.insert(user_id='abc',
                                        travel_id=travel_id,
                                        source_pt=source_pt,
                                        destination_pt=destination_pt,
                                        seats_booked=seats_required,
                                        date_of_travel=date_of_travel,
                                        time_of_travel=time_of_travel
                                        )
    seats_remaining=int(request.vars.seats_available) - int(seats_required)
    row = db(db.share_cab_details.id==int(travel_id)).select().first()
    row.update_record(seats_available=seats_remaining)
    
    return locals()



def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


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
    http://..../[app]/default/user/bulk_register
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
