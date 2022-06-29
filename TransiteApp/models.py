from django.db import models
from sqlalchemy.ext.automap import automap_base
from TransiteAPI.settings import engine
# Create your models here.
Base = automap_base()
Base.prepare(engine.engine, reflect=True)

USERS = Base.classes.transite_users

Example_table = Base.classes.example_table
System_table = Base.classes.system_table

System_europe = Base.classes.system_europe
System_russia = Base.classes.system_russia
System_avia = Base.classes.system_avia
System_container = Base.classes.system_container