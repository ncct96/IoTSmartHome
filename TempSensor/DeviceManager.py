def fan_control(status):
    # turn fan on
    if status:
        print("Enabled fan")
    else:
        print("Disabled fan")


def light_control(status):
    # turn light on
    if status:
        print("Enabled light")
    else:
        print("Disabled light")


def lock_door(status):
    # lock door
    if status:
        print("Locked door")
    else:
        print("Unlocked door")
