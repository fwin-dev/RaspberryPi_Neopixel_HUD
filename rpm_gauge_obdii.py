#!/usr/bin/env python

#Author: James Kinney and other cited/non-cited contributions.
#For educational use, no license for code, all rights reserved on product or experimental ideas and concepts.

from __future__ import division
import time
from jbk_drawing import *
import opc
import random

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
rpm_current = 0

fps = 20  # Frames per second

flipflop = 0

while True:

    # Now we need to create a simulated rpm sweep
    # seem to randomly change rpm per frame, like running car might.
    base_seed = 100  # We always start with at least idle

    base_seed += random.randint(50, 100)  # Now we add a modulator
    ratemod = random.randint(0, 2)
    if flipflop is 0 and ratemod is not 2:
        rpm_current += base_seed  # Positive state
    else:
        rpm_current -= base_seed  # Negative State

    if rpm_current > 8000: # Need to reset
        if flipflop is 1:
            flipflop = 0
        else:
            flipflop = 1

    if rpm_current < 1000 and flipflop is 1:
        flipflop = 0

    # End Test loop

    # Storage location for ultimate raster image
    pixels = []
    # Define our rgb pixel storage location used to create raster.
    rgb = [0, 0, 0]
    # X/Y grid we draw on
    led_grid = create_grid()

    # Setup the background of our display for base color
    if rpm_current < 4000:  # Use green
        current_color = pixel_green
    else:
        current_color = pixel_blue
    if rpm_current >= 8000:
        current_color = pixel_red

    # Draw top and bottom lines
    top_line = bresenham([0, 0], [7, 0])
    bottom_line = bresenham([0, 7], [7, 7])

    # Create our static bar that indicates blueline and redline status
    add_line(led_grid, top_line, current_color)
    add_line(led_grid, bottom_line, pixel_blue)

    if rpm_current < 1000 and rpm_current > 0: #  RPMs less than smallest setting, this is idle
        bars = 1
    else:
        bars = int(rpm_current/1000)  # Smooth out to single groups of 1000 RPM

    # Add bar graph lines when needed, simple math to create linear graph Y-1,X+1
    for bar in range(bars):
        graph_line = bresenham([0+bar, 7], [0+bar, 7-bar])  # Create bar that is +1X and -1Y per 1000 RPM
        add_line(led_grid, graph_line, pixel_red)

    # Create Raster
    for current_pixel in range(n_pixels):
        current_coord = get_coord(current_pixel)
        rgb = tuple(led_grid[current_coord[0], current_coord[1]])
        pixels.append(rgb)

    # Push pixels via OPC client
    client.put_pixels(pixels, 0)

    time.sleep(1 / fps)

