from dronecoria.settings import API_IP
import requests
from gsoc2019.models import *
from gsoc2019.model import *
import time
import bs4
import pandas as pd


DRONE_PATH_TEXT = """
<![CDATA[
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

  </head>
  <body>
  <img src="http://dronecoria.org/wp-content/uploads/2018/04/DRONECORIA-logo-web-1.png" class="img-thumbnail"></img>
  <div class="p-lg-5" align="center">
      <h3>
          <small>Drone path</small>
      </h3>
  </div>
<div class="p-lg-5" align="center">
    This is the path that the drone will follows to take the photos of the burnt forest.
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
]]>
"""

STOP_DRONE = False

def set_stop_drone(value):
    global STOP_DRONE
    STOP_DRONE = value

def clean_kml():
    global STOP_DRONE
    url = "http://%s/kml/manage/clean" % API_IP
    response = requests.get(url)
    STOP_DRONE = True
    print(" >>>>>>>>>>>>>   Stop drone %d <<<<<<<<<<<<<<<<<" %STOP_DRONE )
    print("> Answer received by LiquidGalaxy [%s]." % response.text)
    stop_orbit()
    fly_to(0,42, 20000000)

def check_stop_drone():
    print(" >>>>>>>>>>>>>   Stop drone %d <<<<<<<<<<<<<<<<<" %STOP_DRONE )

def obtain_coordinates_kml(kml_file_name):
    with open(kml_file_name, 'r') as kml_file:
        page = kml_file.read()
        bs = bs4.BeautifulSoup(page, "lxml")
        coordinates = bs.document.findAll("coordinates")[0].text.split()
        middle = coordinates[round(len(coordinates)/2)].split(',')[:2]
    return middle




def send_kml(kml_file, demo=False):
    url = "http://%s/kml/builder/concatenate/" % API_IP
    file_name = kml_file.split('/')[-1]
    print("> Send kml of drone path: [%s] " % file_name)
    lon, lat = obtain_coordinates_kml(kml_file)
    if not demo:
        orbit(lat, lon, 'sending_kml', range = 600)
    time.sleep(3)
    multipart_form_data = {
        'kml': (file_name, open(kml_file, 'r')),
    }
    if not demo:
        send_placemark(lon, lat, '', 'kml_bubble', 0, '', 2, DRONE_PATH_TEXT)
        show_bubble('kml_bubble')
    response = requests.post(url, files=multipart_form_data)

    print("> Answer received by LiquidGalaxy [%s]. "% response.status_code)

def exit_orbit():
    url = "http://%s/kml/manage/stoptour" % API_IP


def send_image(image, fCorner, sCorner, tCorner, ftCorner, do_fly_to=True):
    url = "http://%s/kml/builder/addPhoto" % API_IP
    print("> Send image kml: [%s] " % image)
    image_file = open(image, 'rb')
    print(image)
    image_name = image.split('/')[-1]
    image_id = image.split('/')[-1].replace(".png", "")
    files = {'img': (image_name, image_file)}
    multipart_form_data = {
        'id': image_id,
        'name': image_id,
        'fCorner': fCorner,
        'sCorner': sCorner,
        'tCorner': tCorner,
        'ftCorner': ftCorner
    }
    print(multipart_form_data)
    if do_fly_to:
        lon = (float(ftCorner.split(',')[0]) + float(sCorner.split(',')[0])) / 2
        lat = (float(ftCorner.split(',')[1]) + float(sCorner.split(',')[1])) / 2
        fly_to(lon, lat, 700)
    response = requests.post(url, data=multipart_form_data, files=files)
    print("> Answer received by LiquidGalaxy [%s]. "% response.status_code)


def get_area(image):
    image_name = str(image.img.name.replace("upload_images", "images_located"))

    df_images_located = pd.read_csv("static/metadata_images_located.csv")
    df_regions = pd.read_csv("static/regions.csv")
    region = df_images_located[df_images_located['id_green'] == image_name]['id_region'].values[0]
    area = df_regions[df_regions['region_id'] == region]['area'].values[0]
    return area



def generate_bubble(lon, lat, area):
    return """
<![CDATA[
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

      </head>
      <body>
      <img src="http://dronecoria.org/wp-content/uploads/2018/04/DRONECORIA-logo-web-1.png" class="img-thumbnail"></img>
      <div class="p-lg-5" align="center">
          <h3>
              <small>Information about burnt region</small>
          </h3>
      </div>
    <div class="p-lg-5" align="center">
        <table class="table">
            <tbody>
                <thead class="thead-dark">
                <tr>
                  <th>Longitude</th>
                    <td>%s</td>
                </tr>
                <tr>
                  <th>Latitude</th>
                    <td>%s</td>
                </tr>
              <tr>
                  <th>Area in Ha</th>
                  	<td>%.3f</td>
                </tr>
            </tbody>
        </table>
    </div>

    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
]]>
    """ % ((lat, lon, area))


def show_bubble(id):
    url = "http://%s/kml/manage/balloon/%s/1" % ((API_IP, id))
    response = requests.get(url)
    print("> Answer received by LiquidGalaxy [%s]." % response.text)


def send_bubble(image_name, lon, lat, area, do_fly_to=True, do_orbit=True):
    url = "http://%s/kml/builder/addplacemark" % API_IP
    print("> Sending bubble ")
    id = image_name.split('/')[-1].replace('.png',''),
    description = generate_bubble(lat, lon, area)
    if do_fly_to:
        fly_to(float(lon), float(lat), 2000)
    send_placemark(lon,lat, id, id, 0, 'http://%s/images/fire_logo.png' % API_IP, 2, description)
    if do_orbit:
        orbit(lat, lon, str(id) + "_orbit")
    show_bubble(image_name.split('/')[-1].replace('.png',''))


def send_placemark(lon, lat, name, id='a', range=0, icon='', scale=3, description=''):
    url = "http://%s/kml/builder/addplacemark" % API_IP
    print("> Sending placemark ")
    files = {'img': (None, '')}
    multipart_form_data = {
        'id': id,
        'name': '',
        'longitude': lon,
        'latitude': lat,
        'range': range ,
        'scale': scale,
        'icon': icon,
        'description': description
    }
    response = requests.post(url, data=multipart_form_data, files = files)
    print(" > Answer received by LiquidGalaxy [%s]." % response.text)


def delete_placemark(id, tag):
    url = "http://%s/kml/builder/deleteTag/%s/%s" % ((API_IP, tag, id))
    print(url)
    response = requests.delete(url)
    print("> Answer received by LiquidGalaxy [%s]." % response.text)


def stop_orbit():
    requests.get("http://%s/kml/manage/stoptour" % (API_IP))



def orbit(lon, lat, id, range=500):
    url = "http://%s/kml/builder/Orbit" % (API_IP)
    print("> Starting orbit")
    files = {'img': (None, '')}
    multipart_form_data = {
        'id': id,
        'name': id,
        'latitude': lon,
        'longitude': lat,
        'range': 500,
        'description':''
    }
    response = requests.post(url, data=multipart_form_data, files = files)
    print("> Answer received by LiquidGalaxy [%s]." % response.text)
    time.sleep(3)
    requests.get("http://%s/kml/manage/initTour/%s" % ((API_IP, id)))

def fly_to(lon, lat, range=2000):
    url = "http://%s/kml/flyto/%f/%f/%d" % ((API_IP, lon, lat, range))
    response = requests.get(url)
    print("> Answer received by LiquidGalaxy [%s]." % response.text)


def send_gallery_bubble(images):
    for image in images:
        lon = (float(image.tCorner.split(',')[0]) + float(image.fCorner.split(',')[0]) )/ 2
        lat =  float(image.tCorner.split(',')[1])* 0.6 + float(image.fCorner.split(',')[1])*0.4
        area = get_area(image)
        send_bubble(image.img.name, lon, lat, area)

def detele_gallery_buuble(images):
    for image in images:
        image_name = image.img.name
        id = image_name.split('/')[-1].replace('.png','')
        delete_placemark(id, 'Placemark')


def send_gallery(images):
    for image in images:
        send_image(image.img.name, image.fCorner, image.sCorner, image.tCorner, image.ftCorner)

def delete_image(images):
    for image in images:
        image_id = image.img.name.split('/')[-1].replace(".png", "")
        delete_placemark(image_id, 'GroundOverlay')

def detect_region(images):
    for image in images:
        try:
            send_image(image.img.name.replace(".png", "_delimitted.png"), image.fCorner, image.sCorner, image.tCorner, image.ftCorner)
        except FileNotFoundError:
            draw_burnt_region(image.img.name)
            send_image(image.img.name.replace(".png", "_delimitted.png"), image.fCorner, image.sCorner, image.tCorner, image.ftCorner)
    print("> Sent image <")


def draw_line(path, name, id):
    url = "http://%s/kml/builder/drawpath" % API_IP
    print(" > Drawing path")
    files = {'img': (None, '')}
    print(id)
    multipart_form_data = {
        'id': id,
        'name': name,
        'path': path
    }
    response = requests.post(url, data=multipart_form_data, files = files)
    print(" > Answer received by LiquidGalaxy [%s]." % response.text)

def stop_reforestation(images):
    global STOP_DRONE
    for image in images:
        path_id = image.img.name.replace(".png", "_path").split("/")[-1]
        delete_placemark(path_id, 'Placemark')
        delete_placemark(path_id, 'Placemark')
        STOP_DRONE = True
        delete_placemark('drone', 'Placemark')

def update_placemark(id, lat, lon, range=0):
    url = "http://%s/kml/builder/editcoodplacemark" % API_IP
    print(" > Updating placemark")
    files = {'img': (None, '')}
    print(id)
    multipart_form_data = {
        'id': id,
        'latitude': lat,
        'longitude': lon,
        'range': range,

    }
    response = requests.put(url, data=multipart_form_data, files = files)



def fly_drone(path):
    path_splitted = path.split()
    global STOP_DRONE
    STOP_DRONE = False
    lon_0 = float(path_splitted[0].split(',')[0])
    lat_0 = float(path_splitted[0].split(',')[1])
    send_placemark(lon_0, lat_0, '', 'drone', 35, 'http://%s/images/icon.png' % API_IP, 2)
    for i in range(1, len(path.split())):
        lon_0 = float(path_splitted[i-1].split(',')[0])
        lat_0 = float(path_splitted[i-1].split(',')[1])

        lon_i = float(path_splitted[i].split(',')[0])
        lat_i = float(path_splitted[i].split(',')[1])
        alpha_lon = (lon_i - lon_0)/3
        alpha_lat = (lat_i - lat_0)/3
        for k in range(0, 3):
            lon_0 += alpha_lon
            lat_0 += alpha_lat
            id = "%d%d" % ((i,k))
            #send_placemark(lon_0, lat_0, '', 'drone', 0, 'http://%s/images/icon.png' % API_IP, 2)
            update_placemark('drone', lat_0, lon_0, 15)
            print(id)
            time.sleep(3)
            #delete_placemark('drone', 'Placemark')
            print(" >>>>>>>>>>>>>   Stop drone %d <<<<<<<<<<<<<<<<<" %STOP_DRONE )
            if(STOP_DRONE):
                break;
        if(STOP_DRONE):
            break;
    delete_placemark('drone', 'Placemark')

def get_path(contour, deltaLon, deltaLat):
    real_path = [contour[0]]
    for i  in range(0, len(contour)):
        pixel = contour[i]
        if abs(pixel[0]-real_path[-1][0])  > abs(38*deltaLon) and abs(pixel[1] - real_path[-1][1]) > 1*abs(deltaLat):
            real_path.append(pixel)
            real_path.append((pixel[0], pixel[1]+deltaLat*5))
    return [real_path[i] for i in range(0, len(real_path), 31)]


def fly_to_center_forest(corners):
    ftCorners = corners['ftCorner']
    sCorners  = corners['sCorner']
    lon = (corners['ftCorner'][0] + corners['sCorner'][0]) /2
    lat = (corners['ftCorner'][1] + corners['sCorner'][1]) /2
    fly_to(lon,lat,range=2000)


def reforestation(images):
    for image in images:
        file_delimitted = image.img.name.replace(".png", "_delimitted.png")
        try:
            array_delimitted = np.array(PIL.Image.open(file_delimitted))
            geolocated_contour, deltaLon, deltaLat = geo_locate_contour(array_delimitted, image.ftCorner, image.sCorner)
            print(geolocated_contour)
            path = get_path(geolocated_contour, deltaLon, deltaLat)
            fly_path = " ".join([ "".join("%f,%f,50" % ((path[i][0], path[i][1]))) for i in range(0, len(path)) ])
            print("<> THEEEE FLYY PATHH ISS <> %s <>" % fly_path)
            path_id = image.img.name.replace(".png", "_path").split("/")[-1]
            draw_line(fly_path, path_id, path_id)
            fly_drone(fly_path)
        except FileNotFoundError:
            print("Detect first")
