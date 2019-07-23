import json
from flask import Blueprint
from flask import Flask, render_template, request,send_from_directory,Response
import db_helper as db
from random import randint
user_api = Blueprint('user_api', __name__,template_folder="templates")

def getSixDigitCode():
   return randint(99999,1000000)

@user_api.route("/verificationcode/<uid>", methods = ['POST'])
def generateVerificationCode(uid):
    assert uid == request.view_args['uid']
    code=getSixDigitCode()
    resp=db.saveSixDigitVerificationCode(uid,code)
    if(resp is not None):
        return Response(json.dumps(resp),mimetype="application/json",status=200)
    else:
        resp['Error']='There is some error while generating 6 digit code'
        return Response(json.dumps(resp),mimetype="application/json",status=500)

@user_api.route("/verificationcode/<code>", methods = ['GET'])
def checkVerificationCode(code):
    assert code == request.view_args['code']
    resp=db.checkSixDigitVerificationCode(code)
    if bool(resp):
        resp['Status']="valid"
    else:
        resp['Status']="invalid"
    return Response(json.dumps(resp),mimetype="application/json",status=200)

    



