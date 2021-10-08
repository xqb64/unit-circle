import math
import tkinter as tk

RADIUS = 1
SCALE = 150

EXTRA_PIXELS = 30

DRAGGABLE_CIRCLE_SCALE = 20

root = tk.Tk()

canvas = tk.Canvas(
    root,
    width=(2*RADIUS*SCALE)+EXTRA_PIXELS*2,
    height=(2*RADIUS*SCALE)+EXTRA_PIXELS*2,
    background='white'
)
canvas.pack()

# unit circle
canvas.create_oval(
    EXTRA_PIXELS, EXTRA_PIXELS,
    (2 * RADIUS) * SCALE + EXTRA_PIXELS, (2 * RADIUS) * SCALE + EXTRA_PIXELS,
)

# small circle
canvas.create_oval(
    EXTRA_PIXELS + RADIUS * SCALE - DRAGGABLE_CIRCLE_SCALE / 2,
    EXTRA_PIXELS - DRAGGABLE_CIRCLE_SCALE / 2,
    EXTRA_PIXELS + RADIUS * SCALE + DRAGGABLE_CIRCLE_SCALE / 2,
    EXTRA_PIXELS + DRAGGABLE_CIRCLE_SCALE / 2,
    fill='blue', width=2, tags=['draggable']
)

# sin text
canvas.create_text(
    (EXTRA_PIXELS * 2 + 2 * RADIUS * SCALE) / 6,
    EXTRA_PIXELS + 2 * RADIUS * SCALE + EXTRA_PIXELS / 2,
    text='sin = 1', tags=['sin'], fill='blue'
)

# cos text
canvas.create_text(
    ((EXTRA_PIXELS * 2 + 2 * RADIUS * SCALE) / 6) * 3,
    EXTRA_PIXELS + 2 * RADIUS * SCALE + EXTRA_PIXELS / 2,
    text='cos = 0', tags=['cos'], fill='red'
)

# angle
canvas.create_text(
    ((EXTRA_PIXELS * 2 + 2 * RADIUS * SCALE) / 6) * 5,
    EXTRA_PIXELS + 2 * RADIUS * SCALE + EXTRA_PIXELS / 2,
    text='angle = 1.57', tags=['angle'], fill='green'
)

def math2canvas(x, y):
    return (
        SCALE * x + (RADIUS * SCALE + EXTRA_PIXELS),
        SCALE * -y + (RADIUS * SCALE + EXTRA_PIXELS)
    )

def canvas2math(x, y):
    return (
        (x - (RADIUS * SCALE + EXTRA_PIXELS)) / SCALE,
        (y - (RADIUS * SCALE + EXTRA_PIXELS)) / -SCALE
    )

# horizontal diameter line
canvas.create_line(
    *math2canvas(-1, 0),
    *math2canvas(1, 0)
)

# vertical diameter line
canvas.create_line(
    *math2canvas(0, 1),
    *math2canvas(0, -1)
)

# sin line
canvas.create_line(
    *math2canvas(0, 0),
    *math2canvas(0, 1),
    tags=['sin']
)

def on_drag(event, canvas):
    math_x, math_y = canvas2math(event.x, event.y)
    angle = math.atan2(math_y, math_x)
    canvas_x, canvas_y = math2canvas(math.cos(angle), math.sin(angle))
    canvas.delete('sin')
    canvas.create_line(
        canvas_x, canvas_y,
        canvas_x, math2canvas(1, 0)[1],
        tags=['sin'], fill='blue'
    )
    canvas.create_text(
        (EXTRA_PIXELS * 2 + 2 * RADIUS * SCALE) / 6,
        EXTRA_PIXELS + 2 * RADIUS * SCALE + EXTRA_PIXELS / 2,
        text=f'sin = {round(math.sin(angle), 2)}', tags=['sin'], fill='blue'
    )
    canvas.delete('cos')
    canvas.create_line(
        math2canvas(0, 1)[0], canvas_y,
        canvas_x, canvas_y,
        tags=['cos'], fill='red'
    )
    canvas.create_text(
        ((EXTRA_PIXELS * 2 + 2 * RADIUS * SCALE) / 6) * 3,
        EXTRA_PIXELS + 2 * RADIUS * SCALE + EXTRA_PIXELS / 2,
        text=f'cos = {round(math.cos(angle), 2)}', tags=['cos'], fill='red'
    )
    canvas.delete('angle')
    canvas.create_line(
        *math2canvas(0, 0),
        canvas_x, canvas_y,
        fill='green', tags=['angle']
    )
    canvas.create_text(
        ((EXTRA_PIXELS * 2 + 2 * RADIUS * SCALE) / 6) * 5,
        EXTRA_PIXELS + 2 * RADIUS * SCALE + EXTRA_PIXELS / 2,
        text=f'angle = {round(angle, 2)}', tags=['angle'], fill='green'
    )
    canvas.tk.call(
        str(canvas),
        'moveto',
        'draggable',
        canvas_x - DRAGGABLE_CIRCLE_SCALE / 2,
        canvas_y - DRAGGABLE_CIRCLE_SCALE / 2
    )

canvas.tag_bind(
    'draggable',
    '<Button1-Motion>',
    lambda event, x=canvas: on_drag(event, x)
)

root.mainloop()