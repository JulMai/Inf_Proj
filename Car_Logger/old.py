def add_car_to_track_c(self, piece, location, car_addr):
        global track_c
        i = 0

        old_pos = self.get_car_pos_in_track_c(car_addr)
        i_old_pos = self.get_pos_index_in_track_c(old_pos)
        #old_pos_clockwise = get_pos_clockwise(old_pos)
        # List of track_c Keys
        list_tck = list(self.track_c.keys())

        # if old_pos_clockwise:
        #    stp = -1
        # else:
        #    stp = 1
        if i_old_pos + 1 > len(list_tck) - 1:
            new_pos_prediction = list_tck[0]
        else:
            new_pos_prediction = list_tck[i_old_pos + 1]

        if self.compare_pos_loc_with_str(piece, location, new_pos_prediction):
            new_pos = new_pos_prediction
        else:
            new_pos = ""
            for i in range(i_old_pos + 1, len(list_tck)):
                pos = list_tck[i]
                if self.compare_pos_loc_with_str(piece, location, pos):
                    new_pos = pos
            if new_pos == "":
                for i in range(i_old_pos - 1):
                    pos = list_tck[i]
                    if self.compare_pos_loc_with_str(piece, location, pos):
                        new_pos = pos

        if new_pos != "":
            self.remove_car_from_track_c(car_addr)
            self.track_c[new_pos] = car_addr
            return new_pos
        else:
            return old_pos