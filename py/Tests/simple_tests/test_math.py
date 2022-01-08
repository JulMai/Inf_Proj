def calc_new_speed_intersection_ahead(dist_to_intersection, speed):    
        max_speed = speed
        min_speed = 200
        max_dist = 5
        min_dist = 2
        exp = 3

        if dist_to_intersection == max_dist:
            return speed
        
        a = (max_speed - min_speed) / pow(max_dist - 0.5 - min_dist, exp)
        return a * pow(dist_to_intersection - min_dist, exp) + min_speed





if __name__ == '__main__':
    for i in range(2,6):
        print("{0} : {1}".format(i, calc_new_speed_intersection_ahead(i, 600)))