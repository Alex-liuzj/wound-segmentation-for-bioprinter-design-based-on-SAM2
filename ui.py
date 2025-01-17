import PySimpleGUI as psg
from PIL import Image, ImageTk

def ui_init(wound_img):
    size = (500, 500)
    img = wound_img
    #print the size of the image
    original_size = img.size

    img = img.resize(size, resample=Image.BICUBIC)
    #save the img in the directory 
    img.save('./img/wound_resized.png')

    layout = [
        [psg.Graph(
        canvas_size=(500, 500),
        graph_bottom_left=(0, 0),
        graph_top_right=(500, 500),
        key="-GRAPH-",
        change_submits=True,  # mouse click events
        background_color='lightblue',
        drag_submits=False), ],
        #[psg.Image(key="-IMAGE-", size=(500,500))],
        [psg.Button('Submit'), psg.Button('Exit')]
    ]

    window = psg.Window('Wound Segmentation for Bioprinter', layout, finalize=True)

    graph = window["-GRAPH-"]  # type: sg.Graph

    graph.draw_image('./img/wound_resized.png', location=(0,500))

    dragging = False
    prior_point = None

    x=y=0 

    while True:
        event, values = window.read()

        if event == psg.WIN_CLOSED or event == 'Exit':
            break
        if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse

            if prior_point:
                graph.delete_figure(prior_point)

            x, y = values["-GRAPH-"]
            #show a point where the user clicked
            point=graph.draw_point((x, y), size=10, color='green')

            prior_point = point

        if event == 'Submit':
            print(x,y)
            window.close()
    window.close()

    #convert the coordinates to the original size
    x = int(x * original_size[0] / size[0])
    y = int(original_size[1] - y * original_size[1] / size[1])
    print(x,y)
    return x, y

#ui_init()

