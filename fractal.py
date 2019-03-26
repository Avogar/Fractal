import pygame, random, math
pygame.init()

def get_points(n,R,l,p):
    points = []
    angle = 2*math.pi/n
    if n%2 == 0 and p == 1 or n%2 != 0 and p == -1:
        b = angle/2
    else:
        b = 0
    for i in range(n):
        y = int(l - R*math.cos(b))
        x = int(size[0]//2 - R*math.sin(b))
        points.append([x,y])
        b += angle
    return points

def get_new_R(R,n):
    angle = 2*math.pi/n
    r = R*math.sin(angle/2)/(1 + math.sin(angle/2))
    q = (R - r)*math.cos(angle/2)
    a = (1-math.sin(angle/2)**2)/math.sin(angle/2)**2
    b = r + q/math.sin(angle/2)
    c = q**2
    return (b-(b**2-a*c)**0.5)*(1+math.sin(angle/2))/(math.sin(angle/2)*a)

def get_k(n):
    angle = 2*math.pi/n
    return math.sin(angle/2)**-1

def get_r(size,n,p):
    a = 2*math.pi / n
    if n % 2 == 0:
        if p == 1:
            R = size[1] / (2 * math.cos(a / 2))
        else:
            R = size[1]/2
        l = size[1] / 2
    else:
        R = size[1] / (1 + math.cos(a / 2))
        l = size[1]/2 + R*(1 - math.cos(a/2))/2

    return R, l

def create_point(n):
    xy = []
    for i in range(n):
        xy.append([random.randrange(300, 701), random.randrange(200, 401)])
    return xy

def move_point(xy,point,k):
    for j in range(len(xy)):
        i = random.randrange(0, n)
        xy[j][0] = int((point[i][0] * k + xy[j][0]) / (k + 1))
        xy[j][1] = int((point[i][1] * k + xy[j][1]) / (k + 1))
    return xy

def draw_point(xy):
    for i in range(len(xy)):
        j = random.randrange(len(color))
        pygame.draw.circle(screen, color[j], xy[i], 0)

def turn(point):
    for elem in point:
        elem[1] = size[1] - elem[1]
    return point

def new(n):
    p = 1
    N = 200
    R, l = get_r(size, n, p)
    count = 1
    point = []
    R_list = [R]
    n_ = 0
    while 2*R_list[n_]*math.sin(math.pi/n) >= 1:
        R, l = get_r(size, n, p)
        point.append(get_points(n, R_list[n_], l,p))
        R_list.append(get_new_R(R_list[n_], n))
        p *= -1
        n_ += 1
    k = get_k(n)
    xy = []
    N_ = N
    for i in range(n_):
        if i == 0:
            t = 1
        else:
            t = R_list[i] / R_list[i - 1]
        N_ = int(N_ * t)
        xy.append(create_point(N_))
    return point, k, count, xy, n_


black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
grey = (190,190,190)
orange = (255,165,0)
brown = (139,69,19)
purple = (160,32,240)
DarkGreen = (0,128,0)
color = [white,green,red,blue,yellow,cyan,green,orange,brown,purple,DarkGreen]
size = [950, 750]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = True
stop = False
screen.fill(black)
n = 3
point, k, count, xy, n_ = new(n)
k = get_k(n)

while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                stop = False
                n += 1
                point, k, count, xy, n_ = new(n)
                screen.fill(black)

            if event.key == pygame.K_LEFT and n >= 4:
                stop = False
                n -= 1
                point, k, count, xy, n_ = new(n)
                screen.fill(black)
            if event.key ==  pygame.K_SPACE:
                if stop:
                    stop = False
                else:
                    stop = True

    if not(stop):
        if count >= 300:
            n += 1
            point, k, count, xy, n_ = new(n)
            screen.fill(black)

        if count >= 10:
            for i in range(n_):
                draw_point(xy[i])
        count += 1
        for i in range(n_):
            xy[i] = move_point(xy[i],point[i],k)

        pygame.display.flip()
    clock.tick(100)
pygame.quit()
