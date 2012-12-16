#Required to add our salt, hashed pwd & uuid4
from quetzal.cryptography import operations as crypt_ops
from quetzal.authentication import auth

#Get User schema
from quetzal.schemas import users as user_schema
Users = user_schema.Users



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





def addUser(userObj):
    try:
        if userObj['is_default']=="true" and not userObj['priv_lev'] == "2":
            return "err", "UNABLE_TO_STABLISH_DEFAULT_TO_NON_ADMIN"
        #Set salt'n hashed password
        if 'password' in userObj:
            password = userObj['password']
            #Do not store private user password
            del userObj['password']
            userObj['salt'] = crypt_ops.get_a_bunch_of_salt()
            userObj['hashed_pwd'] = auth.get_hashed_password(password, userObj['salt'])
        #generate a base 64 uuid type 4
        #http://stackoverflow.com/a/786541/1747721
        userObj['userid'] = crypt_ops.get_base64_uuid4()
        try:
            #Remove default from current user who has this token
            if userObj['is_default']=="true":
                remove_default_to = Users.objects(isdefault='true').update(
                    set__isdefault = "false"
                )
        except Exception as e:
            pass
        try:
            #Save new user into "User" schema
            Users(
                name        = userObj['name'],
                username    = userObj['username'],
                salt        = userObj['salt'],
                hashed_pwd  = userObj['hashed_pwd'],
                priv_lev    = userObj['priv_lev'],
                userid      = userObj['userid'],
                email       = userObj['email'],
                isdefault   = userObj['is_default'],
                tokens      = []
            ).save()
            return "ok", userObj
        except Exception as e:
            raise StandardError(e)
    except Exception as e:
        raise StandardError(e)





def updateUser(userObj):
    try:

        if userObj['is_default']=="true" and not userObj['priv_lev'] == "2":
            return "err", "UNABLE_TO_STABLISH_DEFAULT_TO_NON_ADMIN"
        try:
            #Get user with Id
            current_user = Users.objects.get(id=userObj['oid'])
        except Exception as e:
            raise StandardError("User Not Found")

        #Set salt'n hashed password
        if 'current_password' and 'new_password' in userObj:
            current_password    = userObj['current_password']
            new_password        = userObj['new_password']
            del userObj['current_password']
            del userObj['new_password']

        try:
            #Try to remove default from user who has that token, to this always at the end
            if userObj['is_default']=="true":
                remove_default_to = Users.objects(isdefault='true').update(
                    set__isdefault = "false"
                )
        except: pass

        #Trying to update password?
        if len(current_password)>0 or len(new_password)>0:
            #Verify if current password provided matches with the one in mongo
            #To updt pwd manually just remove the following 2 lines
            if not auth.is_password_match(current_password, current_user['hashed_pwd'], current_user['salt']):
                return "err", "CURRENT_PASSWORD_NOT_VALID"
            if not len(new_password)>5:
                return "err", "MUST_PROVIDE_NEW_PASSWORD"
            if current_password == new_password:
                return "err", "PASSWORDS_MUST_NOT_BE_THE_SAME"
            #Generate salt and hashed password for new password
            userObj['salt'] = crypt_ops.get_a_bunch_of_salt()
            userObj['hashed_pwd'] = auth.get_hashed_password(new_password, userObj['salt'])
            #Update Query With Password
            update_results = Users.objects(id=userObj['oid']).update(
                set__name           = userObj['name'],
                set__username       = userObj['username'],
                set__email          = userObj['email'],
                set__salt           = userObj['salt'],
                set__hashed_pwd     = userObj['hashed_pwd'],
                set__priv_lev       = int(userObj['priv_lev']),
                set__isdefault     = userObj['is_default']
            )
        else:
            #Update Query without password
            update_results = Users.objects(id=userObj['oid']).update(
                set__name           = userObj['name'],
                set__username       = userObj['username'],
                set__email          = userObj['email'],
                set__priv_lev       = int(userObj['priv_lev']),
                set__isdefault     = userObj['is_default']
            )

        if not update_results==1:
            #Oops! something went wrong
            raise StandardError("Unable to update user data")

        #Return user object
        r_obj = exclude_fields(userObj)
        return "ok", r_obj

    except Exception as e:
        raise StandardError(e)





def addFirstUser(userObj):
    try:
        #Set salt'n hashed password
        if 'password' in userObj:
            password = userObj['password']
            #Do not store private user password
            del userObj['password']
            userObj['salt'] = crypt_ops.get_a_bunch_of_salt()
            userObj['hashed_pwd'] = auth.get_hashed_password(password, userObj['salt'])

        #generate a base 64 uuid type 4
        #http://stackoverflow.com/a/786541/1747721
        userObj['userid'] = crypt_ops.get_base64_uuid4()

        #Save new user into "User" schema
        Users(
            name        = userObj['name'],
            username    = userObj['username'],
            salt        = userObj['salt'],
            hashed_pwd  = userObj['hashed_pwd'],
            priv_lev    = userObj['priv_lev'],
            userid      = userObj['userid'],
            email       = userObj['email'],
            isdefault   = userObj['is_default'],
            tokens      = []
        ).save()
        r_obj = exclude_fields(userObj)
        return r_obj
    except Exception as e:
        raise StandardError(e)


def delUser(oid):
    try:
        user = Users.objects.get(id=oid)
        if user['isdefault']=="true":
            return "err", "UNABLE_TO_DELETE_DEFAULT_USER"
        else:
            Users.objects(id=oid).delete()
            return "ok", "USER_REMOVED"
    except Exception as e:
        raise StandardError(e)