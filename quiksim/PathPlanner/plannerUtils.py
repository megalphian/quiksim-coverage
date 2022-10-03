import math
import numpy as np
import vg as vec_geo

def calculate_angle_deg(vector1, vector2):
    x1, y1 = vector1
    x2, y2 = vector2
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    if(len1 == 0 or len2 == 0):
        # Some ranks may have zero length if it only covers a single grid cell
        # We're handling this now, but in case we aren't, just return a 0
        return 0
    cosine_val = round(inner_product/(len1*len2), 3)
    return (math.acos(cosine_val) * (180 / math.pi))

def get_signed_angle_deg(vector1, vector2):
    # +1 counterclockwise
    # -1 clockwise

    v1 = np.append(np.asarray(vector1), [[0]])
    # v1.a
    v2 = np.append(np.asarray(vector2), [[0]])
    angle = vec_geo.signed_angle(v1, v2, vec_geo.basis.z)
    return angle

def path_to_vec(path, inverted):
    # Turns are counted as number of line segments + 1
    start = 0
    end = 1
    if(inverted):
        start = 1
        end = 0
    
    x_vec = path[end][0] - path[start][0]
    y_vec = path[end][1] - path[start][1]

    return (x_vec, y_vec)