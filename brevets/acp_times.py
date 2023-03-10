"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

import math


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.

    """

    if control_dist_km >= brevet_dist_km:

        brevet_dist_km = control_dist_km

    if control_dist_km <= 0:

        return brevet_start_time

    if control_dist_km <= 200:

        hours = control_dist_km / 34

        minutes = (hours % 1) * 60

        hours1 = math.floor(hours)

        minutes1 = round(minutes)

        return brevet_start_time.shift(hours=hours1, minutes=minutes1)

    else:

        if (200 < control_dist_km <= 400):
            
            hours = (200/34) + ((control_dist_km - 200) / 32)

            minutes = (hours % 1) * 60 

            hours1 = math.floor(hours)

            minutes1 = round(minutes)

            return brevet_start_time.shift(hours=hours1, minutes=minutes1)

        if (400 < control_dist_km <= 600):

            hours = (200/34) + (200/32) + ((control_dist_km - 400) / 30)

            minutes = (hours % 1) * 60

            hours1 = math.floor(hours)

            minutes1 = round(minutes)

            return brevet_start_time.shift(hours=hours1, minutes=minutes1)

        if (600 < control_dist_km <= 1000):

            hours = (200/34) + (200/32) + (200/30) + ((control_dist_km - 600) / 28)

            minutes = (hours % 1) * 60

            hours1 = math.floor(hours)

            minutes1 = round(minutes)

            return brevet_start_time.shift(hours=hours1, minutes=minutes1)

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    time_table = {200: brevet_start_time.shift(hours=13, minutes=30), 
                  300: brevet_start_time.shift(hours=20), 
                  400: brevet_start_time.shift(hours=27), 
                  600: brevet_start_time.shift(hours=40), 
                  1000: brevet_start_time.shift(hours=75)}

    if control_dist_km == brevet_dist_km:

        return time_table[control_dist_km]

    if control_dist_km < 0:

        return brevet_start_time

    if control_dist_km > brevet_dist_km:

        brevet_dist_km = control_dist_km

    if 0 <= control_dist_km <= 60:

        hours = (control_dist_km / 20) + 1

        minutes = (hours % 1) * 60

        hours1 = math.floor(hours)

        minutes1 = round(minutes)

        return brevet_start_time.shift(hours=hours1, minutes=minutes1)

    if 60 < control_dist_km <= 600:

        hours = control_dist_km / 15

        minutes = (hours % 1) * 60

        hours1 = math.floor(hours)

        minutes1 = round(minutes)

        return brevet_start_time.shift(hours=hours1, minutes=minutes1)

    if (600 < control_dist_km <= 1000):

        hours = (600/15) + ((control_dist_km - 600) / 11.428)

        minutes = (hours % 1) * 60

        hours1 = math.floor(hours)

        minutes1 = round(minutes)

        return brevet_start_time.shift(hours=hours1, minutes=minutes1)