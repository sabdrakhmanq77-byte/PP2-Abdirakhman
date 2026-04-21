import pygame
import datetime


class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.image.load(r"C:\Users\User\OneDrive\Desktop\project\PP2\pr9\mickeys_clock\images\5388708274896572790.jpg").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (800, 800))

        self.hand_m = pygame.image.load(r"C:\Users\User\OneDrive\Desktop\project\PP2\pr9\mickeys_clock\images\ha.png").convert_alpha()
        self.hand_s = pygame.image.load(r"C:\Users\User\OneDrive\Desktop\project\PP2\pr9\mickeys_clock\images\5388708274896572793.jpg").convert_alpha()

        self.hand_m = pygame.transform.scale(self.hand_m, (800, 800)) 
        self.hand_s = pygame.transform.scale(self.hand_s, (800, 800))

        self.angle_m = 0
        self.angle_s = 0

    def updatetime(self):
        now = datetime.datetime.now()
        self.angle_m = -now.minute*6 + 60
        self.angle_s = -now.second*6 

    def drawscreen(self):
        self.screen.blit(self.bg, (0,0))

        rot_m = pygame.transform.rotate(self.hand_m, self.angle_m)
        rect_m = rot_m.get_rect(center=(400, 400))
        self.screen.blit(rot_m, rect_m)

        rot_s = pygame.transform.rotate(self.hand_s, self.angle_s)
        rect_s = rot_s.get_rect(center=(400, 400))
        self.screen.blit(rot_s, rect_s)