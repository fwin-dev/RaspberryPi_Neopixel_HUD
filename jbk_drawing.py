__author__ = 'jkinney'

#Author: James Kinney and other cited/non-cited contributions.
#For educational use, no license for code, all rights reserved on product or experimental ideas and concepts.

# Color Defines
pixel_red = [125, 0, 0]  # Start Green
pixel_green = [0, 125, 0]  # Start Green
pixel_blue = [0, 0, 125]  # Start Green

# Neopixel Display
grid_x = 8  # Number of pixels wide
grid_y = 8  # Number of pixels tall
n_pixels = grid_x * grid_y


# Simple function to get the linear pixel number from X/Y
def get_raster(coordinate):
    if coordinate is [0, 0]:  # No math needed this is zero
        pixel = 0
    else:
        x, y = coordinate
        pixel = y * grid_y
        pixel += x

    return pixel


# Simple function to get the X/Y coordinate back from the linear pixel number used by OPC
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


# Create a storage grid keyed by X/Y and initialized with RGB value holder used to create linear pixel map.
# This function defaults each pixel to black(RGB LED Off)
def create_grid():
    grid = {}
    for x in range(grid_x):
        for y in range(grid_y):
            grid[x, y] = [0, 0, 0]

    return grid


#Add a line to our frame, you provide the active grid, the line to draw and the color(RGB) you want
def add_line(grid, draw_line, color):

    for new_coord in draw_line:
        grid[new_coord[0], new_coord[1]] = color


# Borrowed from roguebasin:
# http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
def bresenham(origin, dest):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end

    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = origin
    x2, y2 = dest
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points
