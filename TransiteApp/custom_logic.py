from sqlalchemy.orm import Session
from django.utils.html import escape
from django.core.mail import send_mail
import time
import os
import json
import datetime
import logging
import secrets
import traceback

import jwt
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from TransiteAPI.settings import BASE_DIR, engine

from .models import USERS  # ,USER_SESSION, USER_SESSION_WITH_DATA

user = "Farid"


head_columns_system = ["Status_N", "Yükün halı", "İcraçı", "Yükgöndərən", "Yükalan", "Yükün adı", "Pallet sayı", "Çəkisi", "Kub",
                       "Yükləmə tarixi", "Maşının nömrəsi", "Çexiyadan verilən qiymət EUR",
                       "Biz verdiyimiz qiymət EUR", "Biz verdiyimiz qiymət USD", "Biz verdiyimiz qiymət AZN",
                       "Daşıyıcıdan verilən qiymət EUR", "Daşıyıcıdan verilən qiymət USD", "Daşıyıcıdan verilən qiymət AZN",
                       "Daşıyıcıya nağd ödəniş EUR", "Daşıyıcıya nağd ödəniş USD", "Daşıyıcıya nağd ödəniş AZN",
                       "Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR", "Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD", "Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN",
                       "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR", "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD",
                       "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN", "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR",
                       "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD", "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN",
                       "Yükalanın ödəyəcəyi pul EUR", "Yükalanın ödəyəcəyi pul USD", "Yükalanın ödəyəcəyi pul AZN",
                       "Yükalanın ödədiyi pul EUR", "Yükalanın ödədiyi pul USD", "Yükalanın ödədiyi pul AZN",
                       "Yükalanın bizə borcu EUR", "Yükalanın bizə borcu USD", "Yükalanın bizə borcu AZN",
                       "Digər xərclər EUR", "Digər xərclər USD", "Digər xərclər AZN", "QEYD",
                       "İnvoice tarixi və nömrəsi", "T.1", "Ex.1", "İnvoice məbləği EUR", "İnvoice məbləği USD", "İnvoice məbləği AZN",
                       "İnvoice fayl", "Nağd alacağımız EUR", "Nağd alacağımız USD", "Nağd alacağımız AZN",
                       "Ödəniş Çexiya daxil olan EUR", "Ödəniş Çexiya daxil olan USD", "Ödəniş Çexiya daxil olan AZN",
                       "Ödəniş Türkiyə daxil olan EUR", "Ödəniş Türkiyə daxil olan USD", "Ödəniş Türkiyə daxil olan AZN",
                       "Ödəniş Azərbaycan daxil olan EUR", "Ödəniş Azərbaycan daxil olan USD", "Ödəniş Azərbaycan daxil olan AZN"]


head_columns_system_2 = ["Status_N", "Yükün halı", "İcraçı", "Yükgöndərən", "Yükalan", "Yükün adı", "Pallet sayı",
                         "Çəkisi", "Kub", "Yükləmə tarixi", "Maşının nömrəsi"]

head_columns_europe = ["Status_N", "Yükün halı", "İcraçı", "Yükgöndərən", "Yükalan", "Yükün adı", "Pallet sayı", "Çəkisi", "Kub",
                       "Yükləmə tarixi", "Maşının nömrəsi", "Çexiyadan verilən qiymət EUR",
                       "Biz verdiyimiz qiymət EUR", "Biz verdiyimiz qiymət USD", "Biz verdiyimiz qiymət AZN",
                       "Daşıyıcıdan verilən qiymət EUR", "Daşıyıcıdan verilən qiymət USD", "Daşıyıcıdan verilən qiymət AZN",
                       "Daşıyıcıya nağd ödəniş EUR",
                       "Daşıyıcıya nağd ödəniş USD", "Daşıyıcıya nağd ödəniş AZN", "Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR",
                       "Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD", "Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN",
                       "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR", "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD",
                       "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN", "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR",
                       "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD", "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN",
                       "Yükalanın ödəyəcəyi pul EUR", "Yükalanın ödəyəcəyi pul USD", "Yükalanın ödəyəcəyi pul AZN",
                       "Yükalanın ödədiyi pul EUR", "Yükalanın ödədiyi pul USD", "Yükalanın ödədiyi pul AZN",
                       "Yükalanın bizə borcu EUR", "Yükalanın bizə borcu USD", "Yükalanın bizə borcu AZN",
                       "Digər xərclər EUR", "Digər xərclər USD", "Digər xərclər AZN",
                       "QEYD", "Anbardan yüklənmə tarixi", "T.1", "Ex.1", "İnvoice tarixi və nömrəsi", "İnvoice məbləği EUR",
                       "İnvoice məbləği USD", "İnvoice məbləği AZN", "İnvoice fayl", "Nağd alacağımız EUR",
                       "Nağd alacağımız USD", "Nağd alacağımız AZN", "Ödəniş Çexiya daxil olan EUR", "Ödəniş Çexiya daxil olan USD",
                       "Ödəniş Çexiya daxil olan AZN", "Ödəniş Türkiyə daxil olan EUR", "Ödəniş Türkiyə daxil olan USD",
                       "Ödəniş Türkiyə daxil olan AZN", "Ödəniş Azərbaycan daxil olan EUR", "Ödəniş Azərbaycan daxil olan USD",
                       "Ödəniş Azərbaycan daxil olan AZN", "Yükün çatma tarixi"]

head_columns_europe_2 = ["Status_N", "Yükün halı", "İcraçı", "Yükgöndərən", "Yükalan", "Yükün adı", "Pallet sayı", "Çəkisi", "Kub",
                         "Yükləmə tarixi", "Maşının nömrəsi"]

head_columns_avia = ["Status_N", "Yükün halı", "İcraçı", "Çıxış aeroport", "Gəliş aeroport", "Yükgöndərən", "Yükalan", "Yükün adı",
                     "Pallet sayı", "Çəkisi", "Kub", "Yükləmə tarixi", "Aviaşirkətin adı", "Aviaşirkətdən verilən qiymət EUR",
                     "Biz verdiyimiz qiymət EUR", "Biz verdiyimiz qiymət USD", "Biz verdiyimiz qiymət AZN", "Daşıyıcıya nağd ödəniş EUR",
                     "Daşıyıcıdan verilən qiymət EUR", "Daşıyıcıdan verilən qiymət USD", "Daşıyıcıdan verilən qiymət AZN",
                     "Daşıyıcıya nağd ödəniş USD", "Daşıyıcıya nağd ödəniş AZN", "Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR",
                     "Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD", "Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN",
                     "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR", "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD",
                     "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN", "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR",
                     "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD", "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN",
                     "Digər xərclər EUR", "Digər xərclər USD", "Digər xərclər AZN",
                     "Yükalanın ödəyəcəyi pul EUR", "Yükalanın ödəyəcəyi pul USD", "Yükalanın ödəyəcəyi pul AZN",
                     "Yükalanın ödədiyi pul EUR", "Yükalanın ödədiyi pul USD", "Yükalanın ödədiyi pul AZN",
                     "Yükalanın bizə borcu EUR", "Yükalanın bizə borcu USD", "Yükalanın bizə borcu AZN",  "QEYD",
                     "İnvoice tarixi və nömrəsi", "İnvoice məbləği EUR", "İnvoice məbləği USD", "İnvoice məbləği AZN", "İnvoice fayl",
                     "Qaimə nömrəsi", "A.W.B", "Nağd alacağımız EUR", "Nağd alacağımız USD", "Nağd alacağımız AZN",
                     "Ödəniş Çexiya daxil olan EUR", "Ödəniş Çexiya daxil olan USD", "Ödəniş Çexiya daxil olan AZN", "Yükün çatma tarixi"]

head_columns_avia_2 = ["Status_N", "Yükün halı", "İcraçı", "Çıxış aeroport", "Gəliş aeroport", "Yükgöndərən", "Yükalan", "Yükün adı",
                       "Pallet sayı", "Çəkisi", "Kub", "Yükləmə tarixi", "Aviaşirkətin adı"]

head_columns_russia = ["Status_N", "Yükün halı", "İcraçı", "Yükgöndərən", "Yükalan", "Yükün adı", "Pallet sayı", "Çəkisi", "Kub",
                       "Yükləmə tarixi", "Maşının nömrəsi",
                       "Biz verdiyimiz qiymət EUR", "Biz verdiyimiz qiymət USD", "Biz verdiyimiz qiymət AZN", 
                       "Daşıyıcıya nağd ödəniş EUR", "Daşıyıcıya nağd ödəniş USD", "Daşıyıcıya nağd ödəniş AZN",
                       "Daşıyıcıdan verilən qiymət EUR", "Daşıyıcıdan verilən qiymət USD", "Daşıyıcıdan verilən qiymət AZN",
                       "Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR", "Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD",
                       "Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN", "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR",
                       "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD", "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN",
                       "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR", "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD",
                       "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN",
                       "Digər xərclər EUR", "Digər xərclər USD",
                       "Yükalanın ödəyəcəyi pul EUR", "Yükalanın ödəyəcəyi pul USD", "Yükalanın ödəyəcəyi pul AZN",
                       "Yükalanın ödədiyi pul EUR", "Yükalanın ödədiyi pul USD", "Yükalanın ödədiyi pul AZN",

                       "Yükalanın bizə borcu EUR", "Yükalanın bizə borcu USD", "Yükalanın bizə borcu AZN",
                       "Digər xərclər AZN", "QEYD", "İnvoice tarixi və nömrəsi",
                       "İnvoice məbləği EUR", "İnvoice məbləği USD", "İnvoice məbləği AZN",
                       "İnvoice fayl", 
                       "Nağd alacağımız EUR", "Nağd alacağımız USD", "Nağd alacağımız AZN",
                       "Ödəniş Çexiya daxil olan EUR", "Ödəniş Çexiya daxil olan USD",  "Ödəniş Çexiya daxil olan AZN",
                       "Ödəniş Türkiyə daxil olan EUR", "Ödəniş Türkiyə daxil olan USD", "Ödəniş Türkiyə daxil olan AZN",
                       "Ödəniş Azərbaycan daxil olan EUR", "Ödəniş Azərbaycan daxil olan USD", "Ödəniş Azərbaycan daxil olan AZN",
                       "Yükün çatma tarixi"]
head_columns_russia_2 = ["Status_N", "Yükün halı", "İcraçı", "Yükgöndərən", "Yükalan", "Yükün adı", "Pallet sayı", "Çəkisi", "Kub",
                         "Yükləmə tarixi", "Maşının nömrəsi"]

head_columns_container = ["Status_N", "Yükün halı", "İcraçı", "Yükgöndərən", "Yükalan", "Yükün adı", "Pallet sayı", "Çəkisi", "Kub",
                          "Dərəcəsi", "Yükləmə tarixi", "Daşıyan şirkətin adı", "Maşının nömrəsi", 
                          "Daşıyan şirkətdən alınan qiymət EUR", "Daşıyan şirkətdən alınan qiymət USD",
                          "Daşıyıcıdan verilən qiymət EUR", "Daşıyıcıdan verilən qiymət USD", "Daşıyıcıdan verilən qiymət AZN", 
                          "Biz verdiyimiz qiymət EUR", "Biz verdiyimiz qiymət USD", "Biz verdiyimiz qiymət AZN",
                          "Daşıyıcıya nağd ödəniş EUR", "Daşıyıcıya nağd ödəniş USD", "Daşıyıcıya nağd ödəniş AZN",
                          "Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR", "Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD",
                          "Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN", "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR",
                          "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD", "Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN",
                          "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR", "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD",
                          "Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN",

                          "Yükalanın bizə borcu EUR", "Yükalanın bizə borcu USD", "Yükalanın bizə borcu AZN",
                          "Yükalanın ödəyəcəyi pul EUR", "Yükalanın ödəyəcəyi pul USD", "Yükalanın ödəyəcəyi pul AZN",
                          "Yükalanın ödədiyi pul EUR", "Yükalanın ödədiyi pul USD", "Yükalanın ödədiyi pul AZN",
                          "Digər xərclər EUR", "Digər xərclər USD", "Digər xərclər AZN",
                          "QEYD", "İnvoice tarixi və nömrəsi",
                          "İnvoice məbləği EUR", "İnvoice məbləği USD", "İnvoice məbləği AZN",
                          "İnvoice fayl", 
                          "Nağd alacağımız EUR", "Nağd alacağımız USD", "Nağd alacağımız AZN",
                          "Ödəniş Çexiya daxil olan EUR", "Ödəniş Çexiya daxil olan USD", "Ödəniş Çexiya daxil olan AZN",
                          "Ödəniş Türkiyə daxil olan EUR", "Ödəniş Türkiyə daxil olan USD", "Ödəniş Türkiyə daxil olan AZN",
                          "Ödəniş Azərbaycan daxil olan EUR", "Ödəniş Azərbaycan daxil olan USD", "Ödəniş Azərbaycan daxil olan AZN",
                          "Yükün çatma tarixi"]

head_columns_container_2 = ["Status_N", "Yükün halı", "İcraçı", "Yükgöndərən", "Yükalan", "Yükün adı", "Pallet sayı", "Çəkisi", "Kub",
                            "Dərəcəsi", "Yükləmə tarixi", "Daşıyan şirkətin adı", "Maşının nömrəsi"]


def add_get_params(resp):
    resp["Access-Control-Allow-Origin"] = "*"
    resp["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT"
    resp["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"


def error_response(text_1, text_2="None", code=501):
    resp = JsonResponse({
        "error_text_1": text_1,
        "error_text_2": text_2,
        "error_status_code": code,

    })
    resp.status_code = code
    add_get_params(resp)
    return resp


@csrf_exempt
def contact_us(request):
    try:
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        print("Contact: ", full_name)
        print("Contact: ", email)
        print("Contact: ", message)
        print("Contact: ", phone)
        send_mail(
            "Contack-Us from: " + full_name,  # subject
            "User Email: "+'email'+" Request for discount: "+'message',  # message
            email,  # from email
            ["hebibliferid20@gmail.com", "cavidan5889@gmail.com",
                "dmp.bestrack@gmail.com", "prodigitrack.dmp@gmail.com"],
            html_message=message)
    except Exception as e:
        print("mail sending error: ", e)
    response = JsonResponse({
        'user_type': "user_type"
    })
    add_get_params(response)
    print("\033[92m Send mail SUCCESSFULLY" '\033[0m')
    return response


@csrf_exempt
def upload_sql_table(request):
    if request.method == 'POST':
        try:
            file_name = 'system_container'
            if token_verification(request)['is_admin'] != True:
                return error_response("Token verification error!", "Please sign in again!", 507)

            try:
                with Session(engine) as session:
                    # df = pd.read_csv(str(BASE_DIR) + '/Transite_Files/excel.csv')
                    df = pd.read_excel(
                        str(BASE_DIR) + '/Transite_Files/Sistem_Konteynr.xlsx', index_col=0)

                    df.to_sql(file_name, engine,
                              if_exists='replace', index=False)

            except Exception as e:
                my_traceback = traceback.format_exc()
                # logging.error(my_traceback)
                print('\33[91m my_traceback_612', my_traceback, '\33[0m')
                response = JsonResponse({'error_text': str(e),
                                         'error_text_2': my_traceback
                                         })
                print("err: ", e)
                response.status_code = 504
                add_get_params(response)
                # response['user_type'] = user_type
                return response

            try:
                with engine.connect() as con:
                    # query_1='ALTER TABLE '+file_name.lower()+ ' ALTER COLUMN '+file_name.lower() +'_ID SET NOT NULL;'
                    query_2 = 'ALTER TABLE '+file_name.lower() + ' ADD PRIMARY KEY (user_id);'
                    # con.execute(query_1)
                    con.execute(query_2)
            except Exception as e:
                print("\033[93m eerror in primari key: ", e)

            response = JsonResponse({
                'user_type': 'user_type'
            })
            add_get_params(response)

            print("\033[92m Uploaded to SQL DATABASE SUCCESSFULLY" '\033[0m')
            return response

        except Exception as e:
            my_traceback = traceback.format_exc()
            logging.error(my_traceback)
            response = JsonResponse({'error_text': str(e),
                                     'error_text_2': my_traceback
                                     })
            response.status_code = 504

            add_get_params(response)
            return response
    else:
        response = JsonResponse(
            {'Answer': "Sorry this method running only POST method. Thanks from DRL", })
        add_get_params(response)
        return response


@csrf_exempt
def login(request):
    try:
        if request.method != 'POST':
            return error_response("This function is working only with POST method.")

        user_type = ""
        mail = ""
        username = ""
        input_username = request.POST.get('input_username')
        input_password = request.POST.get('input_password')
        print("input_username: ", input_username)
        print("input_password: ", input_password)

        if not input_username or not input_password:
            return error_response("Username or Password is not!", code=509)

        with Session(engine) as session:
            sql_table = (
                session.query(
                    USERS.username, USERS.mail, USERS.first_name, USERS.last_name, USERS.password, USERS.user_type, USERS.user_id, USERS.region)
                .select_from(USERS).filter(USERS.username == input_username)
                .order_by(USERS.username))

            user = serializer(sql_table)[0]
            print("user: ", user)

            password = user['password']

            if password != input_password:
                return error_response("Password is wrong!", code=556)

            username = user['username']
            first_name = user['first_name']
            last_name = user['last_name']
            mail = user['mail']
            user_id = user['user_id']
            user_type = user['user_type']
            user_region = user['region']

            payload = {
                'id': user_id,
                'user_type': user_type,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
                'iat': datetime.datetime.utcnow()
            }

            new_token = jwt.encode(payload, 'Dragunov612', algorithm='HS256')

            session.query(USERS).\
                filter(USERS.user_id == user_id).\
                update({'user_token': new_token})

            session.commit()

            response = JsonResponse({
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'mail': mail,
                'user_id': user_id,
                'user_type': user_type,
                'user_token': new_token,
                'user_region': user_region,
            })

            add_get_params(response)
            return response

    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: "+str(e), my_traceback, 505)


@csrf_exempt
def token_verification(request):
    token = request.POST.get('input_token')
    if not token:
        return {'is_user': False, 'user_type': 'none_user'}
    try:
        payload = jwt.decode(token, 'Dragunov612', algorithms=['HS256'])
        user_type = payload['user_type']

        is_admin = False
        is_manager = False
        is_manager_minus = False

        is_user = False
        is_admin_minus = False
        if(user_type == 'admin'):
            is_admin = True
            is_admin_minus = True
            is_manager = True
            is_user = True

        if(user_type == 'admin_minus'):
            is_admin_minus = True
            is_manager = True
            is_user = True

        elif(user_type == 'manager'):
            is_manager = True
            is_user = True

        elif(user_type == 'manager_minus'):
            is_manager_minus = True
            is_user = True

        elif(user_type == 'user'):
            is_user = True

    except Exception as e:
        print("\033[91m token_verification_err: ", e, '\033[0m')
        return {'is_user': False, 'user_type': 'none_user'}

    return {'is_admin': is_admin, 'is_admin_minus': is_admin_minus, 'is_manager': is_manager, 'is_manager_minus': is_manager_minus, 'user_type': user_type, 'is_user': is_user}


@csrf_exempt
def check_user(request):
    try:
        if request.method != 'POST':
            return error_response("This function is working only with POST method.")

        if token_verification(request)['is_user'] != True:
            response = JsonResponse({'Answer': "Failed"})
            add_get_params(response)
            response.status_code = 205
            return response

        response = JsonResponse({'Answer': "Success"})
        add_get_params(response)
        return response

    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: "+str(e), my_traceback, 505)


def escape_dict(data):
    if isinstance(data, list):
        for x, l in enumerate(data):
            if isinstance(l, dict) or isinstance(l, list):
                escape_dict(l)
            else:
                if l is not None:
                    data[x] = escape(l)

    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict) or isinstance(v, list):
                escape_dict(v)
            else:
                if v is not None:
                    data[k] = escape(v)
        return data


def escape_list(data):
    return list(map(lambda item: escape(item), data))


def input_json_sanitizer(request, parameter):
    if request.method == "GET":
        data = json.loads(request.GET.get(parameter))
    elif request.method == "POST":
        data = json.loads(request.POST.get(parameter))

    if isinstance(data, list):
        return escape_list(data)
    if isinstance(data, dict):
        return escape_dict(data)


def input_get_list_sanitizer(request, parameter):
    if request.method == "GET":
        data_list = request.GET.getlist(parameter)
    elif request.method == "POST":
        data_list = request.POST.getlist(parameter)

    return escape_list(data_list)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def serializer(rows) -> list:
    "Return all rows from a cursor as a dict"
    return [dict(row) for row in rows]


def single_table_serializer(model):
    exceptions = ['registry', 'classes', 'prepare', 'metadata']
    result = []
    for item in model:
        fields = {}
        for field in [dir_item for dir_item in dir(item) if not dir_item.startswith("_") and "collection" not in dir_item and dir_item not in exceptions]:
            data = item.__getattribute__(field)
            if field == 'well':
                try:
                    data = item.__getattribute__(field).well_name
                except AttributeError:
                    pass
            fields[field] = data
        result.append(fields)
    return result


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_parametrization_marks(count: int) -> str:
    return " ".join(["?," if i != count else "?" for i in range(1, count + 1)])


def get_parametrization_values(data: dict) -> tuple:
    values = []
    for value in data.values():
        for item in value:
            values.append(item)
    return tuple(values)


def filename_content_search(data, input_data):
    # Will be filled with data
    data_to_response = []

    # Main logic
    if input_data['FileName'] and not input_data['KeyWords']:
        if "and" in input_data['FileName']:
            file_names = input_data['FileName'].split('and')
            for row in data:
                if all(file_name.replace(' ', '') in row['report_name'].lower() for file_name in file_names):
                    data_to_response.append(row)
        elif "or" in input_data['FileName']:
            file_names = input_data['FileName'].split('or')
            for row in data:
                if any(file_name.replace(' ', '') in row['report_name'].lower() for file_name in file_names):
                    data_to_response.append(row)
        else:
            for row in data:
                if input_data['FileName'] in row['report_name'].lower():
                    data_to_response.append(row)

    elif not input_data['FileName'] and input_data['KeyWords']:
        if "and" in input_data['KeyWords']:
            key_words = input_data['KeyWords'].split('and')
            for row in data:
                try:
                    if all(key_word.replace(' ', '') in row['report_content'] for key_word in key_words):
                        data_to_response.append(row)
                except TypeError:
                    continue
        elif "or" in input_data['KeyWords']:
            key_words = input_data['KeyWords'].split('or')
            for row in data:
                try:
                    if any(key_word.replace(' ', '') in row['report_content'] for key_word in key_words):
                        data_to_response.append(row)
                except TypeError:
                    continue
        else:
            for row in data:
                try:
                    if input_data['KeyWords'] in row['report_content']:
                        data_to_response.append(row)
                except TypeError:
                    continue

    elif input_data['FileName'] and input_data['KeyWords']:
        if "and" in input_data['FileName'] and "and" in input_data['KeyWords']:
            file_names = input_data['FileName'].split('and')
            key_words = input_data['KeyWords'].split('and')
            for row in data:
                try:
                    if all(file_name.replace(' ', '') in row['report_name'].lower() for file_name in
                           file_names) and all(key_word.replace(' ', '') in row['report_content'] for key_word in key_words):
                        data_to_response.append(row)
                except TypeError:
                    continue
        elif "or" in input_data['FileName'] and "or" in input_data['KeyWords']:
            file_names = input_data['FileName'].split('or')
            key_words = input_data['KeyWords'].split('or')
            for row in data:
                try:
                    if any(file_name.replace(' ', '') in row['report_name'].lower() for file_name in
                           file_names) and any(key_word.replace(' ', '') in row['report_content'] for key_word in key_words):
                        data_to_response.append(row)
                except TypeError:
                    continue
        elif "or" in input_data['FileName'] and "and" in input_data['KeyWords']:
            file_names = input_data['FileName'].split('or')
            key_words = input_data['KeyWords'].split('and')
            for row in data:
                try:
                    if any(file_name.replace(' ', '') in row['report_name'].lower() for file_name in
                           file_names) and all(key_word.replace(' ', '') in row['report_content'] for key_word in key_words):
                        data_to_response.append(row)
                except TypeError:
                    continue
        elif "and" in input_data['FileName'] and "or" in input_data['KeyWords']:
            file_names = input_data['FileName'].split('and')
            key_words = input_data['KeyWords'].split('or')
            for row in data:
                try:
                    if all(file_name.replace(' ', '') in row['report_name'].lower() for file_name in
                           file_names) and any(key_word.replace(' ', '') in row['report_content'] for key_word in key_words):
                        data_to_response.append(row)
                except TypeError:
                    continue
        elif "and" in input_data['FileName'] and not ("or" in input_data['KeyWords'] or "and" in input_data['KeyWords']):
            file_names = input_data['FileName'].split('and')
            for row in data:
                try:
                    if all(file_name.replace(' ', '') in row['report_name'].lower() for file_name in file_names) and input_data['KeyWords'] in row['report_content']:
                        data_to_response.append(row)
                except TypeError:
                    continue
        elif "or" in input_data['FileName'] and not ("or" in input_data['KeyWords'] or "and" in input_data['KeyWords']):
            file_names = input_data['FileName'].split('or')
            for row in data:
                try:
                    if any(file_name.replace(' ', '') in row['report_name'].lower() for file_name in file_names) and input_data['KeyWords'] in row['report_content']:
                        data_to_response.append(row)
                except TypeError:
                    continue
        elif "and" in input_data['KeyWords'] and not ("or" in input_data['FileName'] or "or" in input_data['FileName']):
            key_words = input_data['KeyWords'].split('and')
            for row in data:
                try:
                    if input_data['FileName'] in row['report_name'].lower() and all(key_word.replace(' ', '') in row['report_content'] for key_word in key_words):
                        data_to_response.append(row)
                except TypeError:
                    continue
        elif "or" in input_data['KeyWords'] and not ("or" in input_data['FileName'] or "or" in input_data['FileName']):
            key_words = input_data['KeyWords'].split('or')
            for row in data:
                try:
                    if input_data['FileName'] in row['report_name'].lower() and any(key_word.replace(' ', '') in row['report_content'] for key_word in key_words):
                        data_to_response.append(row)
                except TypeError:
                    continue
        else:
            for row in data:
                try:
                    if input_data['FileName'] in row['report_name'].lower() and input_data['KeyWords'] in row['report_content']:
                        data_to_response.append(row)
                except TypeError:
                    continue

    return data_to_response
