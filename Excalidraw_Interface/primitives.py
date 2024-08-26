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

    def __init__(self, excal_type: str, default_config: dict,
                 x: float, y: float, width: float, height: float, **kwargs):
        """
        Initialize the excalidraw primitive
        :param excal_type: type of the excalidraw primitive
        :param default_config: default values
        :param x: top left x
        :param y: top left y
        :param width: width
        :param height: height
        :param kwargs: additional config to override defaults
        """
        self.excal_type = excal_type
        self.excal_id = str(uuid.uuid4())
        self.excal_seed = random.randint(0, 100000)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._groupIds = []
        self.apply_recursive_groups = []

        self.config = copy.deepcopy(default_config)
        for key, value in kwargs.items():
            if key not in self.config:
                raise Exception(f"Unexpected key for shape {excal_type}: {key}")
            self.config[key] = value

    def export(self):
        """ Convert the excalidraw primitive specifications to a dictionary """
        export_dict = {'id': self.excal_id, 'type': self.excal_type, 'seed': self.excal_seed,
                       'x': self.x, 'y': self.y, 'width': self.width, 'height': self.height,
                       'groupIds': self._groupIds}
        export_dict.update(self.config)
        return export_dict

    def add_to_group(self, group_id):
        self._groupIds.append(group_id)
        for elem in self.apply_recursive_groups:
            elem.add_to_group(group_id)

    @property
    def center(self):
        """ Return the center of the excalidraw primitive """
        return [self.x + self.width / 2, self.y + self.height / 2]

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
    def __init__(self, shape: str, default_config, x, y, width, height, **kwargs):
        """
        Creates a rectangle, ellipse, or diamond
        :param shape: "rectangle", "ellipse", "diamond"
        :param default_config: default values
        :param x: center x
        :param y: center y
        :param width: width
        :param height: height
        :param kwargs: additional config to override defaults
        """

        x -= width/2
        y -= height/2

        super().__init__(shape, default_config, x=x, y=y, width=width, height=height, **kwargs)

#TODO - fix fonts
class Text(ExcaliDrawPrimitive):
    def __init__(self, text: str, default_config, x, y, **kwargs):
        """
        Creates text item, width and height set automatically
        :param text: text
        :param default_config: default values
        :param x: center x
        :param y: center y
        :param kwargs: additional config to override defaults
        """

        super().__init__('text', default_config, x, y, 0, 0, **kwargs)
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
    def __init__(self, excal_type, default_config, start_pt: tuple, end_pt: tuple, **kwargs):
        """
        Creates a line or arrow
        :param excal_type: 'line' or 'arrow'
        :param default_config: default values
        :param start_pt: start pt | tuple[float, float]
        :param end_pt: end pt | tuple[float, float]
        :param kwargs: additional config to override defaults
        """

        start_x = start_pt[0]
        start_y = start_pt[1]
        end_x = end_pt[0]
        end_y = end_pt[1]
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)
        self.points = [[0, 0], [end_x - start_x, end_y - start_y]]

        super().__init__(excal_type, default_config, x=start_x, y=start_y, width=width, height=height, **kwargs)

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

class Group(ExcaliDrawPrimitive):
    def __init__(self, elems: list[ExcaliDrawPrimitive], first_is_group = False):
        """
        Create a group (a fake element for handling group logic)
        :param elems: list of excalidraw objects to group
        :param first_is_group: treat the first element of the list as representing the whole group
        """
        group_id = str(uuid.uuid4())

        left_x = min([elem.x for elem in elems])
        top_y = min([elem.y for elem in elems])
        width = max([elem.x + elem.width - left_x for elem in elems])
        height = max([elem.y + elem.height - top_y for elem in elems])

        for elem in elems:
            elem.add_to_group(group_id)

        super().__init__('group', {}, left_x, top_y, width, height)
        self.elems = elems

        if first_is_group:
            elems[0].apply_recursive_groups.extend(elems[1:])

    def export(self):
        raise Exception("Group should not be exported - a group was incorrectly added to sketch.")

    def add_to_group(self, group_id):
        for elem in self.elems:
            elem.add_to_group(group_id)