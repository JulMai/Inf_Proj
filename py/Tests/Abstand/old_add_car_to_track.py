def add_car_to_track_c(pos, car):
    global track_c
    i = 0
    piece = pos[0]
    location = pos[1]
    car_before = None
    new_pos = ""

    for x in list(track_c.keys()):
        if track_c[x] == car:
            car_before = x
        if car_before != None:
            if (int(x[2:4]) == piece and int(x[4:6]) == location):
                remove_car_from_track_c(car)            
                new_pos = x
                i += 1 
                break
        i += 1
    
    if new_pos == "":
        i = 0
        for x in list(track_c.keys()):
            if int(x[2:4]) == piece and int(x[4:6]) == location:
                remove_car_from_track_c(car)            
                new_pos = x
                i += 1 
                break
            i += 1


    if car_before == None:
        for x in list(track_c.keys()):
            if int(x[2:4]) == piece and int(x[4:6]) == location:
                new_pos = x
                i += 1
                break
            i += 1

    if new_pos != '' and new_pos != car_before:        
        track_c[new_pos] = car
        logging.info("Car: {0}: Position: {1}".format(car, new_pos))
    return i