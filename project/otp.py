import random
from flask_cors import CORS, cross_origin
from twilio.rest import Client
from flask import jsonify, Blueprint, session, request, make_response
from twilio.base.exceptions import TwilioRestException
from application import redis_client



otp = Blueprint('otp', __name__)
CORS(otp)

""" Sending an OTP to the uses's Mobile Number. When user will enter that OTP which he received on his/her mobile number,
    if it matches to the OTP stored in list "otp_list", then user will be allowed to login. """

def error_message(status_code, sub_code, message, action):
    """
        This Function is to send error messages.
    """
    response = jsonify({
        'status': 'error',
        'status_code': status_code,
        'sub_code': sub_code,
        'message': message,
        'action': action
    })
    response.status_code = status_code
    return response


def success_message(status_code, message):
    """
        This Function is to send success message. 
    """
    response = jsonify({
        'status': 'success',
        'status_code': status_code,
        #'sub_code': sub_code,
        'message': message,
        #'action': action
    })
    response.status_code = status_code
    return response




@otp.route('/api/v1/otp', methods=['POST'])
@cross_origin()
def send_otp():
    """ This Function sends OTP to user's mobile number. """
    try:
        account_sid = 'AC2b7a69d47759b9f8a9753a78eea1b25e'
        auth_token = '88f1eadcc668238445dcfd1ba32ca748'
        client = Client(account_sid, auth_token)
        #send_otp_args = reqparse.RequestParser()
        #send_otp_args.add_argument("mobileNumber", type=str)
        
      
        mobileNumber = request.json['mobileNumber']
        if not mobileNumber:
            return error_message(400, 42, "Mobile Number not found.", "Please add a valid Moble Number.")
    
        
        #print(mobileNumber)
        #args = send_otp_args.parse_args()
        #print(args)
        # random 6 digit number
        rand_num = str(random.randrange(100000, 1000000))
        message = client.messages.create(
            body=rand_num,
            from_='+12162085998',
            to=mobileNumber
        )
        print(message.sid)
        redis_client.set(mobileNumber, rand_num) 
        redis_client.expire(mobileNumber, 600)
        #print("redis key", redis_key) 
        #adding otp to session
        #session['response'] = rand_num
        session['mobileNumber'] = mobileNumber
        data = {
            "OTP": rand_num,
            "from": "+12162085998",
            "to": session['mobileNumber'],
            #"rand_otp": rand_otp
        }

        #return jsonify(data)
        return success_message(200, "OTP send successfully!")
    except TwilioRestException as t:
        # Implement your fallback code
        print(t)
        return error_message(400, 42, "Exception Occured.", "Something went wrong.")
    except Exception as e:
        print(e)
        return error_message(400, 42, "Exception Occured.", "Something went wrong.")

@otp.route('/api/v1/otp/verify', methods=['POST'])
def verify_otp():
    """ This Function varifies the otp provided by the user. """
    try:
        #schema = SendOtoSchema()
        #verify_otp_args = reqparse.RequestParser()
        #verify_otp_args.add_argument("verify_otp", type=str)

        #args = verify_otp_args.parse_args()

        user_otp = str(request.json['verify_otp'])

        if len(user_otp)==0:
            return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="OTP required !!"'}
        )


        #verify = schema.load(request.get_json())
        if redis_client.exists(session['mobileNumber']):
            res = str(redis_client.get(session['mobileNumber']))
            #session.pop('mobileNumber', None)
            if res[2:8] == user_otp:
                return success_message(200, "You are verified Successfully.")
            else:
                print(type(res), res, type(user_otp), user_otp)
                return error_message(400, 42, "Something went wrong.","Please try again.")
            print(res)
        else:
            return jsonify({"result":"Please ask for new OTP by clicking on send otp. "})
       
    except Exception as e:
        print(e)


# @otp.route('/api/v1/otp/verify', methods=['POST'])
# def verify_otp():
#     """ This Function varifies the otp provided by the user. """
#     try:
#         mobileNumber = request.json['mobileNumber']
#         user_otp = request.json['verify_otp']
#         if not mobileNumber or not user_otp:
#             return make_response(
#             'Could not verify',
#             401,
#             {'WWW-Authenticate' : 'Basic realm ="OTP required !!"'}
#         )

#         if redis_client.exists(mobileNumber):
#             res = str(redis_client.get(session['mobileNumber']))
#             if res[2:8] == user_otp:
#                 return jsonify({"result":"You are verified Successfully."})
#             else:
#                 print(type(res), res, type(user_otp), user_otp)
#                 return jsonify({"result":"Please try again."})
#             print(res)
#         else:
#             return jsonify({"result":"Please ask for new OTP by clicking on send otp. "})
       
#     except Exception as e:
#         print(e)

            
        
"""

        if 'response' in session:
            s = session['response']
            session.pop('response', None)
            if s==user_otp:
                return 'You are Verified Successfully.'
            else:
                return 'Please Try again.'
        else:
            return 'Please Click on send otp.'
"""
        
        


   

"""
    for i in data.keys():
        print(i)

    try:
        verify_otp_args = reqparse.RequestParser()
        verify_otp_args.add_argument("otp_verify", type=str)
        verify_args = verify_otp.parse_args()

        value = redis_client.get('mobileNumber')
        
        if verify_args['otp_verify'] == redis_client.get(verify_args['mobile_number']):
            return {"status": "otp matched", "otp": value}
        else:
            return {"status": "otp not matched, try again", "otp":value}
        
    except Exception as e:
        print(e)
        
"""



"""

class Otp(Resource):
    def post():
        try:
            account_sid = 'AC2b7a69d47759b9f8a9753a78eea1b25e'
            auth_token = '88f1eadcc668238445dcfd1ba32ca748'
            client = Client(account_sid, auth_token)
            send_otp_args = reqparse.RequestParser()
            send_otp_args.add_argument("mobileNumber", type=str)

            args = send_otp_args.parse_args()
            print(args)
            # random 6 digit number
            rand_num = str(random.randrange(100000, 1000000))
            message = client.messages.create(
                body=rand_num,
                from_='+12162085998',
                to=args['mobileNumber']
            )
            print(message.sid)
            rand_otp.clear()
            rand_otp.append(rand_num)
            data = {
                "OTP": rand_num,
                "from": "+12162085998",
                "to": args['mobileNumber'],
                "rand_num": rand_num,
                "rand_otp": rand_otp
            }
            return jsonify(data)
        except TwilioRestException as e:
            # Implement your fallback code
            print(e)

    def get():
        try:
            otp = ''
            if len(rand_otp) != 0:
                if otp == rand_otp[0]:
                    return {"status": "otp matched", "otp": otp, "rand_opt": rand_otp}
                else:
                    return {"status": "otp not matched, try again", "otp": otp, "rand_otp": rand_otp}
            else:
                return {"status": "otp not matched, try again", "otp": otp, "rand_otp": rand_otp}
        except Exception as e:
            print(e)
            
            """
            
        
