# Excalidraw_Interface

![Tests Badge](https://github.com/RobertJN64/Excalidraw_Interface/actions/workflows/tests.yml/badge.svg)
![Python Version Badge](https://img.shields.io/pypi/pyversions/Excalidraw_Interface)
![License Badge](https://img.shields.io/github/license/RobertJN64/Excalidraw_Interface)

A pythonic interface for creating diagrams in Excalidraw.

Based on https://github.com/BardOfCodes/procXD by Aditya Ganeshan (MIT License) and updated with modern python support
and API improvements.

## Example: Flowchart

[flowchart.py](Excalidraw_Interface/examples/flowchart.py)

![flowchart image](images/flowchart.png)

```python
from Excalidraw_Interface import SketchBuilder

flowchart_items = ['First Step', 'Second Step', 'Third Step']

sb = SketchBuilder() # Create a Sketch

prev_item = sb.TextBox("Start Here", x = 0, y = 0) # Create a Text Box
for index, item in enumerate(flowchart_items):
    new_item = sb.TextBox(item, x = 0, y = (index+1) * 150) # Create a Text Box
    sb.create_binding_arrows(prev_item, new_item) # Create arrows between boxes
    prev_item = new_item

hcb = sb.HeaderContentBox("Header", "Content", x = -200, y = 400) # Create a multiline text box
circle = sb.Ellipse(200, 400, width=50, height=50, backgroundColor = 'red',
                    roughness=1) # Create a red circle in hand drawn style

sb.create_binding_arrows(prev_item, hcb, sb.DoubleArrow) # Create a double headed arrow
sb.create_binding_arrows(prev_item, circle, strokeColor = 'blue') # Create an blue arrow

sb.export_to_file('out.excalidraw')
```

## Documenation

### SketchBuilder

Every sketch starts by creating a sketch builder object.

```python
from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder() # Create a Sketch
```

Default settings for the sketch can be set using kwargs. For instance:

```python
from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder(roughness=2) # Create a hand drawn sketch
```

The list of configurable settings can be found in [defaults.py](Excalidraw_Interface/defaults.py)

### Exporting a Sketch

```python
from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder()
...
sb.export_to_file('my_sketch')
# OR
data = sb.export_to_json()
```

### Creating Sketch Objects

Rectangles, Diamonds, Ellipses can be created with a center_x and center_y position.
Width and height can also be set (defaults to 100). Other params can be set in kwargs.


```python
from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder()
sb.Rectangle(x = 0, y = 0)
sb.Diamond(x = 0, y = 0, width=50, height=20)
sb.Ellipse(x = 0, y = 0, backgroundColor='red')
```

Text, Lines, and Arrows have similar functions.

```python
from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder()
sb.Text('some text', x = 0, y = 0)
sb.Line((0,0), (100,100))
sb.Arrow((0,0), (100,100))
sb.DoubleArrow((0,0), (100,100))
```

TextBoxes and HeaderContentBoxes have special functions to create multiple objects at once.
Config can be passed to `txt_kwargs`, `rect_kwargs`, `header_kwargs`, or `content_kwargs`.

```python
from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder()
sb.TextBox('some text', x = 0, y = 0)
sb.HeaderContentBox('TITLE', 'content', x = 0, y = 0)
```

### Advanced Sketch Objects

To create arrows between two objects:

```python
from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder()
a = sb.TextBox('some text', x = 0, y = 0)
b = sb.TextBox('some text', x = 200, y = 200)
sb.create_binding_arrows(a, b)
sb.create_binding_arrows(a, b, sb.DoubleArrow, strokeColor='blue') #makes a blue double arrow
```

To create shape around an object (or Group):

```python
from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder()
a = sb.TextBox('some text', x = 0, y = 0)
outer_rect = sb.create_bounding_element(a)
```

To create groups:

```python
from Excalidraw_Interface import SketchBuilder, Group

sb = SketchBuilder()
a = sb.TextBox('some text', x = 0, y = 0)
b = sb.TextBox('some text', x = 200, y = 200)

g = Group([a, b])
```

For more examples see [advanced_groups.py](Excalidraw_Interface/examples/advanced_groups.py)

### Notes:

Groups can be nested.

A special feature exists that allows one element of a group to be treated as the whole group for the purpose of 
further grouping (useful for bounding boxes).

```
if first_is_group:
    elems[0].apply_recursive_groups.extend(elems[1:])
```