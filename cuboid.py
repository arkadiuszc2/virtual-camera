import pygame
import sys
import numpy as np
import math
import projection as proj


class Cuboid:
    def __init__(self, vertices):
        self.vertices = np.array(vertices)
        self.clipped_vertices = self.vertices.copy()
        self.projected_vertices = self.vertices.copy()
        self.center = np.mean(self.vertices, axis=0)
        self.clipped_edges = self.vertices.copy()
        self.clipped_vertices = []


    def translate(self, dx, dy, dz):
        translation_matrix = np.array([[1, 0, 0, dx],
                                       [0, 1, 0, dy],
                                       [0, 0, 1, dz],
                                       [0, 0, 0, 1]])
        for i in range(len(self.vertices)):
            self.vertices[i] = np.dot(translation_matrix, self.vertices[i])
        
    def rotate(self, axis, angle):
        theta = np.radians(angle)
        cos, sin = np.cos(theta), np.sin(theta)

        if axis == 'x':
            rotation_matrix = np.array([[1, 0, 0, 0],
                                        [0, cos, -sin, 0],
                                        [0, sin, cos, 0],
                                        [0, 0, 0, 1]])
        elif axis == 'y':
            rotation_matrix = np.array([[cos, 0, sin, 0],
                                        [0, 1, 0, 0],
                                        [-sin, 0, cos, 0],
                                        [0, 0, 0, 1]])
        elif axis == 'z':
            rotation_matrix = np.array([[cos, -sin, 0, 0],
                                        [sin, cos, 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]])
        else:
            return
            
        for i in range(len(self.vertices)):
            self.vertices[i] = np.dot(rotation_matrix, self.vertices[i]) ###



    def apply_transformation(self, matrix):
        self.vertices = np.dot(matrix, self.vertices)

    def project_to_2d(self, fov, aspect_ratio, near, far):
        f = 1 / math.tan(fov / 2)

        proj_matrix = np.array([
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, far / (far - near), (far * near) / (near - far)],
        [0, 0, 1, 0]
    ])

        for i in range(0,len(self.clipped_vertices)):
            if self.clipped_vertices[i] is not None and len(self.clipped_vertices[i])!=1:
                vertex = np.dot(proj_matrix, self.clipped_vertices[i]) 
                w = math.fabs(vertex[3])

                if vertex[3] == 0:  
                    return vertex

                vertex = np.array(vertex)
                self.projected_vertices[i] = [vertex[0] / w, vertex[1] / w, vertex[2] / w, 1]
        
    

    def draw(self, screen, fov, aspect_ratio, near, far):
        
        edges_scheme = [(0, 1), (1, 2), (2, 3), (3, 0),
                 (4, 5), (5, 6), (6, 7), (7, 4),
                 (0, 4), (1, 5), (2, 6), (3, 7)]

        edges = []
        for i in range(0, len(edges_scheme)):
            edges.append([self.vertices[edges_scheme[i][0]],self.vertices[edges_scheme[i][1]]])
            
        edges, hidden_edges_ids = self.clip_edges(edges, near)

        clipped_vertices = [[0]]*8

        for i, scheme in enumerate(edges_scheme):
            if edges[i] != 0:
                clipped_vertices[scheme[0]] = edges[i][0]
                clipped_vertices[scheme[1]] = edges[i][1]

        self.clipped_vertices = clipped_vertices

        self.project_to_2d(math.radians(fov), aspect_ratio, near, far)


        for i in range(len(self.projected_vertices)):
            self.projected_vertices[i] = self.adjust_to_screen(self.projected_vertices[i], 600, 600)

        projected_vertices_2d = self.projected_vertices[:, :2]

        for i in range(0,len(edges_scheme)):
            if(hidden_edges_ids[i] !=1):
                    pygame.draw.line(screen, (255, 255, 255), projected_vertices_2d[edges_scheme[i][0]], projected_vertices_2d[edges_scheme[i][1]], 2)



    def adjust_to_screen(self, vertex, WIDTH, HEIGHT):
        return (vertex[0] * WIDTH / 2 + WIDTH / 2, vertex[1] * HEIGHT / 2 + HEIGHT / 2, vertex[2], vertex[3])
    
    def clip_edges(self, edges, near):
        clipped_edges = [0]*12
        hidden_edges_ids = [0] * 12
        
        for i, edge in enumerate(edges):
            clipped_edge = self.clip_edge(edge, near)
            if clipped_edge:
                clipped_edges[i] = clipped_edge
            else:
                hidden_edges_ids[i] = 1

        return clipped_edges, hidden_edges_ids
    
    def clip_edge(self, edge, near):
    
        p1 = edge[0]
        p2 = edge[1]
        z_p1 = edge[0][2]
        z_p2 = edge[1][2]

        if z_p1 < near and z_p2 < near:
            return None
        
        if z_p1 < near:
            t = (near - z_p1) / (z_p2 - z_p1)
            p1 = p1 + t * (p2 - p1)
        
        if z_p2 < near:
            t = (near - z_p2) / (z_p1 - z_p2)
            p2 = p2 + t * (p1 - p2)

        return (p1, p2)






