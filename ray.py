from tkinter.messagebox import NO
from lib import *
from math import *
from vector import V3
from sphere import Sphere
from material import *
from light import *



class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.background_color = color(134, 157, 202 )
        self.current_color = color(255, 255, 255)
        self.clear()
        self.scene = []
        self.light = None
    def clear(self):
        self.framebuffer = [
            [self.background_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def point(self, x, y, c=None):
        if y >= 0 and self.height and x >= 0 and x < self.width:
            self.framebuffer[y][x] = c or self.current_color

    def write(self, filename):
        writebmp(filename, self.width, self.height, self.framebuffer)

    def render(self):
        fov = int(pi/2)
        ar = self.width/self.height
        tana = tan(fov/2)

        for y in range(self.height):
            for x in range(self.width):
                color_actual = self.framebuffer[y][x]
                i = (2*(x + 0.5)/self.width - 1) * ar * tana
                j = -(2*(y + 0.5)/self.height - 1) * tana
                direction = V3(i, j, -1).norm()
                self.framebuffer[y][x] = self.cast_ray(V3(0, 0, 0), direction, color_actual)

    def cast_ray(self,origin,direction):
        material, intersect = self.scene_intersect(origin, direction)

        light_dir = (self.light.position - intersect.point).norm()
        if material:
            return material.diffuse
        else:
            return self.background_color


    def scene_intersect(self,origin,direction):
        zbuffer = 999999
        material = None
        intersect = None

        for s in self.scene:
            object_intersect = s.ray_intersect(origin,direction)
            if object_intersect:
                if object_intersect.distance < zbuffer:
                    zbuffer = intersect.distance
                    material = s.material
                    intersect = object_intersect
                return s.material, intersect
    

red = Material(diffuse=color(255,0,0))
white = Material(diffuse=color(255,255,255))


r = Raytracer(800, 800)
r.scene = [
    Sphere(V3(0, 3, -16), 2, white),
    Sphere(V3(0, -2, -16), 1, red),
    Sphere(V3(0, 0.2, -16), 1.5, white),
    
]
r.light = Light(V3(0,0,0), 1)

r.render()
r.write('r.bmp')