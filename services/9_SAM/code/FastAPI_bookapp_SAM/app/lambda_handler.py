from main import app
from mangum import Mangum


# Another way for using mangum
# can also create a handler variable in main.py like:
# handler = Mangum(app)
def handler(event, context):
    mangum_handler = Mangum(app=app, lifespan="off")
    return mangum_handler(event=event, context=context)
