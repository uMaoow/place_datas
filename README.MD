place datas

install :
	download and unzip csv from https://placedata.reddit.com/data/canvas-history/2023/index.html in a subdirectory "csv"
	create a "img" directory

USAGE :
        ./main.py [options]
            
    options:
            time_slot start end
                only browse pixels between dates
            zone x y width height
                only browse pixels in zone
            name x
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


EXAMPLES

`./main.py zone 1619 1037 160 52 compare symbol.png time_slot "2023-07-22 13:00:00.00" "2023-07-24 19:00:00.00" save_id symbol_defend.txt`

will save for every hashed user_ids filling requirements save the number of pixel placed that kept or restored the symbol.png state in the 160x52 rectangle from 1619.1037 between the given date then store a json formated dictionnary of "user_id:pixel_number" in "symbol_defend.txt" 


`./main.py zone 1619 1037 160 52 reverse_compare symbol.png time_slot "2023-07-22 13:00:00.00" "2023-07-24 19:00:00.00" pixel_rate 10000 name symbol_attack`

will draw every pixel destroying the symbol.png state in the 160x52 rectangle from 1619.1037 between the given dates and save a picture of the current state every 10000 pixels in the img subdirectory


`./main.py pixel_rate 10000 use_id symbol_defend.txt 3 name symbol_defenders`

will draw for all the map and all the time pixel placed by ids recorded 3 times or more in symbol_defend.txt, then save a picture for every 10000 pixel in img with the format "symbol_defenders - date.png"



add.py and diff.py are quick tools to create a dictionnary from different data sets
./add.py A B C
will create a C dictionnary that is the A + B entries
./diff.py A B C
will create a C dictionnary that is the A entries without any of the B entries
