""" Excalidraw primitives"""
from Excalidraw_Interface.defaults import FONT_FAMILY
from PIL import ImageFont
import random
import uuid
import math
import copy

class ExcaliDrawPrimitive:
    """
    Base class for all excalidraw primitives
    """

    def __init__(self, excal_type: str, default_keys: dict, x=0, y=0, width=100, height=100, **kwargs):
        """
        Initialize the excalidraw primitive
        :param excal_type: type of the excalidraw primitive
        :param default_keys: default values
        :param x: top left x
        :param y: top left y
        :param width: width
        :param height: height
        :param kwargs: additional config
        """
        self.excal_type = excal_type
        self.excal_id = str(uuid.uuid4())
        self.excal_seed = random.randint(0, 100000)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.groupIds = []

        self.config = copy.deepcopy(default_keys)
        for key, value in kwargs.items():
            if key not in self.config:
                raise Exception(f"Unexpected key for shape {excal_type}: {key}")
            self.config[key] = value

    def export(self):
        """ Convert the excalidraw primitive specifications to a dictionary """
        export_dict = {'id': self.excal_id, 'type': self.excal_type, 'seed': self.excal_seed,
                       'x': self.x, 'y': self.y, 'width': self.width, 'height': self.height, 'groupIds': self.groupIds}
        export_dict.update(self.config)
        return export_dict

    @property
    def center(self):
        """ Return the center of the excalidraw primitive """
        return [self.x + self.width / 2, self.y + self.height / 2]

    @property
    def bbox(self):
        """ Return the bounding box of the excalidraw primitive"""
        return [self.x, self.y, self.x + self.width, self.y + self.height]

    def get_edge_midpoint(self, theta, padding=5):
        # given angle theta measured from the positive x-axis, return the boundary mapped to the center of the edges
        theta_lim = math.atan2(self.height, self.width)
        if abs(theta) < theta_lim or abs(theta) > math.pi - theta_lim:
            sign_indicator = (abs(theta) < math.pi / 2)
            x = self.x + self.width * sign_indicator + \
                padding * (-1 + 2 * sign_indicator)
            y = self.y + (self.height / 2)
        else:
            sign_indicator = (theta > 0)
            x = self.x + self.width / 2
            y = self.y + self.height * sign_indicator + \
                padding * (-1 + 2 * sign_indicator)
        return [x, y]


class Shape(ExcaliDrawPrimitive):
    def __init__(self, shape: str, defaults: dict, x, y, width=100, height=100, **kwargs):
        """
        Creates a rectangle, ellipse, or diamond
        :param shape: "rectangle", "ellipse", "diamond"
        :param defaults: defaults dictionary
        :param x: center x
        :param y: center y
        :param width: width
        :param height: height
        :param kwargs: other properties
        """

        x -= width/2
        y -= height/2

        super().__init__(shape, defaults, x=x, y=y, width=width, height=height, **kwargs)

class Text(ExcaliDrawPrimitive):
    """ Create a text box."""
    def __init__(self, text: str, defaults: dict, x: int, y: int, **kwargs):
        """
        Creates text
        :param text: text
        :param defaults: defaults dictionary
        :param x: center x
        :param y: center y
        :param kwargs: other properties
        """

        super().__init__('text', defaults, x, y, **kwargs)
        self.text = text

        d = super().export()
        _font_file = FONT_FAMILY[d['fontFamily']]
        _font = ImageFont.truetype(_font_file, d['fontSize'])
        left, top, right, bottom = _font.getbbox(self.text)

        self.width = right - left
        self.height = bottom - top
        self.x -= self.width / 2
        self.y -= self.height / 2

    def export(self):
        d = super().export()
        d['text'] = self.text
        return d

class Line(ExcaliDrawPrimitive):
    def __init__(self, excal_type: str, defaults: dict, start_pt: tuple, end_pt: tuple, **kwargs):
        """
        Creates a line or arrow
        :param excal_type: 'line' or 'arrow'
        :param defaults: defaults dictionary
        :param start_pt: start pt
        :param end_pt: end pt
        :param kwargs: other properties
        """

        start_x = start_pt[0]
        start_y = start_pt[1]
        end_x = end_pt[0]
        end_y = end_pt[1]
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)
        self.points = [[0, 0], [end_x - start_x, end_y - start_y]]

        super().__init__(excal_type, defaults, x=start_x, y=start_y, width=width, height=height, **kwargs)

    def export(self):
        d = super().export()
        d['points'] = self.points
        return d

    def set_start_binding(self, element: ExcaliDrawPrimitive, padding=10):
        """ Set binding in both the line as well as the element."""
        self.config["startBinding"] = {
            "elementId": element.excal_id,
            "focus": 0,
            "gap": padding
        }
        bound_e = element.config.get('boundElements', [])
        bound_e.append({
            "id": self.excal_id,
            "type": self.excal_type
        })
        element.config['boundElements'] = bound_e

    def set_end_binding(self, element, padding=10):
        """ Set binding in both the line as well as the element."""
        self.config["endBinding"] = {
            "elementId": element.excal_id,
            "focus": 0,
            "gap": padding
        }
        bound_e = element.config.get('boundElements', [])
        bound_e.append({
            "id": self.excal_id,
            "type": self.excal_type
        })
        element.config['boundElements'] = bound_e