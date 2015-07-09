#!/usr/bin/env python

from __future__ import division
import time
import random
import math
import sys

import opc

fcserver_address = '192.168.2.40:7890'

# Create a client object
client = opc.Client(fcserver_address)

# Test if it can connect
if client.can_connect():
    print 'Connected to %s' % fcserver_address
else:
    print 'Could not connect to %s' % fcserver_address
    exit()

# RPM simulations
rpm_min = 0
rpm_max = 8000
rpm_current = 2000


# Neopixel Display
grid_x = 8  # Number of pixels wide
grid_y = 8  # Number of pixels tall
n_pixels = grid_x * grid_y
fps = 2  # Frames per second
rotation = 0  # temp testing

def get_raster(coordinate):
    if coordinate is [0, 0]:  # No math needed this is zero
        pixel = 0
    else:
        x, y = coordinate
        pixel = y * grid_y
        pixel += x

    return pixel


def get_coord(pixel):
    if pixel is 0:  # This is 0,0 coordinate
        return [0, 0]

    y = int(pixel / grid_y)
    if y is 0:
        offset = 0
    else:
        offset = grid_x * y
    x = pixel - offset

    return [x, y]


def create_grid():
    grid = {}
#    for row in range(grid_y):
#        grid.append([])
#        for column in range(grid_x):
#            grid[row].append(0)
    for x in range(grid_x):
        for y in range(grid_y):
            #new_coord = [x, y]
            grid[x, y] = [0, 0, 0]

    return grid


def add_line(grid, draw_line, color):

    for new_coord in draw_line:
        grid[new_coord[0], new_coord[1]] = color


def bresenham(origin, dest):
    # debug code
    print origin
    print dest
    # end debug code
    x0 = origin[0]; y0 = origin[1]
    x1 = dest[0]; y1 = dest[1]
    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    backward = x0 > x1
    if backward:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

#    backward = x0 > x1

#    if steep:
#        x0, y0 = y0, x0
#        x1, y1 = y1, x1
#    if backward:
#        x0, x1 = x1, x0
#        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)
    error = dx / 2
    y = y0

    if y0 < y1: ystep = 1
    else: ystep = -1

    result = []
    #if x0 > x1: xstep = -1
    #else: xstep = 1
    # debug code
    print "x0 = %d" % (x0)
    print "x1 = %d" % (x1)
    print "y0 = %d" % (y0)
    print "y1 = %d" % (y1)
    for x in range(x0, x1):
        if steep: result.append((y,x))
        else: result.append((x,y))
        error -= dy
        if error < 0:
            y += ystep
            error += dx
    # ensure the line extends from the starting point to the destination
    # and not vice-versa
    if backward: result.reverse()
    print result
    return result


while True:
    pixels = []
    rgb = [0, 0, 0]
    led_grid = create_grid()

    pixel_red = [125, 0, 0]  # Start Green
    pixel_green = [0, 125, 0]  # Start Green
    pixel_blue = [0, 0, 125]  # Start Green

    if rpm_current < 4000:  # Use green
        current_color = pixel_green
    else:
        current_color = pixel_blue
    if rpm_current > 8000:
        current_color = pixel_red

    top_line = bresenham([0, 0], [7, 0])
    bottom_line = bresenham([0, 7], [7, 7])

    if rotation is 0:
        rotation += 1
        line = bresenham([0, 1], [6, 7])
    elif rotation is 1:
        rotation += 1
        line = bresenham([4, 1], [5, 7])
    elif rotation is 2:
        rotation += 1
        line = bresenham([5, 1], [4, 7])
    elif rotation is 3:
        rotation += 1
        line = bresenham([6, 1], [0, 7])
    else:
        rotation = 0

    add_line(led_grid, top_line, current_color)
    add_line(led_grid, bottom_line, pixel_blue)
    add_line(led_grid, line, pixel_red)

    for current_pixel in range(n_pixels):
        current_coord = get_coord(current_pixel)
        rgb = tuple(led_grid[current_coord[0], current_coord[1]])
        pixels.append(rgb)

    client.put_pixels(pixels, 0)

    time.sleep(1 / fps)

