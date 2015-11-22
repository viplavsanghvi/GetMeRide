# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import networkx as nx
import datetime
from gluon.tools import Mail
mail = Mail()
locations={}
points=[]
unweighted_g=nx.Graph()
weighted_g=nx.Graph()
rows=db().select(db.routes.ALL)
for row in rows:
    a=str(row.source_pt)
    b=str(row.destination_pt)
    c=float(row.dist_btw)
    d=float(row.traffic)
    e=c*d
    unweighted_g.add_edge(a,b,weight=c)
    weighted_g.add_edge(a,b,weight=e)
    if locations.has_key(a)==False:
            locations[a]=a
            points.append(a)
    if locations.has_key(b)==False:
            locations[b]=b
            points.append(b)



mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
        # mail.settings.server = 'logging'
        # mail.settings.login = None
mail.settings.sender = 'you@example.com'
mail.settings.login = 'care.getmeride@gmail.com:reglodnsrjjtvnbo'


#########################################################################
##   add_routes() function allows Admin to add new routes
#########################################################################


@auth.requires_login()
def add_routes():
    if not auth.user.is_admin:
          redirect(URL('index'))
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
@auth.requires_login()
def share_a_cab():
    from datetime import datetime
    g=nx.Graph()
    g=unweighted_g
#     rows=db().select(db.routes.ALL)
#     g=nx.Graph()
#     for row in rows:
#         a=str(row.source_pt)
#         b=str(row.destination_pt)
#         c=float(row.dist_btw)
#         g.add_edge(a,b,weight=c)
#         if locations.has_key(a)==False:
#             locations[a]=a
#             points.append(a)
#         if locations.has_key(b)==False:
#             locations[b]=b
#             points.append(b)
    form_share_a_cab=SQLFORM.factory(Field('source_pt',requires=IS_IN_SET(points)),
                                     Field('destination_pt',requires=IS_IN_SET(points)),
                                     Field('date_of_travel','date',requires=IS_NOT_EMPTY()),
                                     Field('time_of_travel','time',requires=IS_NOT_EMPTY()),
                                     Field('vehicle_no','string',requires=IS_NOT_EMPTY()),
                                     Field('type_of_car',requires=IS_IN_SET(['Sedan', 'Hatchback','SUV'])),
                                     Field('seats_available','integer',
                                           requires=IS_IN_SET([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])),
                                     Field('preference',requires=IS_IN_SET(['Male', 'Female','Any']))).process(onvalidation=form_processing)
#     print locations
#     print points
    if form_share_a_cab.accepted:
        ip_user_id=auth.user.email
        ip_source_pt=form_share_a_cab.vars.source_pt
        ip_destination_pt=form_share_a_cab.vars.destination_pt
        ip_date_of_travel=form_share_a_cab.vars.date_of_travel
        ip_time_of_travel=form_share_a_cab.vars.time_of_travel
        ip_vehicle_no=form_share_a_cab.vars.vehicle_no
        ip_type_of_car=form_share_a_cab.vars.type_of_car
        ip_seats_available=form_share_a_cab.vars.seats_available
        ip_preference=form_share_a_cab.vars.preference
#         user_id=
        traffic_wt='NO'
        rows=db(db.peak_time).select()
        for row in rows:
            if datetime.strptime(str(row.from_time), "%H:%M:%S") <= datetime.strptime(str(ip_time_of_travel), "%H:%M:%S") and datetime.strptime(str(ip_time_of_travel), "%H:%M:%S") < datetime.strptime(str(row.to_time), "%H:%M:%S"):
                traffic_wt='YES'
#         if datetime.strptime(str(row.time_of_travel)[:5], "%H:%M")<datetime.strptime(str(ip_time_of_travel), "%H:%M:%S"):
#         if traffic_wt == 'YES':
#             g=weighted_g
#         else:
#             g=unweighted_g
        ip_shortest_path_btw=nx.shortest_path(g,ip_source_pt,ip_destination_pt,weight='weight')
        id1=db.share_cab_details.insert(user_id=ip_user_id,
                                        source_pt=ip_source_pt,
                                        destination_pt=ip_destination_pt,
                                        date_of_travel=ip_date_of_travel,
                                        time_of_travel=ip_time_of_travel,
                                        path_btw=ip_shortest_path_btw,
                                        vehicle_no=ip_vehicle_no,
                                        type_of_car=ip_type_of_car,
                                        seats_available=ip_seats_available,
                                        preference=ip_preference,
                                        traffic_wt=traffic_wt)
        redirect(URL('default','index'))
    return locals()
##############################################################################################################
## 
##############################################################################################################
@auth.requires_login()
def search_cab():
    
    form_search_cab=SQLFORM.factory( Field('source_pt',requires=IS_IN_SET(points)),
                                     Field('destination_pt',requires=IS_IN_SET(points)),
                                     Field('seats_required','integer',
                                           requires=IS_IN_SET([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])),
                                     Field('date_of_travel','date',requires=IS_NOT_EMPTY()),
                                     Field('time_of_travel','time',requires=IS_NOT_EMPTY())).process(onvalidation=form_processing)
    if form_search_cab.accepted:
        redirect(URL('search_cab_details',vars={'source_pt':form_search_cab.vars.source_pt,
                                               'destination_pt':form_search_cab.vars.destination_pt,
                                               'seats_required':form_search_cab.vars.seats_required,
                                               'date_of_travel':form_search_cab.vars.date_of_travel,
                                               'time_of_travel':form_search_cab.vars.time_of_travel}))
        
    return locals()

def form_processing(form):
    from datetime import datetime
    if form.vars.source_pt == form.vars.destination_pt:
        form.errors.destination_pt='Source and Destination can not be same'
    date_of_travel=form.vars.date_of_travel
    todays_date=str(request.now)
    todays_date=todays_date[:10]
    if datetime.strptime(todays_date, "%Y-%m-%d") > datetime.strptime(date_of_travel, "%Y-%m-%d"):
        form.errors.date_of_travel='Date of travel can not be less then todays date'

@auth.requires_login()
def search_cab_details():
    from datetime import datetime
    g=nx.Graph()
    g=unweighted_g
    source_pt=request.vars.source_pt
    destination_pt=request.vars.destination_pt
    seats_required=int(request.vars.seats_required)
    date_of_travel=request.vars.date_of_travel
    time_of_travel=request.vars.time_of_travel
    distance_btw=nx.shortest_path_length(g,source_pt,destination_pt,weight='weight')
    fare=distance_btw*14*seats_required
    rows=db(db.share_cab_details).select()
    cab_list=[]
    
#     print todays_date
    for row in rows:
        c=list(row.path_btw)
        
        if date_of_travel==str(row.date_of_travel):
            if seats_required<=row.seats_available:
                if source_pt in c and destination_pt in c:
                    if c.index(source_pt) < c.index(destination_pt):
                        cab_list.append(row)
    if not cab_list:
        redirect(URL('cabs_not_found'))
    return locals()


@auth.requires_login()
def book_cab():
    travel_id=request.vars.travel_id
    ip_fare=request.vars.fare
    source_pt=request.vars.source_pt
    destination_pt=request.vars.destination_pt
    seats_required=request.vars.seats_required
    date_of_travel=request.vars.date_of_travel
    time_of_travel=request.vars.time_of_travel
    user_id=auth.user.email
    row1 = db(db.auth_user.id==int(auth.user.id)).select().first()
    wallet_amount=row1.wallet_amount
    row2 = db(db.share_cab_details.id==travel_id).select().first()
    vehicle_no=row2.vehicle_no
#     print vehicle_no
    if float(ip_fare) > float(wallet_amount):
        session.flash='Insufficient balance, redirected to a page where you can add money into your wallet'
        redirect(URL('insufficient_wallet_money'))
    form_book_cab=SQLFORM.factory( Field('confirm_booking','boolean'),
                                  hidden={'ip_wallet_amount':wallet_amount,'form_fare':ip_fare}).process(onvalidation=my_form_processing)
    if form_book_cab.accepted:
        id1=db.shared_cab_details.insert(   user_id=user_id,
                                        travel_id=travel_id,
                                        source_pt=source_pt,
                                        destination_pt=destination_pt,
                                        seats_booked=seats_required,
                                        date_of_travel=date_of_travel,
                                        time_of_travel=time_of_travel,
                                        fare=float(ip_fare))
        seats_remaining=int(request.vars.seats_available) - int(seats_required)
        row = db(db.share_cab_details.id==int(travel_id)).select().first()
        row.update_record(seats_available=seats_remaining)
        row1 = db(db.auth_user.id==int(auth.user.id)).select().first()
        wallet_amount=float(row1.wallet_amount)-float(ip_fare)
        row1.update_record(wallet_amount=wallet_amount)
        row2=db(db.share_cab_details.id==int(travel_id)).select().first()
        owner_email_id=row2.user_id
        row3=db(db.auth_user.email==owner_email_id).select().first()
        new_wallet_amount=float(row3.wallet_amount)+float(ip_fare)
        row3.update_record(wallet_amount=new_wallet_amount)
#         mail.send(auth.user.email,'Booking confirmation','Your booking has been successfully approved! Thanks for joining Get Me Ride. Happy Sharing smile emoticon')
        redirect(URL('booking_successful',vars={'user_email':owner_email_id,
                                                'source_pt':source_pt,
                                                'destination_pt':destination_pt,
                                                'seats_booked':seats_required,
                                                'date_of_travel':date_of_travel,
                                                'time_of_travel':time_of_travel,
                                                'fare':ip_fare,
                                                'vehicle_no':vehicle_no}))
#     elif form.errors:
        
        
    return locals()
def cancel_cab():
    id=request.vars.id
    fare=request.vars.fare
    source_pt=request.vars.source_pt
    destination_pt=request.vars.destination_pt
    seats_booked=request.vars.seats_booked
    date_of_travel=request.vars.date_of_travel
    time_of_travel=request.vars.time_of_travel
    user_id=auth.user.email
    form_cancel_cab=SQLFORM.factory( Field('confirm_cancellation','boolean')).process(onvalidation=my_form_processing1)
    if form_cancel_cab.accepted:
        row1 = db(db.shared_cab_details.id==int(id)).select().first()
        row1.update_record(status='Cancelled')
        shared_cab_id=row1.travel_id
        ip_fare=float(fare)/2
        row2=db(db.auth_user.email==user_id).select().first()
        new_wallet_amount=float(row2.wallet_amount)+ip_fare
        row2.update_record(wallet_amount=new_wallet_amount)
        row3 = db(db.share_cab_details.id==shared_cab_id).select().first()
        new_seats=int(row3.seats_available)+int(seats_booked)
        row3.update_record(seats_available=new_seats)
        owner_id=row3.user_id
        row4=db(db.auth_user.email==owner_id).select().first()
        owner_wallet_amount=float(row4.wallet_amount)-ip_fare
        row4.update_record(wallet_amount=owner_wallet_amount)
        redirect(URL('cancel_cab_success',vars={'refund':ip_fare,'wallet_amt':new_wallet_amount}))
#     print owner_id
    
#     id
# travel_id
# user_id
# source_pt
# destination_pt
# seats_booked
# date_of_travel
# time_of_travel
# fare
# status
    
    return locals()

def cancel_cab_success():
    refund=request.vars.refund
    wallet_amt=request.vars.wallet_amt
    return locals()

def my_form_processing1(form):
    c =bool(form.vars.confirm_cancellation)
    if c==False:
        form.errors.confirm_cancellation='Please check the checkbox if you want to cancel the booking'
    return locals()        



def my_form_processing(form):
    c =bool(form.vars.confirm_booking)
    if c==False:
        form.errors.confirm_booking='Please check the checkbox if you satisfy the Gender preference else search a new cab'
    return locals()        

@auth.requires_login()
def add_money():
#     session.flash
    form_add_money=SQLFORM.factory( Field('amount_to_be_added','integer',requires=IS_NOT_EMPTY())).process(onvalidation=add_money_process)
    if form_add_money.accepted:
        row = db(db.auth_user.id==int(auth.user.id)).select().first()
        new_amount=int(row.wallet_amount)+int(form_add_money.vars.amount_to_be_added)
        row.update_record(wallet_amount=new_amount)
        response.flash='Amount added successfully'
    return locals()

@auth.requires_login()
def add_money_process(form_add_money):
    if float(form_add_money.vars.amount_to_be_added) <=0:
        form_add_money.errors.amount_to_be_added='Amount entered should be greater than 0'
        redirect(URL('index'))
    return locals()

@auth.requires_login()
def insufficient_wallet_money():
#     session.flash
    form_add_money=SQLFORM.factory( Field('amount_to_be_added','float',requires=IS_NOT_EMPTY())).process(onvalidation=add_money_process)
    if form_add_money.accepted:
        row = db(db.auth_user.id==int(auth.user.id)).select().first()
        new_amount=float(row.wallet_amount)+float(form_add_money.vars.amount_to_be_added)
        row.update_record(wallet_amount=new_amount)
        session.flash='Amount added successfully'
        redirect(URL('search_cab'))
    return locals()

@auth.requires_login()
def booking_successful():
    user_email=request.vars.user_email
    source_pt=request.vars.source_pt
    destination_pt=request.vars.destination_pt
    seats_booked=request.vars.seats_booked
    date_of_travel=request.vars.date_of_travel
    time_of_travel=request.vars.time_of_travel
    fare=request.vars.fare
    vehicle_no=request.vars.vehicle_no
    row3=db(db.auth_user.email==user_email).select().first()
    contact_no=row3.contact_no
    msg= 'Your booking has been successfull !\n'
    msg= msg + 'Source point :' + source_pt +'\n'
    msg= msg + 'Destination point :' + destination_pt +'\n'
    msg= msg + 'Vehicle Number :'+ vehicle_no +'\n'
    msg= msg + 'Owners Contact Number :'+ contact_no + '\n'
    msg= msg + 'Owners mail-id :' + user_email +'\n'
    msg= msg + 'Seats Booked :' + seats_booked + '\n'
    msg= msg + 'Date of travel :'+ date_of_travel +'\n'
    msg= msg + 'Time of travel :'+ time_of_travel +'\n'
    msg= msg + 'Fare :'+ fare + ' INR \n'
    msg= msg + 'Happy Sharing smile emoticon'
#      +'\n'+  +  ++ 
    mail.send(auth.user.email,'Booking confirmation',msg)
    
    msg2='Your vehicle has been booked \n'
    msg2= msg2 + 'Source point :' + source_pt +'\n'
    msg2= msg2 + 'Destination point :' + destination_pt +'\n'
#     msg2= msg2 + 'Vehicle Number :'+ vehicle_no +'\n'
    msg2= msg2 + 'Sharers Contact Number :'+ auth.user.contact_no + '\n'
    msg2= msg2 + 'Sharers mail-id :' + auth.user.email +'\n'
    msg2= msg2 + 'Seats Booked :' + seats_booked + '\n'
    msg2= msg2 + 'Date of travel :'+ date_of_travel +'\n'
    msg2= msg2 + 'Time of travel :'+ time_of_travel +'\n'
    msg2= msg2 + 'Fare :'+ fare + ' INR \n'
    msg2= msg2 + 'Happy Sharing smile emoticon'
    return locals()

@auth.requires_login()
def cabs_not_found():
    cab_status='No Cabs found'
    return locals()

@auth.requires_login()
def previous_bookings():
    from datetime import datetime
    todays_date=str(request.now)
    current_time=todays_date[11:16]
    todays_date=todays_date[:10]
    todays_date=datetime.strptime(todays_date, "%Y-%m-%d")
    cabs_list=[]
    print current_time
    rows=db(db.shared_cab_details.user_id==auth.user.email).select()
    for row in rows:
        if datetime.strptime(str(row.date_of_travel), "%Y-%m-%d")<todays_date:
            cabs_list.append(row)
        elif datetime.strptime(str(row.date_of_travel), "%Y-%m-%d")==todays_date:
            if datetime.strptime(str(row.time_of_travel)[:5], "%H:%M")<datetime.strptime(str(current_time), "%H:%M"):
                cabs_list.append(row)
    
    if not cabs_list:
        redirect(URL('history_not_available'))
    
    return locals()

def history_not_available():
    return locals()

def upcoming_bookings():
    from datetime import datetime
    todays_date=str(request.now)
    current_time=todays_date[11:16]
    todays_date=todays_date[:10]
    todays_date=datetime.strptime(todays_date, "%Y-%m-%d")
    cabs_list=[]
    print current_time
    rows=db(db.shared_cab_details.user_id==auth.user.email).select()
    for row in rows:
        if row.status=='Successfull':
            if datetime.strptime(str(row.date_of_travel), "%Y-%m-%d")>todays_date:
                cabs_list.append(row)
            elif datetime.strptime(str(row.date_of_travel), "%Y-%m-%d")==todays_date:
                if datetime.strptime(str(row.time_of_travel)[:5], "%H:%M")>datetime.strptime(str(current_time), "%H:%M"):
                    cabs_list.append(row)

    if not cabs_list:
        redirect(URL('no_upcoming_bookings'))


    return locals()

def no_upcoming_bookings():
    return locals()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    try:
        if auth.user.is_admin:
            session.adminhere = 1
            redirect(URL('share_a_cab'))
    except Exception:
        # print ""
        session.adminhere1=1
        # redirect(URL('form_share_a_cabcab'))
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
