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
            response = JsonResponse({'error_text':str(e),
                                        'error_text_2':my_traceback
                                        })
            response.status_code = 505
        
            add_get_params(response)
            return response
    else:
        response = JsonResponse({'Answer': "This promerty only for POST method.", })
        response.status_code=501
        add_get_params(response)
        return response
    
    


@csrf_exempt
def get_table(request):
    # Build the POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")
   
    try:
        if token_verification(request)['is_user'] != True: 
            return error_response("Token verification error!","Please sign in again!", 505)
                    
        
        
        user_region = request.POST.get('user_region')
        
        data_table = ""
        head_columns = ""
        
        selected_region = request.POST.get('selected_region')
        if token_verification(request)['is_admin_minus'] != True: 
        
            if(user_region == 'All'): 
                data_table = System_table
                head_columns= head_columns_system
                
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
                head_columns= head_columns_system
                
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
           
           
            example_df = pd.DataFrame(example_table_serialized,columns= head_columns)
        
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
            
            
                diger_xercler_eur = example_df['Digər xərclər EUR'].sum()
                diger_xercler_usd = example_df['Digər xərclər USD'].sum()
                diger_xercler_azn = example_df['Digər xərclər AZN'].sum()
            
                # Net mebleg: invoice - (chexx + dasiyici + diger)
        
                net_mebleg_eur = invoice_mebleq_eur - (odenis_chexiya_daxil_olan_eur + dasiyiciya_nagd_odenis_eur + diger_xercler_eur)
                net_mebleg_usd = invoice_mebleq_usd - (odenis_chexiya_daxil_olan_usd + dasiyiciya_nagd_odenis_usd + diger_xercler_usd)
                net_mebleg_azn = invoice_mebleq_azn - (odenis_chexiya_daxil_olan_azn + dasiyiciya_nagd_odenis_azn + diger_xercler_azn)
            
        
            
                
                example_html = example_df.to_html()
                session.commit()

            
                response = JsonResponse({'example_table': example_html, 
                                        'table_name': table_name, 
                                        'dasiyiciya_nagd_odenis_eur': dasiyiciya_nagd_odenis_eur,
                                        'dasiyiciya_nagd_odenis_usd': dasiyiciya_nagd_odenis_usd,
                                        'dasiyiciya_nagd_odenis_azn': dasiyiciya_nagd_odenis_azn,
                                        
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
        return error_response("TryCatch: "+str(e),my_traceback,501)






    
@csrf_exempt
def delete_row_from_table_with_id(request):
    # Build th"e POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")
   
    try:
        if token_verification(request)['is_admin'] != True: 
            return error_response("Token verification error!","Please sign in again!", 507)
      
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
            deleted_objects = data_table.__table__.delete().where(data_table.id.in_([row_id]))
            session.execute(deleted_objects)
            session.commit()
    
        
        response = JsonResponse({'Answer': 'Success', })
        # response.status_code=501
        add_get_params(response)
        return response
    
    
    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: "+str(e),my_traceback,501)


    
@csrf_exempt
def delete_row_from_table(request):
    # Build th"e POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")
   
    try:
        if token_verification(request)['is_admin'] != True: 
            return error_response("Token verification error!","Please sign in again!", 507)
                 
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
            deleted_objects = data_table.__table__.delete().where(data_table.Status_N.in_([status_n]))
            session.execute(deleted_objects)
            session.commit()
    
        
        response = JsonResponse({'Answer': 'Success', })
        # response.status_code=501
        add_get_params(response)
        return response
    
    
    except Exception as e:
        my_traceback = traceback.format_exc()
        print("my_traceback", my_traceback)
        return error_response("TryCatch: "+str(e),my_traceback,501)





@csrf_exempt
def edit_row_at_table(request):
    # Build th"e POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")
   
    try:
        if token_verification(request)['is_manager'] != True: 
            return error_response("Token verification error!","Please sign in again!", 505)
                    
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
            
            deleted_objects = data_table.__table__.delete().where(data_table.Status_N.in_([status_n]))
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
        return error_response("TryCatch: "+str(e),my_traceback,501)




@csrf_exempt
def add_row_to_table(request):
    # Build th"e POST parameters
    if request.method != 'POST':
        return error_response("This function is working only with POST method.")
   
    try:
        if token_verification(request)['is_user'] != True: 
            return error_response("Token verification error!","Please sign in again!", 505)
                    
        
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
        return error_response("TryCatch: "+str(e),my_traceback,501)


@csrf_exempt
def download_csv(request):
    if token_verification(request)['is_user'] != True: 
        return error_response("Token verification error!","Please sign in again!", 505)
    
    
    '''
    downloading material searching table result 
    which user see in the material_searching.html
    '''

    user_region = request.POST.get('user_region')

    selected_region = request.POST.get('selected_region')
    if token_verification(request)['is_admin_minus'] != True: 
    
        if(user_region == 'All'): 
            data_table = System_table
            head_columns= head_columns_system
            
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
            head_columns= head_columns_system
            
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
            head_columns= head_columns_system_2
            
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
        
        df = pd.DataFrame(example_table_serialized,columns = head_columns)
        
                
        session.commit()
        
    try:
        df.drop('level_0', axis=1, inplace=True)
    except Exception as e:
        pass
    
    # * change dataframe to csv file and return whith response 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=Sistem_{user_region}_table_{datetime.now().strftime("%Y.%m.%d_%H.%M")}.csv' 
    response.write(u'\ufeff'.encode('utf8'))
    
    
    df.to_csv(path_or_buf=response, index= False)  # with other applicable parameters
    return response