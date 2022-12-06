import os

import requests
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow

from Initializer.models import Credentials


def oauth_request(request):
    flow = Flow.from_client_secrets_file(
        'auth.json',
        scopes=['https://www.googleapis.com/auth/cloud-platform'],
        state='12345678910')

    flow.redirect_uri = request.get_full_path() + '/response'
    print(flow.redirect_uri)

    url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    request.session['state'] = state
    return redirect(url)


def oauth_response(request):
    state = request.session['state']
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    flow = Flow.from_client_secrets_file(
        'auth.json',
        scopes=['https://www.googleapis.com/auth/cloud-platform'],
        state='12345678910')

    flow.redirect_uri = 'http://127.0.0.1:8000/init/oauth/response'
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    c = Credentials(token=credentials.token,
                    refresh_token=credentials.refresh_token,
                    token_uri=credentials.token_uri,
                    client_id=credentials.client_id,
                    client_secret=credentials.client_id,
                    scopes=credentials.scopes)
    c.save()
    request.session['credentials'] = c.to_dict()

    r = requests.get('https://compute.googleapis.com/compute/v1/projects/yu-21913672/zones/asia-northeast3-a/instances',
                     headers={'Authorization': 'Bearer ' + c.token})
    print(r.text)
    return redirect('init')
