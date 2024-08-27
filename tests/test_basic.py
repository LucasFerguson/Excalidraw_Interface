from Excalidraw_Interface import SketchBuilder, Group
import pytest
import json
import os

directory = os.path.dirname(__file__)

def _compare_json(obja, objb, ignore_keys, src_path):
    if isinstance(obja, dict):
        if not isinstance(objb, dict):
            raise Exception(f"Type mismatch. <{src_path}>")

        for key, value in obja.items():
            if key in ignore_keys:
                continue
            if key not in objb:
                raise Exception(f"Missing key {key} from objb. <{src_path}>")
            _compare_json(value, objb[key], ignore_keys, src_path = src_path + '.' + key)
        for key in objb:
            if key not in obja:
                raise Exception(f"Missing key {key} from obja. <{src_path}>")

    elif isinstance(obja, list):
        if not isinstance(objb, list):
            raise Exception(f"Type mismatch. <{src_path}>")

        if len(obja) != len(objb):
            raise Exception(f"Length mismatch. <{src_path}>")

        for index, (obja_item, objb_item) in enumerate(zip(obja, objb)):
            _compare_json(obja_item, objb_item, ignore_keys, src_path + '.' + str(index))

    else:
        if obja != objb:
            raise Exception(f"Item <{obja}> does not match <{objb}>. <{src_path}>")

def test_flowchart_example():
    flowchart_items = ['First Step', 'Second Step', 'Third Step']

    sb = SketchBuilder() # Create a Sketch

    prev_item = sb.TextBox("Start Here", x=0, y=0)  # Create a Text Box
    for index, item in enumerate(flowchart_items):
        new_item = sb.TextBox(item, x=0, y=(index + 1) * 150)  # Create a Text Box
        sb.create_binding_arrows(prev_item, new_item)  # Create arrows between boxes
        prev_item = new_item

    hcb = sb.HeaderContentBox("Header", "Content", x=-200, y=400,
                              header_kwargs={'strokeColor': 'blue'})  # Create a multiline text box
    circle = sb.Ellipse(200, 400, width=50, height=50, backgroundColor='red',
                        roughness=1)  # Create a red circle in hand drawn style

    sb.create_binding_arrows(prev_item, hcb, sb.DoubleArrow)  # Create a double headed arrow
    sb.create_binding_arrows(prev_item, circle, strokeColor='blue')  # Create an blue arrow
    sb.export_to_file('test_flowchart_example.excalidraw')

    a = sb.export_to_json()
    with open(directory + '/_flowchart_example.excalidraw') as f:
        b = json.load(f)

    _compare_json(a, b, ['id', 'seed', 'groupIds', 'elementId'], '')

    with open('test_flowchart_example.excalidraw'): #check that file exists
        pass


def test_other_elems():
    sb = SketchBuilder(roughness=2)  # Create a Sketch
    sb.Diamond(0, 0)
    line = sb.Line((0,0), (15,15))
    bound_elem = sb.create_bounding_element(line, sb.Ellipse)
    sb.create_bounding_element(bound_elem)
    sb.export_to_file('test_other_elem_example')

    a = sb.export_to_json()
    with open(directory + '/_other_elem_example.excalidraw') as f:
        b = json.load(f)

    _compare_json(a, b, ['id', 'seed', 'groupIds', 'elementId'], '')

    with open('test_other_elem_example.excalidraw'): #check that file exists
        pass

def test_errors():
    sb = SketchBuilder()  # Create a Sketch
    with pytest.raises(Exception, match="Key <someKey> not used."):
        SketchBuilder(someKey='value')

    with pytest.raises(Exception, match="Unexpected key for shape diamond: someKey"):
        sb.Diamond(0, 0, someKey='value')

    with pytest.raises(Exception, match="Group should not be exported - a group was incorrectly added to sketch."):
        sb.add_element(Group([sb.Rectangle(0,0)]))
        sb.export_to_json()

def test_examples():
    # noinspection PyUnresolvedReferences
    import Excalidraw_Interface.examples.flowchart
    # noinspection PyUnresolvedReferences
    import Excalidraw_Interface.examples.advanced_groups

def test_internal_comparison():
    with pytest.raises(Exception, match="Type mismatch. <>"):
        _compare_json({}, [], [], '')

    with pytest.raises(Exception, match="Type mismatch. <>"):
        _compare_json([], {}, [], '')

    with pytest.raises(Exception, match="Item <a> does not match <b>. <>"):
        _compare_json('a', 'b', [], '')

    with pytest.raises(Exception, match="Length mismatch. <>"):
        _compare_json([1], [], [], '')

    with pytest.raises(Exception, match="Missing key a from objb. <>"):
        _compare_json({'a': 'a'}, {}, [], '')

    with pytest.raises(Exception, match="Missing key a from obja. <>"):
        _compare_json({}, {'a': 'a'}, [], '')
