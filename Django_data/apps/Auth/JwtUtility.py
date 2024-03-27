import jwt
from decouple import config

def create_jwt(_user, _type="access"):
    payload = {'id': _user.id,
               'username': _user.username,
               'email': _user.email}
    secret_key = config('DJANGO_SECRET_KEY')
    algorithm = config('HASH')
    if _type == "access":
        time_now = datetime.datetime.utcnow()
        payload = {"exp": time_now + datetime.timedelta(minutes=30),
                   "iss": config('NAME')}
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

