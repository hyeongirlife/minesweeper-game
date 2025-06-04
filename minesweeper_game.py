import pygame
import random
import time
import sys
import math

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
MAROON = (128, 0, 0)
TURQUOISE = (64, 224, 208)
DARK_BLUE = (0, 0, 128)
DARK_GREEN = (0, 100, 0)

class Explosion:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.radius = 5
        self.max_radius = size * 2
        self.growing = True
        self.particles = []
        self.create_particles()
        
    def create_particles(self):
        num_particles = 20
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            size = random.randint(2, 8)
            color_idx = random.randint(0, 2)
            color = [RED, ORANGE, YELLOW][color_idx]
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': size,
                'color': color,
                'life': random.uniform(0.5, 1.0)
            })
    
    def update(self):
        # 원형 폭발 효과 업데이트
        if self.growing:
            self.radius += 3
            if self.radius >= self.max_radius:
                self.growing = False
        else:
            self.radius -= 2
            
        # 파티클 업데이트
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.02
            if p['life'] <= 0:
                self.particles.remove(p)
                
        return self.radius > 0 or len(self.particles) > 0
    
    def draw(self, screen):
        # 원형 폭발 효과 그리기
        if self.radius > 0:
            alpha = int(255 * (self.radius / self.max_radius))
            if not self.growing:
                alpha = int(255 * (self.radius / self.max_radius))
            
            s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 100, 0, alpha), (self.radius, self.radius), self.radius)
            screen.blit(s, (self.x - self.radius, self.y - self.radius))
        
        # 파티클 그리기
        for p in self.particles:
            alpha = int(255 * p['life'])
            color = list(p['color'])
            color.append(alpha)
            s = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (p['size'], p['size']), p['size'])
            screen.blit(s, (p['x'] - p['size'], p['y'] - p['size']))

class Minesweeper:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("지뢰 찾기")
        
        # 폰트 초기화
        pygame.font.init()
        
        # macOS에서 한글 지원 폰트 시도
        try:
            # macOS 한글 폰트 경로
            font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
            self.font = pygame.font.Font(font_path, 20)
            self.small_font = pygame.font.Font(font_path, 16)
            self.large_font = pygame.font.Font(font_path, 30)
        except:
            try:
                # 시스템 한글 폰트 시도
                self.font = pygame.font.SysFont('AppleGothic', 20)
                self.small_font = pygame.font.SysFont('AppleGothic', 16)
                self.large_font = pygame.font.SysFont('AppleGothic', 30)
            except:
                # 기본 폰트로 대체
                self.font = pygame.font.SysFont('Arial', 20)
                self.small_font = pygame.font.SysFont('Arial', 16)
                self.large_font = pygame.font.SysFont('Arial', 30)
        
        # 게임 설정
        self.difficulty_levels = {
            "초급": {"width": 9, "height": 9, "mines": 10, "cell_size": 40},
            "중급": {"width": 16, "height": 16, "mines": 40, "cell_size": 30},
            "고급": {"width": 30, "height": 16, "mines": 99, "cell_size": 30}
        }
        
        self.current_difficulty = "초급"
        self.set_difficulty(self.current_difficulty)
        
        # 게임 상태
        self.game_over = False
        self.first_click = True
        self.start_time = 0
        self.elapsed_time = 0
        self.mines_left = self.mines
        
        # 폭발 효과
        self.explosion = None
        self.show_restart_modal = False
        
        # 이미지 로드
        self.load_images()
        
        # 게임 초기화
        self.initialize_game()
        
        # 메인 루프
        self.main_loop()
    
    def set_difficulty(self, level):
        self.current_difficulty = level
        self.width = self.difficulty_levels[level]["width"]
        self.height = self.difficulty_levels[level]["height"]
        self.mines = self.difficulty_levels[level]["mines"]
        self.cell_size = self.difficulty_levels[level]["cell_size"]
        
        # 화면 크기 계산
        self.top_height = 60  # 상단 정보 표시 영역 높이
        self.screen_width = self.width * self.cell_size
        self.screen_height = self.height * self.cell_size + self.top_height
        
        # 화면이 너무 크면 최대 크기 제한
        max_width = 900
        if self.screen_width > max_width:
            self.screen_width = max_width
            self.cell_size = max_width // self.width
            self.screen_height = self.height * self.cell_size + self.top_height
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    
    def load_images(self):
        # 이모지 대신 텍스트 사용
        self.images = {
            'flag': self.font.render('🚩', True, RED),
            'mine': self.font.render('💣', True, BLACK),
            'explosion': self.font.render('💥', True, RED),
            'wrong': self.font.render('❌', True, RED),
            'smile': self.font.render('😊', True, BLACK),
            'sad': self.font.render('😵', True, BLACK),
            'cool': self.font.render('😎', True, BLACK)
        }
    
    def initialize_game(self):
        # 게임 보드 초기화
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.flags = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        # 게임 상태 초기화
        self.game_over = False
        self.first_click = True
        self.start_time = 0
        self.elapsed_time = 0
        self.mines_left = self.mines
        self.face_button = 'smile'
        self.explosion = None
        self.show_restart_modal = False
    
    def place_mines(self, first_row, first_col):
        # 첫 번째 클릭 위치와 주변에는 지뢰를 배치하지 않음
        safe_cells = []
        for i in range(max(0, first_row-1), min(self.height, first_row+2)):
            for j in range(max(0, first_col-1), min(self.width, first_col+2)):
                safe_cells.append((i, j))
        
        # 지뢰 배치
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            if (row, col) not in safe_cells and self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1
        
        # 숫자 계산 (주변 지뢰 수)
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] != -1:
                    self.board[i][j] = self.count_adjacent_mines(i, j)
    
    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(max(0, row-1), min(self.height, row+2)):
            for j in range(max(0, col-1), min(self.width, col+2)):
                if self.board[i][j] == -1:
                    count += 1
        return count
    
    def draw_board(self):
        # 배경 그리기
        self.screen.fill(GRAY)
        
        # 상단 정보 영역 그리기
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, self.screen_width, self.top_height))
        
        # 지뢰 카운터 표시
        mines_text = self.font.render(f"지뢰: {self.mines_left}", True, WHITE)
        self.screen.blit(mines_text, (10, 20))
        
        # 타이머 표시
        timer_text = self.font.render(f"시간: {self.elapsed_time}", True, WHITE)
        timer_rect = timer_text.get_rect()
        timer_rect.midtop = (self.screen_width // 2, 20)
        self.screen.blit(timer_text, timer_rect)
        
        # 제작자 정보 표시
        creator_text = self.small_font.render("Made by hyeongeol", True, WHITE)
        creator_rect = creator_text.get_rect()
        creator_rect.topright = (self.screen_width - 10, 10)
        self.screen.blit(creator_text, creator_rect)
        
        # 재시작 버튼 (이모티콘)
        face_rect = self.images[self.face_button].get_rect()
        face_rect.midtop = (self.screen_width // 2, 45)
        self.screen.blit(self.images[self.face_button], face_rect)
        
        # 게임 보드 그리기
        for row in range(self.height):
            for col in range(self.width):
                x = col * self.cell_size
                y = row * self.cell_size + self.top_height
                
                # 셀 테두리
                pygame.draw.rect(self.screen, DARK_GRAY, (x, y, self.cell_size, self.cell_size), 1)
                
                if self.revealed[row][col]:
                    # 열린 셀
                    pygame.draw.rect(self.screen, WHITE, (x+1, y+1, self.cell_size-2, self.cell_size-2))
                    
                    # 지뢰인 경우
                    if self.board[row][col] == -1:
                        if self.game_over:
                            # 게임 오버 시 폭발한 지뢰
                            pygame.draw.rect(self.screen, RED, (x+1, y+1, self.cell_size-2, self.cell_size-2))
                            mine_rect = self.images['explosion'].get_rect()
                            mine_rect.center = (x + self.cell_size // 2, y + self.cell_size // 2)
                            self.screen.blit(self.images['explosion'], mine_rect)
                    
                    # 숫자인 경우
                    elif self.board[row][col] > 0:
                        # 숫자에 따른 색상
                        colors = [BLUE, GREEN, RED, PURPLE, MAROON, TURQUOISE, BLACK, DARK_GRAY]
                        number_text = self.font.render(str(self.board[row][col]), True, colors[self.board[row][col]-1])
                        number_rect = number_text.get_rect()
                        number_rect.center = (x + self.cell_size // 2, y + self.cell_size // 2)
                        self.screen.blit(number_text, number_rect)
                
                else:
                    # 닫힌 셀
                    pygame.draw.rect(self.screen, GRAY, (x+1, y+1, self.cell_size-2, self.cell_size-2))
                    
                    # 깃발이 있는 경우
                    if self.flags[row][col]:
                        flag_rect = self.images['flag'].get_rect()
                        flag_rect.center = (x + self.cell_size // 2, y + self.cell_size // 2)
                        self.screen.blit(self.images['flag'], flag_rect)
                    
                    # 게임 오버 시 잘못된 깃발 표시
                    if self.game_over and self.flags[row][col] and self.board[row][col] != -1:
                        wrong_rect = self.images['wrong'].get_rect()
                        wrong_rect.center = (x + self.cell_size // 2, y + self.cell_size // 2)
                        self.screen.blit(self.images['wrong'], wrong_rect)
                    
                    # 게임 오버 시 지뢰 표시
                    if self.game_over and self.board[row][col] == -1 and not self.flags[row][col]:
                        mine_rect = self.images['mine'].get_rect()
                        mine_rect.center = (x + self.cell_size // 2, y + self.cell_size // 2)
                        self.screen.blit(self.images['mine'], mine_rect)
        
        # 폭발 효과 그리기
        if self.explosion:
            if not self.explosion.update():
                self.explosion = None
                self.show_restart_modal = True
            else:
                self.explosion.draw(self.screen)
        
        # 재시작 모달 그리기
        if self.show_restart_modal:
            self.draw_restart_modal()
        
        pygame.display.update()
    
    def draw_restart_modal(self):
        modal_width = 300
        modal_height = 150
        modal_x = (self.screen_width - modal_width) // 2
        modal_y = (self.screen_height - modal_height) // 2
        
        # 모달 배경
        pygame.draw.rect(self.screen, WHITE, (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, BLACK, (modal_x, modal_y, modal_width, modal_height), 2)
        
        # 게임 오버 메시지
        game_over_text = self.large_font.render("게임 오버!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, modal_y + 40))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 재시작 버튼
        restart_button_width = 120
        restart_button_height = 40
        restart_button_x = (self.screen_width - restart_button_width) // 2
        restart_button_y = modal_y + 80
        self.restart_button_rect = pygame.Rect(restart_button_x, restart_button_y, restart_button_width, restart_button_height)
        
        pygame.draw.rect(self.screen, BLUE, self.restart_button_rect)
        pygame.draw.rect(self.screen, BLACK, self.restart_button_rect, 2)
        
        restart_text = self.font.render("재시작", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(restart_text, restart_text_rect)
    
    def get_cell_at_pos(self, pos):
        x, y = pos
        if y < self.top_height:
            return None
        
        col = x // self.cell_size
        row = (y - self.top_height) // self.cell_size
        
        if 0 <= row < self.height and 0 <= col < self.width:
            return (row, col)
        return None
    
    def left_click(self, row, col):
        if self.game_over or self.flags[row][col] or self.revealed[row][col] or self.show_restart_modal:
            return
        
        # 첫 번째 클릭인 경우
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
            self.start_time = time.time()
        
        # 지뢰를 클릭한 경우
        if self.board[row][col] == -1:
            self.revealed[row][col] = True
            self.game_over = True
            self.face_button = 'sad'
            
            # 폭발 효과 생성
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.top_height + self.cell_size // 2
            self.explosion = Explosion(x, y, self.cell_size)
            return
        
        # 빈 칸을 클릭한 경우
        self.reveal_cell(row, col)
        
        # 승리 조건 확인
        if self.check_win():
            self.game_over = True
            self.face_button = 'cool'
            self.show_restart_modal = True
    
    def right_click(self, row, col):
        if self.game_over or self.revealed[row][col] or self.show_restart_modal:
            return
        
        # 깃발 토글
        if not self.flags[row][col]:
            self.flags[row][col] = True
            self.mines_left -= 1
        else:
            self.flags[row][col] = False
            self.mines_left += 1
    
    def reveal_cell(self, row, col):
        # 이미 열린 칸이거나 깃발이 있는 경우
        if self.revealed[row][col] or self.flags[row][col]:
            return
        
        # 칸 열기
        self.revealed[row][col] = True
        
        # 빈 칸(0)인 경우 주변 칸 자동 열기
        if self.board[row][col] == 0:
            for i in range(max(0, row-1), min(self.height, row+2)):
                for j in range(max(0, col-1), min(self.width, col+2)):
                    if (i != row or j != col) and not self.revealed[i][j]:
                        self.reveal_cell(i, j)
    
    def check_win(self):
        for row in range(self.height):
            for col in range(self.width):
                # 지뢰가 아닌 칸이 아직 열리지 않았으면 승리하지 않음
                if self.board[row][col] != -1 and not self.revealed[row][col]:
                    return False
        return True
    
    def check_face_button_click(self, pos):
        x, y = pos
        face_rect = self.images[self.face_button].get_rect()
        face_rect.midtop = (self.screen_width // 2, 45)
        
        if face_rect.collidepoint(x, y):
            self.initialize_game()
            return True
        return False
    
    def check_restart_button_click(self, pos):
        if self.show_restart_modal and hasattr(self, 'restart_button_rect'):
            if self.restart_button_rect.collidepoint(pos):
                self.initialize_game()
                return True
        return False
    
    def show_difficulty_menu(self):
        menu_width = 300
        menu_height = 200
        menu_x = (self.screen_width - menu_width) // 2
        menu_y = (self.screen_height - menu_height) // 2
        
        menu_surface = pygame.Surface((menu_width, menu_height))
        menu_surface.fill(WHITE)
        pygame.draw.rect(menu_surface, BLACK, (0, 0, menu_width, menu_height), 2)
        
        title_text = self.font.render("난이도 선택", True, BLACK)
        title_rect = title_text.get_rect(center=(menu_width // 2, 30))
        menu_surface.blit(title_text, title_rect)
        
        button_height = 40
        button_width = 200
        button_margin = 10
        button_x = (menu_width - button_width) // 2
        
        buttons = []
        
        for i, level in enumerate(self.difficulty_levels.keys()):
            button_y = 60 + i * (button_height + button_margin)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            buttons.append((button_rect, level))
            
            pygame.draw.rect(menu_surface, DARK_GRAY, button_rect)
            pygame.draw.rect(menu_surface, BLACK, button_rect, 2)
            
            level_text = self.font.render(level, True, WHITE)
            text_rect = level_text.get_rect(center=button_rect.center)
            menu_surface.blit(level_text, text_rect)
        
        self.screen.blit(menu_surface, (menu_x, menu_y))
        pygame.display.update()
        
        # 메뉴 이벤트 처리
        menu_active = True
        while menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    relative_pos = (mouse_pos[0] - menu_x, mouse_pos[1] - menu_y)
                    
                    for button_rect, level in buttons:
                        if button_rect.collidepoint(relative_pos):
                            self.set_difficulty(level)
                            self.initialize_game()
                            menu_active = False
                            break
    
    def main_loop(self):
        running = True
        while running:
            # 타이머 업데이트
            if not self.game_over and not self.first_click:
                self.elapsed_time = int(time.time() - self.start_time)
            
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    # 재시작 모달 버튼 클릭 확인
                    if self.check_restart_button_click(pos):
                        continue
                    
                    # 재시작 버튼 클릭 확인
                    if self.check_face_button_click(pos):
                        continue
                    
                    # 난이도 메뉴 열기 (상단 영역 더블 클릭)
                    if event.button == 1 and pos[1] < self.top_height and event.button == 1:
                        if hasattr(self, 'last_click_time') and time.time() - self.last_click_time < 0.3:
                            self.show_difficulty_menu()
                        self.last_click_time = time.time()
                    
                    cell = self.get_cell_at_pos(pos)
                    if cell:
                        row, col = cell
                        if event.button == 1:  # 좌클릭
                            self.left_click(row, col)
                        elif event.button == 3:  # 우클릭
                            self.right_click(row, col)
            
            # 화면 그리기
            self.draw_board()
            
            # 프레임 제한
            pygame.time.Clock().tick(30)
        
        pygame.quit()

if __name__ == "__main__":
    game = Minesweeper()
