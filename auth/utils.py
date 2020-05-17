import random
import string
import time

import jwt

chars = string.ascii_letters + string.digits
secret = "".join([random.choice(chars) for x in range(100)])
start = time.time()
encoded_jwt = jwt.encode({'some': 'payload', "another": "value"}, secret, algorithm='HS256')
print(jwt.decode(encoded_jwt, secret, algorithms=['HS256']))
print(time.time() - start)
