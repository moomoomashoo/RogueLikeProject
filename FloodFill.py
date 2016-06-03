def flood_fill(lev, w, h, x, y, oldChar, newChar):
    
    if lev[x][y] != oldChar:
        return
    
    lev[x][y] = newChar
    
    if x > 0:
        flood_fill(lev, w, h, x-1, y, oldChar, newChar)
    if y > 0:
        flood_fill(lev, w, h, x, y-1, oldChar, newChar)
    if x < w-1:
        flood_fill(lev, w, h, x+1, y, oldChar, newChar)
    if y < h-1:
        flood_fill(lev, w, h, x, y+1, oldChar, newChar)