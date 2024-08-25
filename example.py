from Excalidraw_Interface import SketchBuilder

sb = SketchBuilder()

sb.Arrow((0,0), (100,100))
sb.Arrow((200,200), (100,100))

sb.export_to_file('out.excalidraw')