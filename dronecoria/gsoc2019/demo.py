from gsoc2019.aux_functions import *
from gsoc2019.aux_functions import STOP_DRONE
import time
from PIL import Image as pilImage
import numpy as np


DEMO = True


FIRST_KML_PATH = """0.7359388775975861,42.05336835526828,60 0.7458632392696907,42.05360200895878,60 0.7457656913158561,42.05315221244696,60 0.7359955363059112,42.05299603244153,60 0.7360777825489873,42.0527272450558,60 0.7456276400593498,42.0528335605366,60 0.7455045482934097,42.05238597988039,60 0.7361002712017473,42.05244714584795,60 0.7361244746945572,42.05213317966663,60 0.745435523179685,42.05203838556191,60 0.7453578815746598,42.05162691548213,60 0.7361879839649799,42.05188752247133,60 0.735996631148208,42.05163029983645,60 0.7452505538228937,42.05132411475299,60 0.745161458502912,42.05097514793548,60 0.7357121865422789,42.05144945534169,60 0.7356769533293717,42.05125445773196,60 0.7450560548935514,42.05073099176899,60 0.7450534607479531,42.05051040234263,60 0.7356271821131632,42.05105547497965,60 0.7356151489897456,42.05085323081044,60 0.7450068717131031,42.05025373585956,60 0.7449980298063963,42.04999193197326,60 0.7356257215200768,42.05065412607152,60 0.7356119358307267,42.05047186739641,60 0.7449964783915397,42.04978823079409,60 0.7449675929298372,42.04955823758451,60 0.7355735368403593,42.05021939401329,60 0.7356648934618071,42.04992605094172,60 0.7449060798328611,42.04934460628796,60 0.7448715764431957,42.04907224146502,60 0.7356857741168721,42.04967910654738,60 0.7356787967576217,42.04950562926708,60 0.7448507795070625,42.04883947550127,60 0.7448304188382515,42.0486422536901,60 0.735682077758073,42.0493344601902,60 0.7358968968837609,42.04901720170716,60 0.7448131457396601,42.04841596138626,60 0.7448043676089977,42.0482017427583,60 0.7360883774165505,42.04876135205057,60"""


LON_ORBIT = 0.7450560548935514
LAT_ORBIT = 42.05125445773196


LON =  0.7450560548935514
LAT = 42.05125445773196
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

DEMO_PATH_IMAGE = 'upload_images/captura17.png'
FCORNER = "0.7358706060867015,42.04672118972461,0"
SCORNER = "0.7460503011538533,42.04672118972461,0"
TCORNER = "0.7460503011538533,42.05369995886309,0"
FTCORNER = "0.7358706060867015,42.05369995886309,0"



IMAGE_TEXT = """
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
          <small>Drone image</small>
      </h3>
  </div>
<div class="p-lg-5" align="center">
    This is the image taken by the drone. This image has a resolution of one square meter pixel.
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
]]>
"""
DEMO_DELIMITTED_PATH_IMAGE = "upload_images/Captura17_delimitted.png"

DELIMITIED_IMAGE_TEXT = """
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
                <td>0.7699</td>
            </tr>
            <tr>
              <th>Latitude</th>
                <td>42.0472</td>
            </tr>
          <tr>
              <th>Area in Ha</th>
                <td>14.33</td>
            </tr>
        </tbody>
    </table>
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
]]>
"""


REFORESTATION_TEXT = """
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
              <small>Reforestation</small>
      </h3>
  </div>
<div class="p-lg-5" align="center">
    The reforestation is done with this drones using special seeds.
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
]]>
"""

def detect_image_bubble():
    global DEMO
    send_image(DEMO_DELIMITTED_PATH_IMAGE, FCORNER, SCORNER, TCORNER, FTCORNER, do_fly_to=False)
    send_placemark(LON, LAT, '', 'demo_bubble', 0, '', 2, DELIMITIED_IMAGE_TEXT)
    show_bubble('demo_bubble')
    i = 0
    while(DEMO and i<15):
        time.sleep(1)
        i+=1
    delete_placemark('demo_bubble', 'Placemark')


def image_burnt_bubble():
    global DEMO
    send_image(DEMO_PATH_IMAGE, FCORNER, SCORNER, TCORNER, FTCORNER, do_fly_to=False)
    send_placemark(LON, LAT, '', 'demo_bubble', 0, '', 2, IMAGE_TEXT)
    show_bubble('demo_bubble')
    i = 0
    while(DEMO and i<15):
        time.sleep(1)
        i+=1
    delete_placemark('demo_bubble', 'Placemark')



def drone_path_bubble():
    global DEMO
    draw_line(FIRST_KML_PATH, 'path_id','path_id')
    time.sleep(2)
    send_placemark(LON, LAT, '', 'demo_bubble', 0, '', 2, DRONE_PATH_TEXT)
    show_bubble('demo_bubble')
    i = 0
    while(DEMO and i<15):
        time.sleep(1)
        i+=1
    delete_placemark('path_id', 'Placemark')
    delete_placemark('path_id', 'Placemark')
    delete_placemark('demo_bubble', 'Placemark')


def reforestation_demo():
    global STOP_DRONE
    global DEMO
    array_delimitted = np.array(pilImage.open(DEMO_DELIMITTED_PATH_IMAGE))
    geolocated_contour, deltaLon, deltaLat = geo_locate_contour(array_delimitted, FTCORNER, SCORNER)
    print(geolocated_contour)
    path = get_path(geolocated_contour, deltaLon, deltaLat)
    fly_path = " ".join([ "".join("%f,%f,20" % ((path[i][0], path[i][1]))) for i in range(0, len(path)) ])
    print("<> THEEEE FLYY PATHH ISS <> %s <>" % fly_path)
    path_id = "demo_path"
    send_placemark(LON, LAT, '', 'demo_bubble', 0, '', 2, REFORESTATION_TEXT)
    show_bubble('demo_bubble')
    draw_line(fly_path, path_id, path_id)
    fly_drone(fly_path)
    delete_placemark('demo_path', 'Placemark')
    delete_placemark('demo_path', 'Placemark')


def stop():
    global DEMO
    DEMO = False
    set_stop_drone(True)
    print("> DEEEEMOOOOO VALUE %d AND STOP DRONE %d" % ((DEMO, STOP_DRONE)))


def main_demo():
    global DEMO
    DEMO = True
    print("> DEEEEMOOOOO VALUE %d" % DEMO)
    fly_to(LON_ORBIT, LAT_ORBIT, range=2000)
    while(DEMO):
        orbit(LAT_ORBIT, LON_ORBIT, 'demo', range=400)
        time.sleep(3)
        if(DEMO):
            drone_path_bubble()

        else:
            stop_orbit()
            break
        if(DEMO):
            time.sleep(3)
            image_burnt_bubble()
        else:
            stop_orbit()
            break
        if(DEMO):
            time.sleep(3)
            detect_image_bubble()
        else:
            stop_orbit()
            break
        if(DEMO):
            time.sleep(3)
            reforestation_demo()
        else:
            stop_orbit()
            break
        stop_orbit()
        clean_kml()
        time.sleep(4)
    clean_kml()
