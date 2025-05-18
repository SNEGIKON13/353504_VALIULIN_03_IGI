# Module for drawing and filling shapes (Task 4)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as MplRect, Polygon

def draw_rectangle(rect, label):
    """
    Draw and fill a rectangle object, annotate with label.
    """
    fig, ax = plt.subplots()
    patch = MplRect(
        (0, 0),
        rect.width,
        rect.height,
        facecolor=rect.color_obj.color
    )
    ax.add_patch(patch)
    ax.set_xlim(-1, rect.width + 1)
    ax.set_ylim(-1, rect.height + 1)
    ax.set_aspect('equal', 'box')
    ax.text(
        rect.width / 2,
        rect.height / 2,
        label,
        ha='center',
        va='center'
    )
    plt.title(rect.shape_name)
    plt.show()


def draw_trapezoid(trap, label):
    """
    Draw and fill an isosceles trapezoid, annotate with label.
    """
    # compute coordinates
    a, b, h = trap.a, trap.b, trap.h
    dx = abs(b - a) / 2
    if b > a:
        verts = [(0, 0), (a, 0), (a + dx, h), (-dx, h)]
    else:
        verts = [(dx, 0), (dx + b, 0), (b, h), (0, h)]

    fig, ax = plt.subplots()
    poly = Polygon(verts, closed=True, facecolor=trap.color_obj.color)
    ax.add_patch(poly)
    xs, ys = zip(*verts)
    ax.set_xlim(min(xs) - 1, max(xs) + 1)
    ax.set_ylim(0, h + 1)
    ax.set_aspect('equal', 'box')
    ax.text(
        sum(xs) / 4,
        sum(ys) / 4,
        label,
        ha='center',
        va='center'
    )
    plt.title(trap.shape_name)
    plt.show()
