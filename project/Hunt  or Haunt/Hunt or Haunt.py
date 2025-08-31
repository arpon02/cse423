from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random
import math

#globl variables :
tile_size = 100
grid_size = 8

quad = None

player_tile_x = 3
player_tile_y = 3
player_dir = 0
player_pos = (0, 0, 0)




dir_delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]

items = {}


def init_game():
    global player_tile_x, player_tile_y, player_pos
    player_tile_x = 3
    player_tile_y = 3
    player_dir = 0
    player_pos = tile_center(player_tile_x, player_tile_y)
    

    #tiems generaion:
    tiles = [(i, j) for i in range(grid_size) for j in range(grid_size)]
    random.shuffle(tiles)
    items = {}
    for k in range(30):
        items[tiles[k]] = 'treasure'
    for k in range(30, 45):
        items[tiles[k]] = 'fruit'
    for k in range(45, 55):
        items[tiles[k]] = 'mushroom'

    #obstacle over item tiles
    item_tiles = list(items.keys())
    random.shuffle(item_tiles)
    obstacles = {}
    for k in range(3):
        obstacles[item_tiles[k]] = 'bush'
    for k in range(3, 6):
        obstacles[item_tiles[k]] = 'boulder'

def tile_center(i, j):
    return (-350 + i * tile_size, -350 + j * tile_size, 0)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    glBegin(GL_QUADS)
    for i in range(-1, 9):
        for j in range(-1, 9):
            left = -500 + (i + 1) * tile_size
            bottom = -500 + (j + 1) * tile_size
            right = left + tile_size
            top = bottom + tile_size
            if 0 <= i < 8 and 0 <= j < 8:
                t = (i, j)
                if t in dug:
                    glColor3f(0.5, 0.5, 0.5)
                else:
                    if (i + j) % 2 == 0:
                        glColor3f(0.2, 0.8, 0.2)
                    else:
                        glColor3f(0.5, 0.5, 0.3)
            else:
                glColor3f(1.0, 1.0, 1.0)
            glVertex3f(left, bottom, 0)
            glVertex3f(right, bottom, 0)
            glVertex3f(right, top, 0)
            glVertex3f(left, top, 0)
    glEnd()

def draw_player():
    current_time = time.time()
    if invisible_start > 0 and current_time - invisible_start < 5:
        #blink:
        if ((current_time - invisible_start) % 1.25) < 0.625:
            return ##invisible
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 0)
    glRotatef(-player_dir * 90, 0, 0, 1)
    ##legs:
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(-10, 0, 0)
    gluCylinder(quad, 10, 10, 40, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(10, 0, 0)
    gluCylinder(quad, 10, 10, 40, 10, 10)
    glPopMatrix()
    #body:
    glPushMatrix()
    glTranslatef(0, 0, 70)
    glColor3f(0, 0, 1)
    glScalef(1, 0.5, 1.5)
    glutSolidCube(40)
    glPopMatrix()
    ###hands
    glColor3f(1.0, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(-15, 20, 90)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 8, 8, 30, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(15, 20, 90)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 8, 8, 30, 10, 10)
    glPopMatrix()
    #grayhand:
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(0, 20, 90)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 8, 8, 30, 10, 10)
    glPopMatrix()
    #head:
    if blink_start > 0 and current_time - blink_start < 0.5:
        glColor3f(*blink_color)
    else:
        glColor3f(0, 0, 0)
    glTranslatef(0, 0, 120)
    gluSphere(quad, 20, 10, 10)
    glPopMatrix()



def draw_red_dot():
    dx, dy = dir_delta[player_dir]
    fx = player_tile_x + dx
    fy = player_tile_y + dy
    if 0 <= fx < 8 and 0 <= fy < 8:
        pos = tile_center(fx, fy)
        glPushMatrix()
        glTranslatef(pos[0], pos[1], 5)
        glColor3f(1, 0, 0)
        gluSphere(quad, 5, 10, 10)
        glPopMatrix()

def draw_obstacles_and_items():
    current_time = time.time()
    for t in obstacles:
        if t not in removed:
            pos = tile_center(t[0], t[1])
            glPushMatrix()
            glTranslatef(pos[0], pos[1], 20)
            if obstacles[t] == 'bush':
                glColor3f(0, 0.5, 0)
            else:
                glColor3f(0.5, 0.5, 0.5)
            gluSphere(quad, 30, 10, 10)
            glPopMatrix()
    for t in dug:
        if current_time - dug[t] < 3 and t in items:
            pos = tile_center(t[0], t[1])
            glPushMatrix()
            glTranslatef(pos[0], pos[1], 10)
            item = items[t]
            if item == 'treasure':
                glColor3f(1, 1, 0)
            elif item == 'fruit':
                glColor3f(1, 0.5, 0)
            elif item == 'mushroom':
                glColor3f(1, 0, 1)
            gluSphere(quad, 15, 10, 10)
            glPopMatrix()
    if scan_start > 0 and current_time - scan_start < 1:
        for t in items:
            if items[t] == 'treasure' and t not in dug:
                dist = abs(t[0] - player_tile_x) + abs(t[1] - player_tile_y)
                if dist <= 2:
                    pos = tile_center(t[0], t[1])
                    glPushMatrix()
                    glTranslatef(pos[0], pos[1], 10)
                    glColor3f(1, 1, 0)
                    gluSphere(quad, 15, 10, 10)
                    glPopMatrix()


def idle():
    current_time = time.time()
    global last_time
    if 'last_time' not in globals():
        last_time = current_time
    delta = current_time - last_time
    last_time = current_time
    update_bear(delta)
    glutPostRedisplay()



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_grid()
    draw_player()
    
    glClear(GL_DEPTH_BUFFER_BIT)
    draw_red_dot()
    
    glutSwapBuffers()

def main():
    global quad, last_time
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Hunt or Haunt!")
    glutDisplayFunc(showScreen)
    
    glutIdleFunc(idle)
    quad = gluNewQuadric()
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)
    init_game()
    last_time = time.time()
    glutMainLoop()

if __name__ == "__main__":
    main()
