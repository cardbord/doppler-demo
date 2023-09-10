import pygame;from pygame.gfxdraw import aacircle;pygame.init();font = pygame.font.SysFont('consolas.ttf',32);winsize = pygame.display.get_desktop_sizes()
if len(pygame.display.get_desktop_sizes()) > 1: winsize = winsize[0]
dis = pygame.display.set_mode(winsize);distance_from_edge = round((winsize[0] - 520)/2);pygame.display.set_caption('doppler effect simulation')
def draw_transparent_circle(win,x,y,radius,color,alpha_level):aacircle(win,round(x),round(y),radius,(color[0],color[1],color[2],alpha_level))
class control: #slider
    def __init__(self):self.value = [30/100,900];self.highlighted = False
    def calcval(self,newval):self.value[0] = newval/100
    def draw(self): 
        pygame.draw.aaline(dis,(50,50,50),(distance_from_edge,900),(distance_from_edge+520,900))
        if self.highlighted is True:aacircle(dis,round(self.value[0]*100)+distance_from_edge,900,20,(50,50,50,255))
        else:aacircle(dis,round(self.value[0]*100)+distance_from_edge,900,20,(50,50,50,80))
class wave: #generated wave
    def __init__(self,sourcepos):self.og_source = sourcepos;self.alpha = 255;self.rad = 30
    def draw(self):draw_transparent_circle(dis,self.og_source[0],self.og_source[1],self.rad,(0,0,0),self.alpha if self.alpha > -1 else 0)
    def update(self,wavelength):self.rad += 3;self.alpha -= wavelength
class wavesource: #source
    def __init__(self):self.pos = [200,200]
    def draw(self):pygame.draw.circle(dis,(0,0,0),(self.pos[0],self.pos[1]),30)
source = wavesource();slider = control();up = False;down = False;left = False;right = False;speed = 1;wavelength = 3;isclicked = False;clock = pygame.time.Clock();waves = []
while True:
    temp_pos = [];temp_pos.append(source.pos[0]);temp_pos.append(source.pos[1]);waves.append(wave(temp_pos));dis.fill((255,255,255));source.draw() #drawing source
    for event in pygame.event.get():
        if event.type == pygame.QUIT:pygame.quit();quit() 
        if event.type == pygame.KEYDOWN: #wasd movement
            if event.key == pygame.K_s:down = True
            if event.key == pygame.K_w:up = True
            if event.key == pygame.K_a:left = True
            if event.key == pygame.K_d:right = True
            if event.key == pygame.K_RIGHT: #wave life settings (DO NOT USE 1 IT LAGS SO BAD)
                    if wavelength == 1:print('maximum wave life reached.')
                    else:wavelength -=1; print(f'wave life increased to {round(1920/wavelength)}mm')
            if event.key == pygame.K_LEFT:wavelength +=1; print(f'wave life decreased to {round(1920/wavelength)}mm')
            if event.key == pygame.K_ESCAPE:pygame.quit();quit()
        if event.type == pygame.KEYUP: #wasd movement, releases
            if event.key == pygame.K_s:down = False
            if event.key == pygame.K_w:up = False
            if event.key == pygame.K_a:left = False
            if event.key == pygame.K_d:right = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            if mousepos[0] in range(round(slider.value[0]*100)+distance_from_edge-20,round(slider.value[0]*100)+distance_from_edge+60): slider.highlighted = True;isclicked = True #if clicked on slider  
        if event.type == pygame.MOUSEBUTTONUP: isclicked = False;slider.highlighted = False #if released from slider
    text = font.render(f'{round(speed*66)}m/s',True,(0,0,0),None); textRect = text.get_rect();textRect.center = (1300,900);dis.blit(text,textRect);speed = slider.value[0] # display velocity and set speed to slider's velocity value
    for wave_value in waves:
        if wave_value.alpha <= 0: del wave_value #del wave if it is transparent
        else: wave_value.update(wavelength);wave_value.draw() #enlarge and draw waves
    if up == True:source.pos[1] -= speed
    if down == True:source.pos[1] +=speed
    if left == True:source.pos[0] -=speed
    if right == True:source.pos[0] += speed
    if isclicked == True:
        mousepos = pygame.mouse.get_pos()
        if mousepos[0] in range(distance_from_edge,distance_from_edge+520):slider.calcval(mousepos[0]-distance_from_edge)
    slider.draw();pygame.display.flip();clock.tick(120)