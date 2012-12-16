from quetzal.utils import serializers
from quetzal.cryptography import operations as crypt_ops
from quetzal.authentication import auth
import web

#Get mysql sessions
from quetzal.database import dbs
mysql = dbs.DBS.getSqlDatabase('mysql')

#Get User schema
from quetzal.schemas import users as user_schema
Users = user_schema.Users

#Load Quetzal configuration
from quetzal import conf
quetzal_config = conf.QuetzalConfig.load()

#Quetzal config statics
qdays = quetzal_config['session_time']['days']
qseconds = quetzal_config['session_time']['seconds']
qminutes = quetzal_config['session_time']['minutes']
qhours = quetzal_config['session_time']['hours']

#Set token life time
import datetime
token_lifetime = datetime.timedelta(days=qdays, seconds=qseconds, minutes=qminutes, hours=qhours)





def getTokenData():
    try:

        session_id = web.cookies().get('session_id')
        mysql_query = mysql.fetch_one("""
                    SELECT * FROM sessions
                WHERE session_id=%s
            """, (str(session_id)))
        session_fields = mysql_query

        if session_fields != None:
            session_data_encoded = session_fields[2]
        else:
            raise err.NotFoundError("Error, no session found")

        return crypt_ops.transform_session_data(session_data_encoded)

    except Exception as e:
        return str(e)




def getUserFromToken():
    tokenData = getTokenData()
    ret_value = Users.objects()._collection.find_one({'userid':tokenData['userid']})
    if not ret_value is None:
        return serializers.SerializeObject(ret_value)
    return "user not in token"





#Exclude private fields from returned user
def exclude_fields(userObj):
    #
    excl = {
        'hashed_pwd','_id', 'tokens', 'salt'
    }
    for key in excl:
        if key in userObj:
            del userObj[key]
    return userObj





#Compare what you have against the database
def authenticate():
    try:
        the_user = getUserFromToken()
        session_data = getTokenData()
        if auth.is_token_expired(session_data['token'], token_lifetime):
            raise StandardError("Token Expired")

        #Compare token session_data/user_data
        #if token matches authentication is Okay
        for token in the_user['tokens']:
            #user token is still valid with session token
            if token == session_data['token']:
                #Return authenticated user with public fields
                r_dict = dict(r='ok')
                r_dict['data'] = exclude_fields(the_user)
                #returns true
                return r_dict
    except Exception as e:
        raise StandardError("Unable to authenticate user with session")

    #This may be an attempt of cookie stealing and/or session hijacking
    #http://en.wikipedia.org/wiki/Session_hijacking
    #EXCEPTION #8, Login hacking attempt
    raise StandardError("Not Allowed")





def login(username, password):
    try:
        session = web.ctx.session
    except Exception as e:
        raise StandardError(e)
    try:
        the_user = Users.objects.get(username=username)
    except Exception as e:
        raise StandardError("User Not Found")
    if not auth.is_password_match(password, the_user['hashed_pwd'], the_user['salt']):
        raise StandardError("Password do not match")
    try:
        #Generate a random token that will be compared from session data against user token
        created_token = auth.create_token(the_user['userid'])
        #set this token in session
        session.token = created_token
        #Set other session values
        session.userid = the_user['userid']
        session.authenticated = True
        session.priv_lev = the_user['priv_lev']

        #Update user tokens
        #MongoDb/MongoEngine Using Atomic Updates
        #mongodb.users.update( { 'username': dbUser['username'] },
        #{ '$set': { 'tokens':dbUser['tokens'] } }
        #)
        #Update Query in MongoEngine
        #https://github.com/hmarr/mongoengine/blob/master/docs/guide/querying.rst
        Users.objects(username=the_user['username']).update_one(
            push__tokens = created_token
            #set__tokens__S = created_token
        )

        #Remove expired tokens from curent user
        for token in the_user['tokens']:
            if auth.is_token_expired(token, token_lifetime):
                token_exp.append(token)
                Users.objects(username=the_user['username']).update_one(
                    pull__tokens = token
                )

        #Get Our user object.
        user_obj = Users.objects.get(username=the_user['username'])
        ret_obj = {}

        ret_obj['userid'] = serializers.SerializeObject(user_obj['userid'])
        ret_obj['name'] = serializers.SerializeObject(user_obj['name'])
        ret_obj['username'] = serializers.SerializeObject(user_obj['username'])
        ret_obj['priv_lev'] = serializers.SerializeObject(user_obj['priv_lev'])

        r_dict = dict(r='ok',data=ret_obj)
        #returns true
        return r_dict

    except Exception as e:
        raise StandardError(e)

    #Hacking attempt
    raise StandardError("Not Allowed")





def logout():
    try:
        session = web.ctx.session
    except Exception as e:
        pass
    try:
        the_user = getUserFromToken()
        session_data = getTokenData()
        #Remove utilized token
        for token in the_user['tokens']:

            if token == session_data['token']:
                #Remove token from user
                Users.objects(username=the_user['username']).update_one(
                    pull__tokens = token
                )
                return dict(r='ok')
            #Leave session & cookie to remember user data such as prefered language, remember user and so on
        #If token not in iteration just raise error
        raise StandardError("token does not exists")
    except Exception as e:
        return StandardError(e)
        #remove session record if logout fails from database
        session.kill()
        web.setcookie(quetzal_config['cookie_name'], '', expires=-1)
        raise StandardError("Error During Logout, Session terminated anyway")






def auth_admin_res():
    try:
        auth_user = authenticate()
        priv_level = auth_user['data']['priv_lev']
        if int(priv_level)==2:
            return auth_user
        raise StandardError("Not An Admin")
    except Exception as e:
        raise StandardError(e)






def auth_priv_res():
    try:
        auth_user = authenticate()
        priv_level = auth_user['data']['priv_lev']
        if int(priv_level)==1:
            return auth_user
        raise StandardError("Not a private Admin")
    except Exception as e:
        raise StandardError(e)