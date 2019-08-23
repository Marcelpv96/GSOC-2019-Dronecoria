from dronecoria.settings import API_IP, DATASET_URL, PROTOTYPE
import PIL
import numpy as np


def reforest(image):
    print(API_IP)


def check_all_positions(segment_image_arr, i,j):
    return not np.array_equal(np.array((0,0,0)), segment_image_arr[i][j]) and\
                (np.array_equal(np.array((0,0,0)), segment_image_arr[i][j+1]) or\
                 np.array_equal(np.array((0,0,0)), segment_image_arr[i+1][j]) or\
                 np.array_equal(np.array((0,0,0)), segment_image_arr[i+1][j+1]) or\
                 np.array_equal(np.array((0,0,0)), segment_image_arr[i][j-1]) or\
                 np.array_equal(np.array((0,0,0)), segment_image_arr[i-1][j]) or\
                 np.array_equal(np.array((0,0,0)), segment_image_arr[i-1][j-1]))

def get_contour_pixels(burnt_image, segment_image):
    coordinates_contour = []
    segment_image_arr = np.array(segment_image)
    burnt_image_arr = np.array(burnt_image)
    for i in range(0, segment_image_arr.shape[0]):
        for j in range(0, segment_image_arr.shape[1]):
            if check_all_positions(segment_image_arr, i, j):
                coordinates_contour += [(i, j)]
                burnt_image_arr[i][j] = np.array((255,0,255))
    return burnt_image_arr

def save_delimited_image(image_name, image):
    image.save(image_name.replace(".png", "_delimitted.png"))


def gen_segment_image(burnt_image):
    prediction_mask = np.array(burnt_image)
    positions = np.all()


def draw_burnt_region(image):
    if PROTOTYPE:
        segment_image = PIL.Image.open(DATASET_URL + "/" + image.replace('upload_images','images_located_segmented'))
    else:
        segment_image = gen_segment_image(burnt_image)
    burnt_image = PIL.Image.open(image)
    print("-> start")
    burnt_image_arr = get_contour_pixels(burnt_image, segment_image)
    save_delimited_image(image, PIL.Image.fromarray(burnt_image_arr))
    print("-> end")

def gelocation_pix(coor, deltaLon, deltaLat, baseLon, baseLat):
    lon = deltaLon*coor[1] + baseLon
    lat = deltaLat*coor[0] + baseLat
    return (lon, lat)


def geo_locate_contour(array, coor_0, coor_2):
    baseLon, baseLat = list(map(float, coor_0.split(',')[:2]))
    lon_2, lat_2 = list(map(float, coor_2.split(',')[:2]))
    deltaLon = (lon_2 - baseLon)/array.shape[1]
    deltaLat = (lat_2 - baseLat)/array.shape[0]
    pos_array = np.array([[(i,j) for j in range(0, array.shape[1])] for i in range(0, array.shape[0])])
    contour_pix = pos_array[np.all( array == np.array((255, 0, 255)).reshape(1,1,3), axis=2)]
    print(contour_pix)
    geolocated_contour = [gelocation_pix(coor, deltaLon, deltaLat, baseLon, baseLat) for coor in contour_pix]
    geolocated_contour = sorted(geolocated_contour, key = lambda x: x[1])
    return geolocated_contour, deltaLon, deltaLat
