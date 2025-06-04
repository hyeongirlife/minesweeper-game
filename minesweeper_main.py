import pygame
import sys
import random
import math
import time

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
BLUE = (0, 0, 255)

class Mine:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.size = random.randint(10, 30)
        self.speed = random.uniform(0.5, 2.0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # 화면 경계 처리
        if self.x < 0:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = 0
        
        if self.y < 0:
            self.y = self.screen_height
        elif self.y > self.screen_height:
            self.y = 0
    
    def draw(self, screen):
        # 지뢰 그리기 (간단한 원과 십자가)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size)
        pygame.draw.line(screen, GRAY, (self.x - self.size/2, self.y), (self.x + self.size/2, self.y), 2)
        pygame.draw.line(screen, GRAY, (self.x, self.y - self.size/2), (self.x, self.y + self.size/2), 2)

class MainPage:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("지뢰 찾기")
        
        # 화면 설정
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # 폰트 초기화
        pygame.font.init()
        
        # macOS에서 한글 지원 폰트 시도
        try:
            # macOS 한글 폰트 경로
            font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
            self.title_font = pygame.font.Font(font_path, 60)
            self.button_font = pygame.font.Font(font_path, 30)
            self.credit_font = pygame.font.Font(font_path, 20)
        except:
            try:
                # 시스템 한글 폰트 시도
                self.title_font = pygame.font.SysFont('AppleGothic', 60, bold=True)
                self.button_font = pygame.font.SysFont('AppleGothic', 30)
                self.credit_font = pygame.font.SysFont('AppleGothic', 20)
            except:
                # 기본 폰트로 대체
                self.title_font = pygame.font.SysFont('Arial', 60, bold=True)
                self.button_font = pygame.font.SysFont('Arial', 30)
                self.credit_font = pygame.font.SysFont('Arial', 20)
        
        # 배경 지뢰 애니메이션
        self.mines = [Mine(self.screen_width, self.screen_height) for _ in range(15)]
        
        # 버튼 설정
        self.button_width = 200
        self.button_height = 60
        self.button_x = (self.screen_width - self.button_width) // 2
        self.button_y = self.screen_height // 2 + 50
        self.button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        
        self.run()
    
    def draw_main_page(self):
        # 배경 그리기
        self.screen.fill(GRAY)
        
        # 배경 지뢰 애니메이션
        for mine in self.mines:
            mine.move()
            mine.draw(self.screen)
        
        # 제목 그리기
        title_text = self.title_font.render("지뢰 찾기 게임", True, BLACK)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(title_text, title_rect)
        
        # 시작 버튼 그리기
        pygame.draw.rect(self.screen, DARK_GRAY, self.button_rect)
        pygame.draw.rect(self.screen, BLACK, self.button_rect, 2)
        
        start_text = self.button_font.render("게임 시작", True, WHITE)
        start_rect = start_text.get_rect(center=self.button_rect.center)
        self.screen.blit(start_text, start_rect)
        
        # 제작자 정보
        credit_text = self.credit_font.render("Made by hyeongeol", True, BLACK)
        credit_rect = credit_text.get_rect(bottomright=(self.screen_width - 20, self.screen_height - 20))
        self.screen.blit(credit_text, credit_rect)
        
        pygame.display.update()
    
    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        # 게임 시작
                        running = False
            
            self.draw_main_page()
            clock.tick(60)
        
        # 메인 페이지 종료 후 게임 시작
        from minesweeper_game import Minesweeper
        game = Minesweeper()

if __name__ == "__main__":
    MainPage()
