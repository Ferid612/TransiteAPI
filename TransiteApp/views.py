from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
import traceback
from TransiteAPI.settings import engine
from sqlalchemy.orm import Session
from .custom_logic import *
from .models import System_table, System_avia, System_russia, System_europe, System_container
import pandas as pd
from django.http import HttpResponse
from datetime import datetime


@csrf_exempt
def testing(request):
    # Build the POST parameters
    if request.method == 'POST':
        try:
            response = JsonResponse({'Answer': "Success", })
            # response.status_code=501
            add_get_params(response)
            return response
        except Exception as e:
            my_traceback = traceback.format_exc()

            logging.error(my_traceback)
            response = JsonResponse({
                                    'error_text': str(e),
                                    'error_text_2': my_traceback
                                    })
            response.status_code = 505

            add_get_params(response)
            return response
    else:
        response = JsonResponse(
            {'Answer': "This promerty only for POST method.", })
        response.status_code = 501
        add_get_params(response)
        return response


@csrf_exempt
def get_table(request):
    # Build the POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")

    try:
        if token_verification(request)['is_user'] != True:
            return error_response("Token verification error!", "Please sign in again!", 505)

        user_region = request.POST.get('user_region')

        data_table = ""
        head_columns = ""

        selected_region = request.POST.get('selected_region')
        if token_verification(request)['is_admin_minus'] != True:

            if(user_region == 'All'):
                data_table = System_table
                head_columns = head_columns_system

            elif(user_region == 'Europe'):
                data_table = System_europe
                head_columns = head_columns_europe

            elif(user_region == 'Avia'):
                data_table = System_avia
                head_columns = head_columns_avia

            elif(user_region == 'Russia'):
                data_table = System_russia
                head_columns = head_columns_russia

            elif(user_region == 'Container'):
                data_table = System_container
                head_columns = head_columns_container

        else:
            if(selected_region == 'System'):
                data_table = System_table
                head_columns = head_columns_system

            elif(selected_region == 'Europe'):
                data_table = System_europe
                head_columns = head_columns_europe

            elif(selected_region == 'Avia'):
                data_table = System_avia
                head_columns = head_columns_avia

            elif(selected_region == 'Russia'):
                data_table = System_russia
                head_columns = head_columns_russia

            elif(selected_region == 'Container'):
                data_table = System_container
                head_columns = head_columns_container

        if token_verification(request)['is_manager_minus'] == True:

            if(user_region == 'All'):
                head_columns = head_columns_system_2

            elif(user_region == 'Europe'):
                head_columns = head_columns_europe_2

            elif(user_region == 'Avia'):
                head_columns = head_columns_avia_2

            elif(user_region == 'Russia'):
                head_columns = head_columns_russia_2

            elif(user_region == 'Container'):
                head_columns = head_columns_container_2

        with Session(engine) as session:
            example_table = session.query(data_table)
            table_name = ""
            example_table_serialized = single_table_serializer(example_table)

            example_df = pd.DataFrame(
                example_table_serialized, columns=head_columns)

            if token_verification(request)['is_manager_minus'] != True:

                invoice_mebleq_eur = example_df['İnvoice məbləği EUR'].sum()
                invoice_mebleq_usd = example_df['İnvoice məbləği USD'].sum()
                invoice_mebleq_azn = example_df['İnvoice məbləği AZN'].sum()

                odenis_chexiya_daxil_olan_eur = example_df['Ödəniş Çexiya daxil olan EUR'].sum()
                odenis_chexiya_daxil_olan_usd = example_df['Ödəniş Çexiya daxil olan USD'].sum()
                odenis_chexiya_daxil_olan_azn = example_df['Ödəniş Çexiya daxil olan AZN'].sum()


                dasiyiciya_nagd_odenis_eur = example_df['Daşıyıcıya nağd ödəniş EUR'].sum()
                dasiyiciya_nagd_odenis_usd = example_df['Daşıyıcıya nağd ödəniş USD'].sum()
                dasiyiciya_nagd_odenis_azn = example_df['Daşıyıcıya nağd ödəniş AZN'].sum()

                dasiyiciya_kocurme_odenis_chexiya_eur = 0
                dasiyiciya_kocurme_odenis_chexiya_usd = 0
                dasiyiciya_kocurme_odenis_chexiya_azn = 0

                dasiyiciya_kocurme_odenis_turkiye_eur = 0
                dasiyiciya_kocurme_odenis_turkiye_usd = 0
                dasiyiciya_kocurme_odenis_turkiye_azn = 0

                dasiyiciya_kocurme_odenis_azerbaycan_eur = 0
                dasiyiciya_kocurme_odenis_azerbaycan_usd = 0
                dasiyiciya_kocurme_odenis_azerbaycan_azn = 0
                try:

                    dasiyiciya_kocurme_odenis_chexiya_eur = example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR'].sum()
                    dasiyiciya_kocurme_odenis_chexiya_usd = example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD'].sum()
                    dasiyiciya_kocurme_odenis_chexiya_azn = example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN'].sum()

                    dasiyiciya_kocurme_odenis_turkiye_eur = example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR'].sum()
                    dasiyiciya_kocurme_odenis_turkiye_usd = example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD'].sum()
                    dasiyiciya_kocurme_odenis_turkiye_azn = example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN'].sum()

                    dasiyiciya_kocurme_odenis_azerbaycan_eur = example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR'].sum()
                    dasiyiciya_kocurme_odenis_azerbaycan_usd = example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD'].sum()
                    dasiyiciya_kocurme_odenis_azerbaycan_azn = example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN'].sum()
                except Exception as e:
                    print("exception sum: ", str(e))

                diger_xercler_eur = example_df['Digər xərclər EUR'].sum()
                diger_xercler_usd = example_df['Digər xərclər USD'].sum()
                diger_xercler_azn = example_df['Digər xərclər AZN'].sum()

                # Net mebleg: invoice - (chexx + dasiyici + diger)

                net_mebleg_eur = invoice_mebleq_eur - \
                    (odenis_chexiya_daxil_olan_eur +
                     dasiyiciya_nagd_odenis_eur + diger_xercler_eur)
                net_mebleg_usd = invoice_mebleq_usd - \
                    (odenis_chexiya_daxil_olan_usd +
                     dasiyiciya_nagd_odenis_usd + diger_xercler_usd)
                net_mebleg_azn = invoice_mebleq_azn - \
                    (odenis_chexiya_daxil_olan_azn +
                     dasiyiciya_nagd_odenis_azn + diger_xercler_azn)

                # sum two columns and create report

                example_df['Yükalanın ödədiyi pul EUR'] = example_df['Yükalanın ödədiyi pul EUR'].fillna()
                example_df['Yükalanın ödədiyi pul USD'] = example_df['Yükalanın ödədiyi pul USD'].fillna()
                example_df['Yükalanın ödədiyi pul AZN'] = example_df['Yükalanın ödədiyi pul AZN'].fillna()

                example_df['Yükalanın ödəyəcəyi pul EUR'] = example_df['Yükalanın ödəyəcəyi pul EUR'].fillna()
                example_df['Yükalanın ödəyəcəyi pul USD'] = example_df['Yükalanın ödəyəcəyi pul USD'].fillna()
                example_df['Yükalanın ödəyəcəyi pul AZN'] = example_df['Yükalanın ödəyəcəyi pul AZN'].fillna()

                example_df['Yükalanın bizə borcu EUR'] = example_df['Yükalanın ödəyəcəyi pul EUR'] - \
                    example_df['Yükalanın ödədiyi pul EUR']
                example_df['Yükalanın bizə borcu USD'] = example_df['Yükalanın ödəyəcəyi pul USD'] - \
                    example_df['Yükalanın ödədiyi pul USD']
                example_df['Yükalanın bizə borcu AZN'] = example_df['Yükalanın ödəyəcəyi pul AZN'] - \
                    example_df['Yükalanın ödədiyi pul AZN']

                yukalanlarin_bize_borcu_eur = example_df['Yükalanın bizə borcu EUR'].sum()
                yukalanlarin_bize_borcu_usd = example_df['Yükalanın bizə borcu USD'].sum()
                yukalanlarin_bize_borcu_azn = example_df['Yükalanın bizə borcu AZN'].sum()

                example_df['Daşıyıcıya nağd ödəniş EUR'] = example_df['Daşıyıcıya nağd ödəniş EUR'].fillna(0)
                example_df['Daşıyıcıya nağd ödəniş USD'] = example_df['Daşıyıcıya nağd ödəniş USD'].fillna(0)
                example_df['Daşıyıcıya nağd ödəniş AZN'] = example_df['Daşıyıcıya nağd ödəniş AZN'].fillna(0)

                try:
                    example_df['Daşıyıcıdan verilən qiymət EUR'] = example_df['Daşıyıcıdan verilən qiymət EUR'].fillna(0)
                    example_df['Daşıyıcıdan verilən qiymət USD'] = example_df['Daşıyıcıdan verilən qiymət USD'].fillna(0)
                    example_df['Daşıyıcıdan verilən qiymət AZN'] = example_df['Daşıyıcıdan verilən qiymət AZN'].fillna(0)
                except Exception as e:
                    print("Error handling daşıyıcıdan: ", e)
                    example_df['Daşıyıcıdan verilən qiymət EUR'] = 0
                    example_df['Daşıyıcıdan verilən qiymət USD'] = 0
                    example_df['Daşıyıcıdan verilən qiymət AZN'] = 0

                example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR'] = example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR'].fillna(0)
                example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD'] = example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD'].fillna(0)
                example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN'] = example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN'].fillna(0)

                example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR'] = example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR'].fillna(0)
                example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD'] = example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD'].fillna(0)
                example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN'] = example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN'].fillna(0)

                example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR'] = example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR'].fillna(0)
                example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD'] = example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD'].fillna(0)
                example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN'] = example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN'].fillna(0)

                example_df['Daşıyıcıya qalıq borc EUR'] = example_df['Daşıyıcıdan verilən qiymət EUR'] - (
                    example_df['Daşıyıcıya nağd ödəniş EUR'] + example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı EUR'] + example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı EUR'] + example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı EUR'])
                example_df['Daşıyıcıya qalıq borc USD'] = example_df['Daşıyıcıdan verilən qiymət USD'] - (
                    example_df['Daşıyıcıya nağd ödəniş USD'] + example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı USD'] + example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı USD'] + example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı USD'])
                example_df['Daşıyıcıya qalıq borc AZN'] = example_df['Daşıyıcıdan verilən qiymət AZN'] - (
                    example_df['Daşıyıcıya nağd ödəniş AZN'] + example_df['Daşıyıcıya köçürmə ödəniş Çexiya hesabı AZN'] + example_df['Daşıyıcıya köçürmə ödəniş Türkiyə hesabı AZN'] + example_df['Daşıyıcıya köçürmə ödəniş Azərbaycanhesabı AZN'])

                dasiyicilara_qaliq_borc_eur = example_df['Daşıyıcıya qalıq borc EUR'].sum()
                dasiyicilara_qaliq_borc_usd = example_df['Daşıyıcıya qalıq borc USD'].sum()
                dasiyicilara_qaliq_borc_azn = example_df['Daşıyıcıya qalıq borc AZN'].sum()

                example_html = example_df.to_html()
                session.commit()

                # print('dasiyicilara_qaliq_borc_eur: ', dasiyicilara_qaliq_borc_eur)
                # print('dasiyicilara_qaliq_borc_usd: ', dasiyicilara_qaliq_borc_usd)
                # print('dasiyicilara_qaliq_borc_azn: ', dasiyicilara_qaliq_borc_azn)

                # print("yukalanlarin_bize_borcu_eur: ", yukalanlarin_bize_borcu_eur)
                # print("yukalanlarin_bize_borcu_usd: ", yukalanlarin_bize_borcu_usd)
                # print("yukalanlarin_bize_borcu_azn: ", yukalanlarin_bize_borcu_azn)

                response = JsonResponse({
                                        'example_table': example_html,
                                        'table_name': table_name,
                                        'dasiyiciya_nagd_odenis_eur': dasiyiciya_nagd_odenis_eur,
                                        'dasiyiciya_nagd_odenis_usd': dasiyiciya_nagd_odenis_usd,
                                        'dasiyiciya_nagd_odenis_azn': dasiyiciya_nagd_odenis_azn,

                                        'dasiyiciya_kocurme_odenis_chexiya_eur': dasiyiciya_kocurme_odenis_chexiya_eur,
                                        'dasiyiciya_kocurme_odenis_chexiya_usd': dasiyiciya_kocurme_odenis_chexiya_usd,
                                        'dasiyiciya_kocurme_odenis_chexiya_azn': dasiyiciya_kocurme_odenis_chexiya_azn,

                                        'dasiyiciya_kocurme_odenis_turkiye_eur': dasiyiciya_kocurme_odenis_turkiye_eur,
                                        'dasiyiciya_kocurme_odenis_turkiye_usd': dasiyiciya_kocurme_odenis_turkiye_usd,
                                        'dasiyiciya_kocurme_odenis_turkiye_azn': dasiyiciya_kocurme_odenis_turkiye_azn,

                                        'dasiyiciya_kocurme_odenis_azerbaycan_eur': dasiyiciya_kocurme_odenis_azerbaycan_eur,
                                        'dasiyiciya_kocurme_odenis_azerbaycan_usd': dasiyiciya_kocurme_odenis_azerbaycan_usd,
                                        'dasiyiciya_kocurme_odenis_azerbaycan_azn': dasiyiciya_kocurme_odenis_azerbaycan_azn,

                                        'odenis_chexiya_daxil_olan_eur': odenis_chexiya_daxil_olan_eur,
                                        'odenis_chexiya_daxil_olan_usd': odenis_chexiya_daxil_olan_usd,
                                        'odenis_chexiya_daxil_olan_azn': odenis_chexiya_daxil_olan_azn,

                                        'invoice_mebleq_eur': invoice_mebleq_eur,
                                        'invoice_mebleq_usd': invoice_mebleq_usd,
                                        'invoice_mebleq_azn': invoice_mebleq_azn,

                                        'diger_xercler_eur': diger_xercler_eur,
                                        'diger_xercler_usd': diger_xercler_usd,
                                        'diger_xercler_azn': diger_xercler_azn,

                                        'net_mebleg_eur': net_mebleg_eur,
                                        'net_mebleg_usd': net_mebleg_usd,
                                        'net_mebleg_azn': net_mebleg_azn,

                                        'yukalanlarin_bize_borcu_eur': float(yukalanlarin_bize_borcu_eur),
                                        'yukalanlarin_bize_borcu_azn': float(yukalanlarin_bize_borcu_azn),
                                        'yukalanlarin_bize_borcu_usd': float(yukalanlarin_bize_borcu_usd),

                                        'dasiyicilara_qaliq_borc_eur': float(dasiyicilara_qaliq_borc_eur),
                                        'dasiyicilara_qaliq_borc_usd': float(dasiyicilara_qaliq_borc_usd),
                                        'dasiyicilara_qaliq_borc_azn': float(dasiyicilara_qaliq_borc_azn),

                                        })
                # response.status_code=501
                add_get_params(response)
                return response

            else:

                example_html = example_df.to_html()
                session.commit()
                response = JsonResponse({
                                        'example_table': example_html,
                                        'table_name': table_name,

                                        })
                # response.status_code=501
                add_get_params(response)
                return response

    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: "+str(e), my_traceback, 501)


@csrf_exempt
def delete_row_from_table_with_id(request):
    # Build th"e POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")

    try:
        if token_verification(request)['is_admin'] != True:
            return error_response("Token verification error!", "Please sign in again!", 507)

        user_region = request.POST.get('user_region')
        selected_region = request.POST.get('selected_region')

        if(selected_region == 'System'):
            data_table = System_table

        elif(selected_region == 'Europe'):
            data_table = System_europe

        elif(selected_region == 'Avia'):
            data_table = System_avia

        elif(selected_region == 'Russia'):
            data_table = System_russia

        elif(selected_region == 'Container'):
            data_table = System_container

        row_id = request.POST.get('row_id')
        with Session(engine) as session:
            deleted_objects = data_table.__table__.delete().where(
                data_table.id.in_([row_id]))
            session.execute(deleted_objects)
            session.commit()

        response = JsonResponse({'Answer': 'Success', })
        # response.status_code=501
        add_get_params(response)
        return response

    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: "+str(e), my_traceback, 501)


@csrf_exempt
def delete_row_from_table(request):
    # Build th"e POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")

    try:
        if token_verification(request)['is_admin'] != True:
            return error_response("Token verification error!", "Please sign in again!", 507)

        user_region = request.POST.get('user_region')

        selected_region = request.POST.get('selected_region')

        if(selected_region == 'System'):
            data_table = System_table

        elif(selected_region == 'Europe'):
            data_table = System_europe

        elif(selected_region == 'Avia'):
            data_table = System_avia

        elif(selected_region == 'Russia'):
            data_table = System_russia

        elif(selected_region == 'Container'):
            data_table = System_container

        status_n = request.POST.get('status_n')
        with Session(engine) as session:
            deleted_objects = data_table.__table__.delete().where(
                data_table.Status_N.in_([status_n]))
            session.execute(deleted_objects)
            session.commit()

        response = JsonResponse({'Answer': 'Success', })
        # response.status_code=501
        add_get_params(response)
        return response

    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: "+str(e), my_traceback, 501)


@csrf_exempt
def edit_row_at_table(request):
    # Build th"e POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")

    try:
        if token_verification(request)['is_manager'] != True:
            return error_response("Token verification error!", "Please sign in again!", 505)

        user_region = request.POST.get('user_region')

        selected_region = request.POST.get('selected_region')
        data_table = ''

        if token_verification(request)['is_admin_minus'] != True:

            if(user_region == 'All'):
                data_table = System_table

            elif(user_region == 'Europe'):
                data_table = System_europe

            elif(user_region == 'Avia'):
                data_table = System_avia

            elif(user_region == 'Russia'):
                data_table = System_russia

            elif(user_region == 'Container'):
                data_table = System_container

        else:
            if(selected_region == 'System'):
                data_table = System_table

            elif(selected_region == 'Europe'):
                data_table = System_europe

            elif(selected_region == 'Avia'):
                data_table = System_avia

            elif(selected_region == 'Russia'):
                data_table = System_russia

            elif(selected_region == 'Container'):
                data_table = System_container

        status_n = request.POST.get('status_n')

        dict = json.loads(request.POST.get('json_text'))

        with Session(engine) as session:

            deleted_objects = data_table.__table__.delete().where(
                data_table.Status_N.in_([status_n]))
            session.execute(deleted_objects)
            session.commit()

        with Session(engine) as session:
            new_row = data_table(**dict)
            session.add(new_row)
            session.commit()

        response = JsonResponse({'Answerr': 'Success', })
        # response.status_code=501
        add_get_params(response)
        return response

    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: "+str(e), my_traceback, 501)


@csrf_exempt
def add_row_to_table(request):
    # Build th"e POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")

    try:
        if token_verification(request)['is_user'] != True:
            return error_response("Token verification error!", "Please sign in again!", 505)

        status_n = request.POST.get('status_n')

        dict = json.loads(request.POST.get('json_text'))
        user_region = request.POST.get('user_region')

        selected_region = request.POST.get('selected_region')
        if token_verification(request)['is_admin_minus'] != True:

            if(user_region == 'All'):
                data_table = System_table

            elif(user_region == 'Europe'):
                data_table = System_europe

            elif(user_region == 'Avia'):
                data_table = System_avia

            elif(user_region == 'Russia'):
                data_table = System_russia

            elif(user_region == 'Container'):
                data_table = System_container

        else:
            if(selected_region == 'System'):
                data_table = System_table

            elif(selected_region == 'Europe'):
                data_table = System_europe

            elif(selected_region == 'Avia'):
                data_table = System_avia

            elif(selected_region == 'Russia'):
                data_table = System_russia

            elif(selected_region == 'Container'):
                data_table = System_container

        with Session(engine) as session:
            new_row = data_table(**dict)
            session.add(new_row)
            session.commit()

        response = JsonResponse({'Answerr': 'Success', })
        # response.status_code=501
        add_get_params(response)
        return response

    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: " + str(e), my_traceback, 501)


@csrf_exempt
def download_csv(request):
    if token_verification(request)['is_user'] != True:
        return error_response("Token verification error!", "Please sign in again!", 505)

    '''
    downloading material searching table result 
    which user see in the material_searching.html
    '''

    user_region = request.POST.get('user_region')

    selected_region = request.POST.get('selected_region')
    # print("Selected_region: ", selected_region)
    # print("user_region: ", user_region)
    # print("is_admin_minus: ", token_verification(request)['is_admin_minus'])

    if token_verification(request)['is_admin_minus'] != True:

        user_select_region = user_region

        if(user_region == 'All'):
            data_table = System_table
            head_columns = head_columns_system

        elif(user_region == 'Europe'):
            data_table = System_europe
            head_columns = head_columns_europe

        elif(user_region == 'Avia'):
            data_table = System_avia
            head_columns = head_columns_avia

        elif(user_region == 'Russia'):
            data_table = System_russia
            head_columns = head_columns_russia

        elif(user_region == 'Container'):
            data_table = System_container
            head_columns = head_columns_container

    else:

        user_select_region = selected_region

        if(selected_region == 'System'):
            data_table = System_table
            head_columns = head_columns_system

        elif(selected_region == 'Europe'):
            data_table = System_europe
            head_columns = head_columns_europe

        elif(selected_region == 'Avia'):
            data_table = System_avia
            head_columns = head_columns_avia

        elif(selected_region == 'Russia'):
            data_table = System_russia
            head_columns = head_columns_russia

        elif(selected_region == 'Container'):
            data_table = System_container
            head_columns = head_columns_container

    if token_verification(request)['is_manager_minus'] == True:

        if(user_region == 'All'):
            head_columns = head_columns_system_2

        elif(user_region == 'Europe'):
            head_columns = head_columns_europe_2

        elif(user_region == 'Avia'):
            head_columns = head_columns_avia_2

        elif(user_region == 'Russia'):
            head_columns = head_columns_russia_2

        elif(user_region == 'Container'):
            head_columns = head_columns_container_2

    with Session(engine) as session:
        example_table = session.query(data_table)
        example_table_serialized = single_table_serializer(example_table)

        df = pd.DataFrame(example_table_serialized, columns=head_columns)

        session.commit()

    try:
        df.drop('level_0', axis=1, inplace=True)
    except Exception as e:
        pass

    # * change dataframe to csv file and return whith response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=Sistem_{user_select_region}_table_{datetime.now().strftime("%Y.%m.%d_%H.%M")}.csv'
    response.write(u'\ufeff'.encode('utf8'))

    # with other applicable parameters
    df.to_csv(path_or_buf=response, index=False)
    return response
