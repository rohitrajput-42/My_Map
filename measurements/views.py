from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
import folium

def calculate_distance_view(request):

    distance = None
    destination = None
    location = None
    obj = get_object_or_404(Measurement, id = 72)
    form = MeasurementModelForm(request.POST or None)
    geoloacator = Nominatim(user_agent = 'measurements')

#    USE WHEN GOING LIVE
#    ip_ = get_ip_address(request)
#    print(ip_)

    ip = '203.199.104.251'
    country, city, lat, lon = get_geo(ip)
    #print('Location Country : ', country)
    #print('Location City : ', city)
    #print('Location Latitude & Logitude : ', lat, lon)
    location = geoloacator.geocode(city)
    #print("Your current location is: ", location)

    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    #MAP
    m = folium.Map(width = 800, height = 500, location = get_center_coordinates(l_lat, l_lon), get_zoom = 7)
    
    folium.Marker([l_lat, l_lon], tooltip='Your Location.', popup=location, icon = folium.Icon(color = 'red')).add_to(m)
    #

    mains = request.user

    if form.is_valid():
        instance = form.save(commit = False)
        destination_ = form.cleaned_data.get('destination')
        destination = geoloacator.geocode(destination_)
        
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)

        distance = round(geodesic(pointA, pointB).km, 2)

        instance.location = location
        instance.distance = distance
        instance.created_by = mains.username

        m = folium.Map(width = 800, height = 500, location = get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start = get_zoom(distance))

        folium.Marker([l_lat, l_lon], tooltip='Your Location(Tap for more info).', popup=location, icon = folium.Icon(color = 'red')).add_to(m)

        folium.Marker([d_lat, d_lon], tooltip='Your Destination(Tap for more info).', popup=destination, icon = folium.Icon(color = 'purple', icon = 'cloud')).add_to(m)

        line = folium.PolyLine(locations = [pointA, pointB], weight = 2 , color = 'blue')
        m.add_child(line)

        instance.save()

    m = m._repr_html_()

    context = {
        'distance': distance,
        'destination': destination,
        'location': location,
        'form': form,
        'map': m
    }

    return render(request, 'index.html', context)