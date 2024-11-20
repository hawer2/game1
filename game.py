Web VPython 3.2

from vpython import *
from random import uniform

# 캐릭터
body = box(pos=vector(0, 10, 0), size=vec(0.5, 0.5, 0.5), color=color.red)
leg1 = box(pos=vector(0.5, 9.7, 0), size=vec(0.2, 0.3, 0.2), color=color.red)
leg2 = box(pos=vector(-0.5, 9.7, 0), size=vec(0.2, 0.3, 0.2), color=color.red)
leg3 = box(pos=vector(0.3, 9.2, 0), size=vec(0.2, 0.3, 0.2), color=color.blue)
leg4 = box(pos=vector(-0.3, 9.2, 0), size=vec(0.2, 0.3, 0.2), color=color.blue)
myball = compound([body, leg1, leg2, leg3, leg4])

# 바닥
ground = box(pos=vec(0, 0, 0), size=vec(10, 0.1, 30000), color=vec(0.5, 0.5, 0.5))

# 초기 속도 및 변수
myball.velocity = vector(0, 0, 0)
speed = -0.5
dt = 0.01
dx = 0.2
jump_velocity = 21
gravity = -60
on_ground = True

# 장애물 생성
obstacles = []
num_obstacles = 200

# 장애물 추가
for _ in range(num_obstacles):
    x_pos = uniform(-5, 5)
    y_pos = uniform(0.1, 3)
    z_pos = uniform(-50, -3000)
    x_size = uniform(2, 5)
    z_size = uniform(3, 5)
    obstacles.append(box(pos=vector(x_pos, y_pos, z_pos), size=vec(x_size, 3, z_size), color=color.white))

# 게임 오버 메시지 표시
def show_game_over(score):
    message = label(pos=scene.center, text='GAME OVER', color=color.red, height=30, box=False, opacity=0)
    score_label = label(pos=vector(scene.center.x, scene.center.y + 4, scene.center.z), text=f"Final Score: {score:.2f}", color=color.white, height=20, box=False, opacity=0)
    t = 0
    while t < 0.3:
        rate(100)
        t += dt
    message.visible = False
    score_label.visible = False

# 게임 초기화
def reset_game():
    global myball, on_ground, score
    myball.pos = vector(0, 10, 0)
    myball.velocity = vector(0, 0, 0)
    on_ground = True
    score = 0

# 충돌 감지
def check_collision():
    global myball
    for obstacle in obstacles:
        dist_x = abs(myball.pos.x - obstacle.pos.x)
        dist_y = abs(myball.pos.y - obstacle.pos.y)
        dist_z = abs(myball.pos.z - obstacle.pos.z)
        if dist_x < (obstacle.size.x / 2 + 0.5) and dist_y < (obstacle.size.y / 2 + 0.5) and dist_z < (obstacle.size.z / 2 + 0.25):
            return True
    return False

# 점수 초기화
score = 0
score_label = label(pos=vector(scene.center.x, scene.center.y + 2, scene.center.z), text=f"Score: {score:.2f}", color=color.white, height=20, box=False, opacity=0)

while True:
    rate(100)
    score += dt
    myball.pos.z += speed

    # 키 입력 처리
    keys = keysdown()
    if 'left' in keys:
        myball.pos.x -= dx
    if 'right' in keys:
        myball.pos.x += dx

    # 캐릭터가 길 밖으로 나가면 떨어지게 설정
    if myball.pos.x < -5 or myball.pos.x > 5:
        on_ground = False

    if 'up' in keys and on_ground:
        myball.velocity.y = jump_velocity
        on_ground = False

    # 중력 반영
    myball.velocity.y += gravity * dt
    myball.pos.y += myball.velocity.y * dt

    # 캐릭터가 땅에 닿으면 속도와 위치 조정
    if myball.pos.y <= 0.5 and -5 <= myball.pos.x <= 5:
        myball.pos.y = 0.5
        myball.velocity.y = 0
        on_ground = True
    elif myball.pos.y <= 0.5:
        on_ground = False 

    # Y축 기준 아래로 떨어지면 게임 오버
    if myball.pos.y < -3:
        show_game_over(score)
        reset_game()
        continue

    # 장애물과 충돌 체크
    if check_collision():
        show_game_over(score)
        reset_game()
        continue

    score_label.pos = vector(myball.pos.x, myball.pos.y + 7, myball.pos.z - 10)
    score_label.text = f"Score: {score:.2f}"

    scene.camera.pos = vector(myball.pos.x, myball.pos.y + 3, myball.pos.z + 10)
    scene.camera.axis = vector(0, -2, -10)

# 죽을 때마다 장애물 변경

# 최고점수 화면에 계속 띄우기

# 

 



