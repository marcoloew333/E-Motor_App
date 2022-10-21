direction = 'Stopped'
degree = 0

def update_rot_dir(dir):
    global direction
    direction = dir

def get_rot_dir():
    global direction
    return direction

def update_degree(deg):
    global degree
    degree += deg

def get_degree():
    global degree
    return degree
