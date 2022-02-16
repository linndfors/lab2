import json
import folium
from ast import arg
from geopy.geocoders import Nominatim, ArcGIS
from functools import lru_cache
from geopy import distance

def main():

    arcgis = ArcGIS(timeout=10)
    nominatim = Nominatim(timeout=10, user_agent="justme")

    def take_data():
        '''
        Thist function open json file, read it and save data
        '''
        names = []
        locations = []
        new_pair = []
        with open('twiter2.json') as my_file:
            data = json.load(my_file)
            for i_var in range(len(data.get('users'))):
                user_info = data.get('users')[i_var]
                for elem in user_info.keys():
                    if elem == 'screen_name':
                        names.append(user_info[elem])
                    if elem == 'location':
                        locations.append(user_info[elem])
                about_user = list(zip(names, locations))
            for pair in about_user:
                cords = geocode(pair[1])
                if cords != None:
                    new_pair.append((pair[0], cords))
            return new_pair


    geocoders = [arcgis, nominatim]

    @lru_cache(maxsize=None)
    def geocode(address):
        '''
        Return coordinates, where address take place
        >>> print(geocode('Aeroporto, Lisbon, Portugal'))
        (38.88560396835856, -9.038366756931474)
        '''
        i = 0
        try:
            location = geocoders[i].geocode(address)
            if location != None:
                return location.latitude, location.longitude
            i += 1
            location = geocoders[i].geocode(address)
            if location != None:
                return location.latitude, location.longitude
        except:
            return None


    def web_work(data):
        '''
        Make layers and markers for web-map
        '''
        map = folium.Map(location=[55.2744,13.7751])
        fg_hc = folium.FeatureGroup(name="My friends")

        for pair in data:
            fg_hc.add_child(folium.Marker(location=[pair[1][0], pair[1][1]],
                popup = f"username: {pair[0]}",
                icon=folium.Icon(color = 'pink')))

        map.add_child(fg_hc)
        map.add_child(folium.LayerControl())
        map.save('templates/Friends_locations.html')

    res = take_data()
    map_friend = web_work(res)

if __name__ == '__main__':
    main()