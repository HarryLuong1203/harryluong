import pygame
import sys
import random 


#Tạo cửa sổ game
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480


#tạo lưới, kích thước của mỗi ô caro, mỗi ô có kích thước 24 x 24
GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE 
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE


#dùng để lưu phương hướng của con rắn.
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)

# vẽ bàn caro lên cửa sổ của game
def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)



#class này tạo ra con rắn của mình. 
class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)

    #Tạo cái đầu cho nó - Vị trí đứng đầu
    def get_head_position(self):
        return self.positions[0]

    # Turn này hỗ trợ việc chuyển hướng của con rắn
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point


    #Move này điều khiển cách con rắn của chúng ta di chuyển.
    #Hàm này hoạt động bằng cách
    #tính toán vị trí tiếp theo của đầu rắn
    #nếu nó không trùng với vị trí của phần thân nào thì
    #sẽ được thêm vào rắn, đồng thời bỏ đi phần thân cuối, còn nếu trùng thì trò chơi sẽ bắt đầu lại.
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()            
            

    #Reset để bắt đầu lại trò chơi
    def reset(self):
        self.length = 1
        self.positions =  [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    

    #vẽ cái thân con rắn
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)


    #Sử lí thao tác của người chơi    
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

#Cái này tạo thức ăn cho rắn
class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (233, 163, 49)
        self.randomize_position()

    # randomize_position để những ô đồ ăn xuất hiện ngẫu nhiên trên bàn caro
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)


    # hàm này để vẽ thức ăn
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def main():#main chính
    #Cái đoạn này tạo một Clock để theo dõi thời gian và tạo một cửa sổ game.
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    drawGrid(surface) # Vẽ caro

    #Cái này tạo thức ăn
    snake = Snake()
    food = Food()
    
    myfont = pygame.font.SysFont("monospace", 16)
    
    score = 0 

    #while này tạo vòng lặp cho game - chạy game
    while True:
        clock.tick(10) #Ta sẽ quy định game chạy với tốc độ 10 khung hình 1 giây.
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position: #Nếu vị trí đầu rắn trùng với vị trí của thức ăn
                                    #ta tăng độ dài rắn lên một, đồng thời tạo ô thức ăn mới ngẫu nhiên
            snake.length += 1
            score += 1
            food.randomize_position()


        snake.draw(surface)#vẽ lại rắn
        food.draw(surface) #vẽ lại game


        # 4 dòng cuối này tạo một ô nhỏ để hiển thị điểm số
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(score), 1, (0,0,0))
        screen.blit(text, (5, 10))
        pygame.display.update()


main()#Khởi động game