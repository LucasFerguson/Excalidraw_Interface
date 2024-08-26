from Excalidraw_Interface import SketchBuilder, Group

sb = SketchBuilder()

tb_1 = sb.TextBox('Start Here', 0.5, 0.5)
tb_2 = sb.TextBox('End Here', 100, 100)

group_1 = Group([tb_1, tb_2])
bound_1 = sb.create_bounding_element(group_1)

hcb = sb.HeaderContentBox('Header', 'Some Extremely Long Content', 200, 200)

group_2 = Group([bound_1, hcb])
sb.create_bounding_element(group_2, strokeColor="#FF0000",)

sb.export_to_file('out.excalidraw')