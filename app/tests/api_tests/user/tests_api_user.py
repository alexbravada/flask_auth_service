import os

import random
import requests
from mimesis import Person

API_BRANCH = 'user'
host = os.environ.get('TEST_URL')


# data = api_auth.get_routes().get(API_BRANCH)


def test_signup_valid_data():
    mimerand = Person()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = 'http://127.0.0.1:5000/api/v1/auth/user/signup'
    data = {'email': mimerand.email(unique=True), 'password': str(random.randint(0, 65536))}
    response = requests.post(url=url,
                             data=data,
                             headers=headers
                             )
    print(response.headers)
    print(response)
    assert response.status_code == 201
