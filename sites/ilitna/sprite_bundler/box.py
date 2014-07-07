# coding=utf-8
"""A simple 2D packing algorithm for making sprites."""
from .conf.bundler_settings import SPRITE_SPACING


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


class HorizontalArea(Box):
    """Horizontal box area. Includes box and vertical area. Box is always placed left, vertical area fills the width
    of the area to the right. Height of the area itself gets height of the box but can be restricted to not exceed
    given height (if height is 0 then unrestricted)."""

    def __init__(self, *args, **kwargs):
        super(HorizontalArea, self).__init__(*args, **kwargs)
        self.box = None
        self.area = None

    def add(self, box):
        """Add box to the area. If don't have box yet, add it. If have box, try to recursively add it to included area.
        Return True if the box was added, False if didn't find a place to fit."""
        if self.box is None:
            # Add box to self
            if box.width > self.width or box.height > self.height > 0:
                return False
            box.x = self.x
            box.y = self.y
            self.height = box.height
            self.box = box
            return True
        else:
            # Add box to included area
            if self.area is None:
                area_width = self.width - self.box.width - SPRITE_SPACING
                area_x = self.x + self.box.width + SPRITE_SPACING
                area = VerticalArea(area_width, self.height, area_x, self.y)
                fitted = area.add(box)
                if fitted:
                    self.area = area
                return fitted
            return self.area.add(box)

    def boxes(self):
        if self.box:
            for box in self.box.boxes():
                yield box
        if self.area:
            for box in self.area.boxes():
                yield box

class VerticalArea(Box):
    """ Vertical box area. Includes list of horizontal areas. Width of the every horizontal area equals width of
    the area."""

    def __init__(self, *args, **kwargs):
        super(VerticalArea, self).__init__(*args, **kwargs)
        self.areas = []
        self.areas_height = 0

    def add(self, box):
        """Add box to the area. If don't have box yet, add it. If have box, try to recursively add it to included area.
        Return True if the box was added, False if didn't find a place to fit."""

        # Try existing areas
        for area in reversed(self.areas):
            if area.add(box):
                return True

        # Add new area if have space
        fitted = False
        if self.areas_height < self.height:
            area_height = self.height - self.areas_height
            area_y = self.y + self.areas_height
            area = HorizontalArea(self.width, area_height, self.x, area_y)
            fitted = area.add(box)
            if fitted:
                self.areas_height += area.height + SPRITE_SPACING
                self.areas.append(area)
        return fitted

    def boxes(self):
        for area in self.areas:
            for box in area.boxes():
                yield box


def arrange(boxes):
    """Arrange boxes in a rectangle.

    Basic algorithm:
    - Sort the boxes by their width.
    - Pick a width of the biggest rectangle.
    - While there are more boxes, attempt to fill a horizontal strip:
        - For each box that we haven't already placed, if it fits in the strip,
          place it, otherwise continue checking the rest of the boxes.
    """
    if not boxes:
        return [], 0
    unplaced = sorted(boxes, key=lambda box: (-box.width * box.height, -box.width, -box.height))
    max_width = unplaced[0].width
    areas = []
    areas_height = 0
    while unplaced:
        area_height = unplaced[0].height
        area = VerticalArea(max_width, area_height, 0, areas_height)
        next_unplaced = []
        for box in unplaced:
            if not area.add(box):
                next_unplaced.append(box)
        areas.append(area)
        areas_height += area_height + SPRITE_SPACING
        unplaced = next_unplaced
    return areas, areas_height
