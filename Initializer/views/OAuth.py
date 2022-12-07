import os

import requests
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow

from Initializer.models import Credentials


def oauth_request(request):
    c = Credentials.objects.all().last()
    if c:
        return redirect('init_next')

    flow = Flow.from_client_secrets_file(
        'auth.json',
        scopes=['https://www.googleapis.com/auth/cloud-platform'],
        state='12345678910')

    flow.redirect_uri = request.build_absolute_uri('/init/oauth/response')

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

    flow.redirect_uri = request.build_absolute_uri('/init/oauth/response')
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

    return redirect('init_next')
