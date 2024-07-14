import datetime

now = datetime.datetime.now()

schedule = [{"grey": [0,7,8,9,16,17,18], "white": [1,2,10,11,19,20], "black": [3,4,5,6,12,13,14,15,21,22,23]},
            {"grey": [1,2,3,10,11,12,19,20,21], "white": [4,5,13,14,22,23], "black": [0,6,7,8,9,15,16,17,18]},
            {"grey": [4,5,6,13,14,15,22,23], "white": [7,8,16,17], "black": [0,1,2,3,9,10,11,12,18,19,20,21]},
            {"grey": [0,7,8,9,16,17,18], "white": [1,2,10,11,19,20], "black": [3,4,5,6,12,13,14,15,21,22,23]},
            {"grey": [1,2,3,10,11,12,19,20,21], "white": [4,5,13,14,22,23], "black": [0,6,7,8,9,15,16,17,18]},
            {"grey": [4,5,6,13,14,15,22,23], "white": [7,8,16,17], "black": [0,1,2,3,9,10,11,12,18,19,20,21]},
            {"grey": [0,7,8,9,16,17,18], "white": [1,2,10,11,19,20], "black": [3,4,5,6,12,13,14,15,21,22,23]}]

weekday = now.weekday()
offset = 0

now_area = ""
next1_area = ""
next1_hour = 25
next2_area = ""
next2_hour = 0

next1 = int(now.hour)

key_list = list(schedule[now.weekday()].keys())
val_list = list(schedule[now.weekday()].values())

for area in key_list:
    if int(now.hour) in schedule[now.weekday()][area]:
        now_area = area
        key_list.remove(area)

for i in range(4):
    if next1 == 23:
        if weekday == 6:
            weekday = 0
        else: 
            weekday +=1
        offset = 1
        next1 = 0
    else:
        next1+=1
    for area in key_list:
        if next1 in schedule[weekday][area]:
            if next1_area == "":
                next1_date_str = "" + str(now.year) + "," + str(now.month) + "," + str(now.day) + ":" + str(next1) + "-00"
                next1_date = datetime.datetime.strptime(next1_date_str, "%Y,%m,%d:%H-%M")
                if offset == 1:
                    next1_date += datetime.datetime.timedelta(days=1)
                diff = next1_date - now
                print("Now it is " + now_area.upper() + " zone, and it will be for another " + str(diff).split(".")[0] + ".")
                print("Then it will be " + area.upper() + " zone, at " + str(next1) + ":00")
                next1_area = area
                next1_hour = next1
                key_list.remove(area)
            else:
                next2_date_str = "" + str(now.year) + "," + str(now.month) + "," + str(now.day) + ":" + str(next1) + "-00"
                next2_date = datetime.datetime.strptime(next2_date_str, "%Y,%m,%d:%H-%M")
                if offset == 1:
                    next2_date += datetime.timedelta(days=1)
                diff = next2_date - now
                print("Next " + area.upper() + " will be in " + str(diff).split(".")[0] + ",at " + str(next1) + ":00.")
                next2_area = area
                next2_hour = next1
                key_list.remove(area)
            break

if len(key_list) > 0:
    for i in range(4):
        if next1 == 23:
            if weekday == 6:
                weekday = 0
            else: 
                weekday +=1
            offset = 1
            next1 = 0
        else:
            next1+=1
        for area in key_list:
            if next1 in schedule[weekday][area]: 
                next2_date_str = "" + str(now.year) + "," + str(now.month) + "," + str(now.day) + ":" + str(next1) + "-00"
                next2_date = datetime.datetime.strptime(next2_date_str, "%Y,%m,%d:%H-%M")
                if offset == 1:
                    next2_date += datetime.timedelta(days=1)
                diff = next2_date - now
                print("Next " + area.upper() + " will be in " + str(diff).split(".")[0] + ",at " + str(next1) + ":00.")
                next2_area = area
                next2_hour = next1
                key_list.remove(area)
