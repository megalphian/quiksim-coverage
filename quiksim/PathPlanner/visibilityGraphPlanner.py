from ctypes import ArgumentError

import math
import cv2
import numpy as np
from PathPlanner.debug import stdout_redirected
from PathPlanner.plannerUtils import calculate_angle_deg, DriveType

import visilibity as vis

from enum import Enum

def create_cost_strategy(dynamics, cur_path_vec, next_path_vec):
    if(dynamics.drive_type == DriveType.acceleration_based):
        return create_traversal_time_strategy(cur_path_vec, next_path_vec, dynamics)
    elif(dynamics.drive_type == DriveType.velocity_based):
        return create_vel_traversal_time_strategy(cur_path_vec, next_path_vec, dynamics)
    else:
        raise ArgumentError("Invalid Strategy Type")

def create_traversal_time_strategy(rank_1_vec, rank_2_vec, dynamics):
    # lin_vel chosen to mimic a roomba's normal speed - 1m/s = 100 cm/s - 20 px/s
    # lin_acc chosen so that max velocity can be reached quickly
    # ang_vel chosen arbitrarily

    # Parametrize this
    # lin_vel = 20 # 1m/s
    max_lin_vel = dynamics.get_lin_vel() # 3m/s
    lin_acc = dynamics.get_lin_acc() # 0.5m/s2
    ang_vel = dynamics.ang_vel

    fn_pointer = lambda vg_path: VG_Cost_Strategies.acc_traversal_time(vg_path, rank_1_vec, rank_2_vec, max_lin_vel, ang_vel, lin_acc)
    return fn_pointer

def create_vel_traversal_time_strategy(start_vec, end_vec, dynamics):
    # lin_vel chosen to be 5 px/s = 25 cm/s to mimic a roomba's normal speed - 1m/s = 100 cm/s - 20 px/s
    # lin_acc chosen so that max velocity can be reached quickly
    # ang_vel chosen arbitrarily

    lin_vel = dynamics.get_lin_vel()
    ang_vel = dynamics.ang_vel

    fn_pointer = lambda vg_path: VG_Cost_Strategies.vel_traversal_time(vg_path, start_vec, end_vec, lin_vel, ang_vel)
    return fn_pointer

class VG_Cost_Strategies:

    @staticmethod
    def euc_distance(vg_path):
        return vg_path.length()
    
    @staticmethod
    def acc_traversal_time(vg_path, start_vec, end_vec, max_lin_vel, ang_vel, lin_acc):
        # lin_vel => px/s
        # ang_vel => deg/s
        # lin_acc => px/s^2

        # Eqs. of motions used:
        # s = ut + (at^2)/2
        # v^2 = u^2 + 2as
        # v = u + at
        
        path = vg_path.path()
        
        last_vec = start_vec
        total_turn_time = 0
        turns = 0
        linear_time = 0
        total_angle = 0

        for index in range(len(path) - 1):
            pt1 = path[index]
            pt2 = path[index + 1]
            new_vec = (pt2.x() - pt1.x(), pt2.y() - pt1.y())

            length = vis.distance(pt1, pt2)
            s1 = length / 2
            s2 = (max_lin_vel**2) / (2 * lin_acc)
            if(s1 >= s2):
                s3 = s1 - s2
                linear_time += 2 * ((s3 / max_lin_vel) + (max_lin_vel / lin_acc))
            else:
                linear_time += 2 * math.sqrt((2 * s1) / lin_acc)

            angle = calculate_angle_deg(last_vec, new_vec)
            if(angle != 0):
                turns += 1
                total_angle += angle
            total_turn_time += angle / ang_vel
            last_vec = new_vec
        
        new_vec = end_vec
        angle = calculate_angle_deg(new_vec, last_vec)
        if(angle != 0):
            turns += 1
            total_angle += angle
        total_turn_time +=  angle / ang_vel

        total_time = linear_time + total_turn_time
        return (total_time, turns, total_angle)
    
    @staticmethod
    def vel_traversal_time(vg_path, start_vec, end_vec, lin_vel, ang_vel):
        linear_time = vg_path.length() / lin_vel

        path = vg_path.path()
        last_vec = start_vec
        total_turn_time = 0
        turns = 0
        total_angle = 0

        for index in range(len(path) - 1):
            pt1 = path[index]
            pt2 = path[index + 1]
            new_vec = (pt2.x() - pt1.x(), pt2.y() - pt1.y())

            angle = calculate_angle_deg(last_vec, new_vec)
            
            # Megnath: Just random thought. Remove once confirmed
            if(angle < 0):
                raise

            if(angle != 0):
                turns += 1
                total_angle += angle
            total_turn_time += angle / ang_vel
            last_vec = new_vec
        
        new_vec = end_vec
        angle = calculate_angle_deg(new_vec, last_vec)

        # Megnath: Just random thought. Remove once confirmed
        if(angle < 0):
            raise

        if(angle != 0):
            turns += 1
            total_angle += angle
        total_turn_time +=  angle / ang_vel

        total_time = linear_time + total_turn_time
        return (total_time, turns, total_angle)

def contour_to_vis_polygon(contour):
    poly_list = []
    c_list = list(contour)
    
    # Since we are working in the image axis, we'd need to reverse the contour to make a valid vis polygon
    c_list.reverse()

    min_i = 0
    for i in range(1, len(c_list)):
        point_x = c_list[min_i][0][0]
        point_y = c_list[min_i][0][1]
        new_point_x = c_list[i][0][0]
        new_point_y = c_list[i][0][1]
        if((new_point_x < point_x) or (new_point_x == point_x and new_point_y < point_y)):
            min_i = i
            
    temp = c_list[:min_i]
    c_list = c_list[min_i:]
    c_list.extend(temp)

    for vertex in c_list:
        # Have to cast as int because np.int32 isn't being accepted
        poly_list.append(vis.Point(int(vertex[0][0]), int(vertex[0][1])))

    return vis.Polygon(poly_list)

class VisibilityGraphPlanner:

    def __init__(self, iop, config):
        # Hyper parameter as defined by Visilibity
        self.epsilon = 0.0000001

        self.envs, self.vgs = VisibilityGraphPlanner.create_visibility_graph(iop, self.epsilon, config)

        self.main_env = self.envs[0]
        self.main_vg = self.vgs[0]
        for env_id in range(1, len(self.envs)):
            env = self.envs[env_id]
            if(env.area() > self.main_env.area()):
                self.main_env = env
                self.main_vg = self.vgs[env_id]

    def planning(self, sx, sy, fx, fy):
        start = vis.Point(sx, sy)
        end = vis.Point(fx, fy)

        if not(start._in(self.main_env)) or not(end._in(self.main_env)):
            return None
        
        # There is no way to turn off the extremely verbose C++ debug output from the path planning algorithm
        # This decorator can accept a file output to dump the debug logs if we need it
        with stdout_redirected():
            shortest_path = self.main_env.shortest_path(start, end, self.main_vg, self.epsilon)
        
        path = []
        for point in shortest_path.path():
            path.append([point.x(), point.y()])

        return path

    def calculate_cost(self, path, cost_strategy):
        if(path == None):
            return (None, None, None, None)

        vis_path_points = []
        for point in path:
            vis_path_points.append(vis.Point(point[0], point[1]))

        vis_path = vis.Polyline(vis_path_points)

        cost, turns, total_angle = cost_strategy(vis_path)
        length = VG_Cost_Strategies.euc_distance(vis_path)

        return (length, cost, turns, total_angle)

    @staticmethod
    def create_visibility_graph(iop, epsilon, config, debugging = False):

        threshold = np.uint8(np.asarray(iop))

        # Erode more to allow for some space from the boundaries
        # Taking a matrix of size 3 as the kernel
        k = config.erosion_kernel_size

        kernel = np.ones((k,k), np.uint8)
        threshold_dilation = cv2.erode(threshold, kernel, iterations=1)
        threshold_dilation = cv2.medianBlur(threshold_dilation, config.dilation_kernel_size)

        # Detect contours to get the polygons in the rectilinear approximation
        # https://www.geeksforgeeks.org/python-detect-polygons-in-an-image-using-opencv/

        contours, hierarchy = cv2.findContours(threshold_dilation, cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_TC89_L1)

        env_sets = []
        unvisited_contours = [*range(len(contours))]

        while unvisited_contours:
            current_contour = unvisited_contours[0]
            
            parent_contour = current_contour
            contour_hierarchy = hierarchy[0][parent_contour]

            while(contour_hierarchy[3] != -1):
                parent_contour = contour_hierarchy[3]
                contour_hierarchy = hierarchy[0][parent_contour]
            
            bound_poly = contour_to_vis_polygon(contours[parent_contour])
            if debugging:
                print('Bound: ',bound_poly.is_in_standard_form())
            env_polys = [bound_poly]

            if(parent_contour not in unvisited_contours):
                unvisited_contours.remove(current_contour)
                continue

            unvisited_contours.remove(parent_contour)
            parent_hierarchy = hierarchy[0][parent_contour]

            # Access the child layer in the hierarchy
            # Split into a seperate function

            child_contour = parent_hierarchy[2]
            if(child_contour == -1):
                env_sets.append(env_polys)
                continue

            unvisited_contours.remove(child_contour)
            child_hierarchy = hierarchy[0][child_contour]
            
            child_poly = contour_to_vis_polygon(contours[child_contour])
            if debugging:
                print('Child: ',child_poly.is_in_standard_form())
            env_polys.append(child_poly)

            # right now we're assuming there is no third nested layer
            # No premature optimization :)
            queue = [child_hierarchy[0], child_hierarchy[1]]

            while queue:
                index = queue.pop(0)
                if index == -1 or index not in unvisited_contours:
                    continue

                unvisited_contours.remove(index)

                child_poly = contour_to_vis_polygon(contours[index])
                if debugging:
                    print('Child: ',child_poly.is_in_standard_form())
                env_polys.append(child_poly)
                
                child_hierarchy = hierarchy[0][index]
                queue.append(child_hierarchy[0])
                queue.append(child_hierarchy[1])
            
            env_sets.append(env_polys)

        vgs = []
        envs = []
        for env_polys in env_sets:
            env = vis.Environment(env_polys)
            if(env.is_valid(epsilon)):
                vg = vis.Visibility_Graph(env, epsilon)

                envs.append(env)
                vgs.append(vg)
            else:
                print('Invalid Polygon!!')

        return (envs, vgs)
