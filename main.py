from PIL import Image
import json
from sys import argv
from dateutil import parser as dateparse
import csv
img = Image.new( 'RGBA', (3000,2000), "#00000000") 


compare = [False, None, None]
reverse_compare = [False, None, None]
save_id = [False, ""]
use_id = [False, 0]
id_dict = {}
zone = [False, [0,0,0,0]]
time_slot = [False, 0,0]
pixel_rate = -1
pixel = 0
imgname = ""





def usage():
    print("
        ./main.py [options]
            
    options:
            time_slot start end
                only browse pixels between dates
            zone x y width height
                only browse pixels in zone
            name x.png
                name used to save picture files
            pixel_rate x
                if set, save a picture every x pixel drawn
            compare x.png
                only record pixel egals (coords and color) to the ones in given picture file
            reverse_compare
                only record pixel differents (coords and color) to the ones in given picture file (ignore non full alpha pixels)
            save_id x.txt
                save hashed user_id of every pixel which fills set requirements into x.txt
            use_id x.txt y
                only browse pixel set by user ids found y times according to x.txt list
          ")
def parse_argv():
    global zone, time_slot, pixel_rate, imgname, compare, save_id, id_dict, reverse_compare
    if len(argv) == 1:
        return
    i = 1
    while i < len(argv):
        print(argv[i])
        if argv[i] == "time_slot":
            if i + 2 >= len(argv):
                usage()
                return
            time_slot[0] = True
            time_slot[1] = dateparse.parse(argv[i + 1])
            time_slot[2] = dateparse.parse(argv[i + 2])
            print (time_slot)
            i += 2
        if argv[i] == "zone":
            if i + 4 >= len(argv):
                usage()
                return
            zone[0] = True
            zone[1][0] = int(argv[i + 1])
            zone[1][1] = int(argv[i + 2])
            zone[1][2] = int(argv[i + 3])
            zone[1][3] = int(argv[i + 4])
            i += 4
        if argv[i] == "name":
            if i + 1 >= len(argv):
                usage()
                return
            imgname = argv[i + 1]
            i += 1
        if argv[i] == "pixel_rate":
            if i + 1 >= len(argv):
                usage()
                return
            pixel_rate = int(argv[i + 1])
            print(pixel_rate)
            i += 1
        if argv[i] == "reverse_compare":
            if i + 1 >= len(argv):
                usage()
                return
            reverse_compare[0] = True
            reverse_compare[2] = Image.open(argv[i + 1])
            reverse_compare[1] = reverse_compare[2].load()

            i += 1
        if argv[i] == "compare":
            if i + 1 >= len(argv):
                usage()
                return
            compare[0] = True
            compare[2] = Image.open(argv[i + 1])
            compare[1] = compare[2].load()

            i += 1
        if argv[i] == "save_id":
            if i + 1 >= len(argv):
                usage()
                return
            save_id[0] = True
            save_id[1] = argv[i + 1]
            i += 1
        if argv[i] == "use_id":
            if i + 2 >= len(argv):
                usage()
                return
            with open(argv[i + 1]) as jsonf:
                id_dict = json.load(jsonf)
            use_id[0] = True
            use_id[1] = int(argv[i + 2])
            i += 2
        i += 1
 
def get_date_range():
    if time_slot[0] == False:
        return 0,53
    start = -1
    stop = -1
    for i in range(53):
        if stop != -1:
            print("start %d" % start)
            print("stop %d" % stop)
            return start, stop
        name = 'csv/2023_place_canvas_history-0000000000' + str("%02d" % i)
        with open(name+'.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if row[0][0:] != "timestamp":
                    tmp = dateparse.parse(row[0][:-3])
                    if tmp < time_slot[1]:
                        start = i
                    if tmp > time_slot[2]:
                        stop = i
                    break


def is_in_zone(row):
    if int(row[2][1:])+1500 < zone[1][0]:
        return False
    if int(row[3][:-1])+1000 < zone[1][1]:
        return False
    if int(row[2][1:])+1500 > zone[1][0] + zone[1][2]:
        return False
    if int(row[3][:-1])+1000 > zone[1][1] + zone[1][3]:
        return False
    return True

def correct_id(row):
    tmp = row[1]
    if id_dict.get(row[1]) == None:
        return False
    if id_dict[row[1]] < use_id[1]:
        return False
    return True

def is_in_time(row):
    global pixel
    tmp = dateparse.parse(row[0][:-3])
    if tmp < time_slot[1]:
        return False
    if tmp > time_slot[2]:
        return False
    return True

def draw(row):
    global pixel, pixel_rate, imgname, save_id, id_dict, compare, reverse_compare
    hcolor = row[4][1:]
    hred, hgreen, hblue = hcolor[:2], hcolor[2:4], hcolor[4:]
    red, green, blue = int("0x"+hred, 16), int("0x"+hgreen, 16), int("0x"+hblue, 16)
    if reverse_compare[0] == True:
        if reverse_compare[1][int(row[2][1:])+1500, int(row[3][:-1])+1000][3] != 255:
            return
        if reverse_compare[1][int(row[2][1:])+1500, int(row[3][:-1])+1000] == (red, green, blue, 255):
            return
    if compare[0] == True:
        if compare[1][int(row[2][1:])+1500, int(row[3][:-1])+1000] != (red, green, blue, 255):
            return
    pixels[int(row[2][1:])+1500, int(row[3][:-1])+1000] = (red, green, blue)
    if save_id[0] == True:
        if id_dict.get(row[1]) == None:
            id_dict[row[1]] = 0
        id_dict[row[1]] += 1
    if pixel_rate != -1:
        if pixel % pixel_rate == 0:
            img.save("img/%s.png" % (imgname + " - " + row[0][:-3]))
        pixel += 1



parse_argv()


for file_nb in range(*get_date_range()):
    not_parsed = 0
    parsed = 0
    name = 'csv/2023_place_canvas_history-0000000000' + str("%02d" % file_nb)
    print(name)
    pixels = img.load() # create the pixel map

    with open(name+'.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0][0:] != "timestamp":
                if row[4][0] == "#":
                    parsed += 1
                    if zone[0] == True:
                        if is_in_zone(row) == False:
                            continue
                    if time_slot[0] == True:
                        if is_in_time(row) == False:
                            continue
                    if use_id[0] == True:
                        if correct_id(row) == False:
                            continue
                    draw(row)
                else:
                    not_parsed += 1


    print("not parsed %d" % not_parsed)
    print("parsed %d" % parsed)
    ratio = not_parsed / parsed
    print("ratio %f" % ratio)
if (save_id[0] == True):
    with open(save_id[1], "w") as fp:
        sorted_dic = sorted(id_dict.items(), key=lambda x:x[1])
        print(sorted_dic)
        json.dump(id_dict, fp)
    print("dict saved in %s" % save_id[1])
print("%s.png" % imgname)
img.save("%s.png" % imgname)
