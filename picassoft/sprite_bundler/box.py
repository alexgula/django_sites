# coding=utf-8
"""A simple 2D packing algorithm for making sprites.
The idea is to pack boxes from the biggest to the smallest using a tree of containing area boxes."""
import math
from .settings import SPRITE_SPACING


class Box(object):
    def __init__(self, width, height, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def same_size(self, other):
        return self.width == other.width and self.height == other.height

    def boxes(self):
        yield self

    def __repr__(self):
        return "Box({}, {})@({}, {})".format(self.width, self.height, self.x, self.y)


class Area(Box):
    """Base class for area, contains shared methods. If area height is None, it is unrestricted."""

    def __init__(self, *args, **kwargs):
        super(Area, self).__init__(*args, **kwargs)
        self.can_grow = self.height is None
        if self.height is None:
            self.height = 0

    def fits(self, box):
        """Verify that box fits the area."""
        return box.width <= self.width and (self.can_grow or box.height <= self.height)


class HorizontalArea(Area):
    """Horizontal box area. Includes box and vertical area. Box is always placed left, vertical area fills the width
    of the area to the right. Height of the area itself gets height of the box, but can be restricted to not exceed
    given height (if height is None then unrestricted)."""

    def __init__(self, *args, **kwargs):
        super(HorizontalArea, self).__init__(*args, **kwargs)
        self.box = None
        self.area = None

    def add(self, box):
        """Add box to the area. If don't have box yet, add it. If have box, try to recursively add it to included area.
        Return True if the box was added, False if didn't find a place to fit."""

        if self.box is None:
            if not self.fits(box):
                # If does not fit, immediattely return
                return False

            # Add box to self
            box.x = self.x
            box.y = self.y
            self.height = box.height
            self.box = box

            # Add remaining area
            area_width = max(self.width - self.box.width - SPRITE_SPACING, 0)
            area_x = self.x + self.box.width + SPRITE_SPACING
            self.area = VerticalArea(area_width, self.height, area_x, self.y)
            return True

        return self.area.add(box)

    def boxes(self):
        if self.box:
            for box in self.box.boxes():
                yield box
        if self.area:
            for box in self.area.boxes():
                yield box


class VerticalArea(Area):
    """ Vertical box area. Includes list of horizontal areas. Width of the every horizontal area equals width of
    the area. Height of an area is usually restricted, if norestricted, will grow up to include all boxes (if height
    is None then unrestricted)."""

    def __init__(self, *args, **kwargs):
        super(VerticalArea, self).__init__(*args, **kwargs)
        self.areas = []
        self.arranged_height = 0

    def add(self, box):
        """Add box to the area. Try to recursively add box to included area. If did not add, create a new horizontal
        area. Return True if the box was added, False if didn't find a place to fit."""

        if not self.fits(box):
            # If does not fit, immediattely return
            return False

        # Try existing areas
        for area in self.areas:
            if area.add(box):
                return True

        if not self.can_grow and self.arranged_height >= self.height:
            # If there is no space left, return
            return False

        # Add new area
        area_height = self.height - self.arranged_height
        area_y = self.y + self.arranged_height
        area = HorizontalArea(self.width, area_height, self.x, area_y)
        fitted = area.add(box)
        if fitted:
            self.arranged_height += area.height + SPRITE_SPACING
            self.areas.append(area)
        return fitted

    def boxes(self):
        for area in self.areas:
            for box in area.boxes():
                yield box


def arrange(boxes):
    """Arrange boxes in a rectangle.

    Basic algorithm:
    - Sort the boxes by their height descending.
    - Pick a width as the square root of total image area (to form a square),
      but not less than the width of the widest rectangle.
    - While there are more boxes, attempt to fill a horizontal strip:
        - For each box that we haven't already placed, if it fits in the strip,
          place it, otherwise continue checking the rest of the boxes.
    """
    if not boxes:
        return [], 0
    unplaced = sorted(boxes, key=lambda box: -box.width)
    max_box_width = max(box.width for box in boxes)
    full_area = sum(box.width * box.height for box in boxes)
    max_width = max(max_box_width, int(math.sqrt(full_area)))
    areas = []
    areas_height = 0
    while unplaced:
        area_height = unplaced[0].height
        area = VerticalArea(max_width, area_height, 0, areas_height)
        next_unplaced = []
        placed = False
        for box in unplaced:
            if area.add(box):
                placed = True
            else:
                next_unplaced.append(box)
        if not placed:
            raise RuntimeError(u"Could not place boxes in areas.")
        areas.append(area)
        areas_height += area_height + SPRITE_SPACING
        unplaced = next_unplaced
    return areas, areas_height
