from Excalidraw_Interface import SketchBuilder, Group
import pytest

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
    sb.export_to_json() #TODO - verify output

def test_other_elems():
    sb = SketchBuilder(roughness=2)  # Create a Sketch
    sb.Diamond(0, 0)
    line = sb.Line((0,0), (15,15))
    bound_elem = sb.create_bounding_element(line, sb.Ellipse)
    sb.create_bounding_element(bound_elem)
    sb.export_to_json()  # TODO - verify output

    sb = SketchBuilder()  # Create a Sketch

def test_errors():
    sb = SketchBuilder()  # Create a Sketch
    with pytest.raises(Exception, match="Key <someKey> not used."):
        SketchBuilder(someKey='value')

    with pytest.raises(Exception, match="Unexpected key for shape diamond: someKey"):
        sb.Diamond(0, 0, someKey='value')

    with pytest.raises(Exception, match="Group should not be exported - a group was incorrectly added to sketch."):
        sb.add_element(Group([sb.Rectangle(0,0)]))
        sb.export_to_json()