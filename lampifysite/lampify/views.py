from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

import json
import paho.mqtt.publish

#spotify import 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Create your views here.

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id="7fb0b30be5194943ac0e2bc89463f963", client_secret="6adabaf3e12044e495f522bab6d79d27")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            song = form.cleaned_data['songs']
            songSearched = sp.search(song, limit = 1, type = 'track')
            uri = songSearched['tracks']['items']
            uri = uri[len(uri) - 1]
            uri = uri['uri']
            data = {}
            data['track'] = uri
            paho.mqtt.publish.single(
                'devices/b827eb1e9033/lamp/song',
                json.dumps(data),
                qos=2,
                hostname="localhost",
                port=50001,
            )
            print(uri)
    
    form = ContactForm()
    return render(request, 'forms.html', {'form': form})