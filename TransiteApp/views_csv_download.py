from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
from TransiteAPI.settings import engine, BASE_DIR
import pandas as pd
from sqlalchemy.orm import Session
from .models import Example_table
from .custom_logic import add_get_params, single_table_serializer
 

