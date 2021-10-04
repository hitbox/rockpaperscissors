from itertools import tee

def layout_flow(rects, width, betweenx=0, betweeny=0):
    """
    move rects, in-place, from left-to-right and top-to-bottom breaking
    "newlines" when `width` is exceeded.
    """
    a, b, c = tee(rects, 3)
    top = min(rect.top for rect in a)
    left = min(rect.left for rect in b)
    rowsize = max(rect.height for rect in c) + betweeny
    for r1, r2 in pairwise(rects):
        r2.top = top
        r2.left = r1.right + betweenx
        if r2.right > width:
            top += rowsize + betweeny
            r2.top = top
            r2.left = left
