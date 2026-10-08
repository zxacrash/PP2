import pygame, sys, math, os
from datetime import datetime

SCREEN_W, SCREEN_H, TOOLBAR_W = 900, 650, 160
CANVAS_X, CANVAS_W, CANVAS_H = TOOLBAR_W, 900 - TOOLBAR_W, 650
WHITE, BLACK = (255,255,255), (0,0,0)
BG_TOOLBAR, BG_CANVAS = (40,42,54), (255,255,255)
HIGHLIGHT, TEXT_COLOUR = (80,140,255), (220,220,220)

PALETTE = [(0,0,0),(220,40,40),(30,120,255),(50,200,80),(255,220,0),
           (255,140,0),(180,60,200),(0,200,200),(255,105,180),
           (139,90,43),(128,128,128),(255,255,255)]
BRUSH_SIZES = [2, 4, 8, 16]

TOOL_PENCIL, TOOL_LINE, TOOL_RECT, TOOL_SQUARE = "pencil","line","rect","square"
TOOL_CIRCLE, TOOL_RTRIANGLE, TOOL_EQTRIANGLE   = "circle","right_tri","eq_tri"
TOOL_RHOMBUS, TOOL_FILL, TOOL_ERASER           = "rhombus","fill","eraser"
TOOL_TEXT                                       = "text"

TOOL_LABELS = {TOOL_PENCIL:"Pencil",TOOL_LINE:"Line",TOOL_RECT:"Rectangle",
               TOOL_SQUARE:"Square",TOOL_CIRCLE:"Circle",TOOL_RTRIANGLE:"R-Triangle",
               TOOL_EQTRIANGLE:"Eq-Triangle",TOOL_RHOMBUS:"Rhombus",
               TOOL_FILL:"Fill",TOOL_ERASER:"Eraser",TOOL_TEXT:"Text"}
TOOL_ORDER = [TOOL_PENCIL,TOOL_LINE,TOOL_RECT,TOOL_SQUARE,TOOL_CIRCLE,
              TOOL_RTRIANGLE,TOOL_EQTRIANGLE,TOOL_RHOMBUS,TOOL_FILL,TOOL_ERASER,TOOL_TEXT]

# Font sizes mapped to brush sizes
FONT_SIZES = {2: 12, 4: 18, 8: 28, 16: 48}

def pts_right_tri(x1,y1,x2,y2): return [(x1,y1),(x1,y2),(x2,y2)]
def pts_eq_tri(x1,y1,x2,y2):
    bx1,bx2,by = min(x1,x2),max(x1,x2),max(y1,y2)
    cx,side = (bx1+bx2)/2, bx2-bx1
    return [(cx, by-side*math.sqrt(3)/2),(bx1,by),(bx2,by)]
def pts_rhombus(x1,y1,x2,y2):
    lx,rx,ty,by = min(x1,x2),max(x1,x2),min(y1,y2),max(y1,y2)
    cx,cy = (lx+rx)/2,(ty+by)/2
    return [(cx,ty),(rx,cy),(cx,by),(lx,cy)]

def flood_fill(surface, pos, fill_colour):
    target = surface.get_at(pos)[:3]
    if target == fill_colour: return
    w,h = surface.get_size()
    stack, visited = [pos], set()
    while stack:
        x,y = stack.pop()
        if (x,y) in visited or not(0<=x<w and 0<=y<h): continue
        if surface.get_at((x,y))[:3] != target: continue
        surface.set_at((x,y), fill_colour)
        visited.add((x,y))
        stack += [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]


class Toolbar:
    BTN_H, BTN_PAD, SEC_GAP = 34, 4, 10

    def __init__(self, font, small_font):
        self.font, self.small_font = font, small_font
        self.tool_rects = {}
        y = 10
        for tool in TOOL_ORDER:
            self.tool_rects[tool] = pygame.Rect(6, y, TOOLBAR_W-12, self.BTN_H)
            y += self.BTN_H + self.BTN_PAD
        self.tool_bottom = y + self.SEC_GAP

        self.palette_rects = []
        px, py, S = 8, self.tool_bottom+24, 28
        for i, col in enumerate(PALETTE):
            r = pygame.Rect(px+(i%4)*(S+4), py+(i//4)*(S+4), S, S)
            self.palette_rects.append((r, col))
        self.pal_bottom = py+((len(PALETTE)//4)+1)*(S+4)+self.SEC_GAP

        self.size_rects = []
        sx, sy = 10, self.pal_bottom+24
        for i, sz in enumerate(BRUSH_SIZES):
            self.size_rects.append((pygame.Rect(sx+i*34, sy, 30, 30), sz))
        self.clear_rect = pygame.Rect(10, sy+44, TOOLBAR_W-20, 32)

    def draw(self, surface, active_tool, active_colour, active_size):
        pygame.draw.rect(surface, BG_TOOLBAR, (0,0,TOOLBAR_W,SCREEN_H))
        pygame.draw.line(surface, HIGHLIGHT, (TOOLBAR_W-1,0),(TOOLBAR_W-1,SCREEN_H),2)
        surface.blit(self.small_font.render("TOOLS",True,TEXT_COLOUR),(4,2))
        for tool, rect in self.tool_rects.items():
            pygame.draw.rect(surface, HIGHLIGHT if tool==active_tool else (60,63,78), rect, border_radius=5)
            label_surf = self.small_font.render(TOOL_LABELS[tool],True,WHITE)
            surface.blit(label_surf, label_surf.get_rect(center=rect.center))
        surface.blit(self.small_font.render("COLOUR",True,TEXT_COLOUR),(4,self.tool_bottom+6))
        for rect, col in self.palette_rects:
            pygame.draw.rect(surface, col, rect, border_radius=4)
            pygame.draw.rect(surface, WHITE if col==active_colour else (100,100,100), rect, 3 if col==active_colour else 1, border_radius=4)
        surface.blit(self.small_font.render("SIZE",True,TEXT_COLOUR),(4,self.pal_bottom+6))
        for rect, sz in self.size_rects:
            pygame.draw.rect(surface, HIGHLIGHT if sz==active_size else (60,63,78), rect, border_radius=4)
            pygame.draw.circle(surface, WHITE, rect.center, min(sz//2,10))
        pygame.draw.rect(surface, (180,50,50), self.clear_rect, border_radius=6)
        clear_surf = self.small_font.render("Clear",True,WHITE)
        surface.blit(clear_surf, clear_surf.get_rect(center=self.clear_rect.center))

    def handle_click(self, pos, tool, colour, size):
        clear = False
        for t, r in self.tool_rects.items():
            if r.collidepoint(pos): tool = t
        for r, c in self.palette_rects:
            if r.collidepoint(pos): colour = c
        for r, s in self.size_rects:
            if r.collidepoint(pos): size = s
        if self.clear_rect.collidepoint(pos): clear = True
        return tool, colour, size, clear


class TextInput:
    """Manages inline text editing state."""
    def __init__(self):
        self.active = False
        self.pos = (0, 0)       # canvas coords
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0

    def start(self, pos):
        self.active = True
        self.pos = pos
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0

    def stop(self):
        self.active = False
        self.text = ""

    def tick(self):
        """Call once per frame to blink the cursor."""
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def handle_key(self, event):
        """Returns True if the key was consumed."""
        if not self.active:
            return False
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return False   # caller should commit
        elif event.key == pygame.K_ESCAPE:
            self.stop()
        else:
            ch = event.unicode
            if ch and ch.isprintable():
                self.text += ch
        return True


class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Paint")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial",18,bold=True)
        self.small_font = pygame.font.SysFont("arial",13)
        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(BG_CANVAS)
        self.toolbar = Toolbar(self.font, self.small_font)
        self.active_tool, self.active_colour, self.active_size = TOOL_PENCIL, BLACK, 4
        self.drawing, self.start_pos, self.last_pos, self.running = False, None, None, True
        self.save_msg, self.save_msg_timer = "", 0
        self.text_input = TextInput()

    def _get_text_font(self):
        size = FONT_SIZES.get(self.active_size, 18)
        return pygame.font.SysFont("arial", size)

    def to_canvas(self, pos): return (pos[0]-CANVAS_X, pos[1])
    def on_canvas(self, pos): return pos[0] >= CANVAS_X

    def save_canvas(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(script_dir, f"drawing_{timestamp}.png")
        pygame.image.save(self.canvas, filename)
        self.save_msg = f"Saved: {os.path.basename(filename)}"
        self.save_msg_timer = 180

    def _commit_text(self):
        """Render the typed text onto the canvas."""
        if self.text_input.text:
            tf = self._get_text_font()
            surf = tf.render(self.text_input.text, True, self.active_colour)
            self.canvas.blit(surf, self.text_input.pos)
        self.text_input.stop()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self._handle_events()
            if self.text_input.active:
                self.text_input.tick()
            self._draw()
        pygame.quit(); sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False

            elif event.type == pygame.KEYDOWN:
                # Text tool captures keys when active
                if self.text_input.active:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self._commit_text()
                    else:
                        self.text_input.handle_key(event)
                    continue  # swallow the key

                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_DELETE:
                    self.canvas.fill(BG_CANVAS)
                if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                    self.save_canvas()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                # If text is active and user clicks somewhere else — commit first
                if self.text_input.active:
                    self._commit_text()

                if not self.on_canvas(pos):
                    self.active_tool, self.active_colour, self.active_size, clear = \
                        self.toolbar.handle_click(pos, self.active_tool, self.active_colour, self.active_size)
                    if clear: self.canvas.fill(BG_CANVAS)
                else:
                    cp = self.to_canvas(pos)
                    if self.active_tool == TOOL_TEXT:
                        self.text_input.start(cp)
                    elif self.active_tool == TOOL_FILL:
                        flood_fill(self.canvas, cp, self.active_colour)
                    else:
                        self.drawing, self.start_pos, self.last_pos = True, cp, cp
                        if self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                            pygame.draw.circle(self.canvas,
                                WHITE if self.active_tool==TOOL_ERASER else self.active_colour,
                                cp, self.active_size//2)

            elif event.type == pygame.MOUSEMOTION and self.drawing:
                pos = event.pos
                if self.on_canvas(pos) and self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                    cp = self.to_canvas(pos)
                    pygame.draw.line(self.canvas,
                        WHITE if self.active_tool==TOOL_ERASER else self.active_colour,
                        self.last_pos, cp, self.active_size)
                    self.last_pos = cp

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.drawing and self.on_canvas(event.pos):
                    self._commit_shape(self.start_pos, self.to_canvas(event.pos))
                self.drawing, self.start_pos = False, None

    def _shape_pts(self, tool, x1, y1, x2, y2):
        if tool == TOOL_RTRIANGLE:  return pts_right_tri(x1,y1,x2,y2)
        if tool == TOOL_EQTRIANGLE: return pts_eq_tri(x1,y1,x2,y2)
        if tool == TOOL_RHOMBUS:    return pts_rhombus(x1,y1,x2,y2)
        return None

    def _commit_shape(self, p1, p2):
        x1,y1,x2,y2 = *p1, *p2
        col, w, tool = self.active_colour, self.active_size, self.active_tool
        if tool == TOOL_LINE:
            pygame.draw.line(self.canvas, col, p1, p2, w)
        elif tool == TOOL_RECT:
            pygame.draw.rect(self.canvas, col, (min(x1,x2),min(y1,y2),abs(x2-x1),abs(y2-y1)), w)
        elif tool == TOOL_SQUARE:
            side = min(abs(x2-x1),abs(y2-y1))
            pygame.draw.rect(self.canvas, col, ((x1 if x2>=x1 else x1-side),(y1 if y2>=y1 else y1-side),side,side), w)
        elif tool == TOOL_CIRCLE:
            pygame.draw.circle(self.canvas, col, ((x1+x2)//2,(y1+y2)//2), max(1,int(math.hypot(x2-x1,y2-y1)/2)), w)
        else:
            pts = self._shape_pts(tool,x1,y1,x2,y2)
            if pts: pygame.draw.polygon(self.canvas, col, [(int(px),int(py)) for px,py in pts], w)

    def _draw_preview(self, surface, p1, p2):
        x1,y1,x2,y2 = *p1, *p2
        col, w, tool = self.active_colour, self.active_size, self.active_tool
        def sc(pt): return (pt[0]+CANVAS_X, pt[1])
        if tool == TOOL_LINE:
            pygame.draw.line(surface, col, sc(p1), sc(p2), w)
        elif tool == TOOL_RECT:
            pygame.draw.rect(surface, col, (min(x1,x2)+CANVAS_X,min(y1,y2),abs(x2-x1),abs(y2-y1)), w)
        elif tool == TOOL_SQUARE:
            side = min(abs(x2-x1),abs(y2-y1))
            pygame.draw.rect(surface, col, ((x1 if x2>=x1 else x1-side)+CANVAS_X,(y1 if y2>=y1 else y1-side),side,side), w)
        elif tool == TOOL_CIRCLE:
            pygame.draw.circle(surface, col, ((x1+x2)//2+CANVAS_X,(y1+y2)//2), max(1,int(math.hypot(x2-x1,y2-y1)/2)), w)
        else:
            pts = self._shape_pts(tool,x1,y1,x2,y2)
            if pts: pygame.draw.polygon(surface, col, [(int(px)+CANVAS_X,int(py)) for px,py in pts], w)

    def _draw_text_cursor(self, surface):
        """Draw the live text preview + blinking cursor on screen."""
        ti = self.text_input
        tf = self._get_text_font()
        preview = tf.render(ti.text, True, self.active_colour)
        sx, sy = ti.pos[0] + CANVAS_X, ti.pos[1]
        surface.blit(preview, (sx, sy))

        # Blinking cursor
        if ti.cursor_visible:
            cursor_x = sx + preview.get_width() + 1
            cursor_h = tf.get_height()
            pygame.draw.line(surface, self.active_colour,
                             (cursor_x, sy), (cursor_x, sy + cursor_h), 2)

        # Underline showing the text baseline
        pygame.draw.line(surface, (180, 180, 220),
                         (sx, sy + preview.get_height()),
                         (sx + max(preview.get_width(), 40) + 6, sy + preview.get_height()), 1)

    def _draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.canvas, (CANVAS_X, 0))

        if self.drawing and self.start_pos and self.active_tool not in (TOOL_PENCIL,TOOL_ERASER,TOOL_FILL,TOOL_TEXT):
            self._draw_preview(self.screen, self.start_pos, self.to_canvas(pygame.mouse.get_pos()))

        if self.text_input.active:
            self._draw_text_cursor(self.screen)

        self.toolbar.draw(self.screen, self.active_tool, self.active_colour, self.active_size)

        cx,cy = self.to_canvas(pygame.mouse.get_pos())
        pygame.draw.rect(self.screen,(25,25,35),(0,SCREEN_H-18,TOOLBAR_W,18))

        # Status bar hint for text tool
        if self.active_tool == TOOL_TEXT and self.text_input.active:
            hint = "Type text · Enter = commit · Esc = cancel"
        elif self.active_tool == TOOL_TEXT:
            hint = "Click canvas to place text"
        else:
            hint = f"{TOOL_LABELS.get(self.active_tool,'')} ({cx},{cy}) sz:{self.active_size}"
        self.screen.blit(self.small_font.render(hint, True, TEXT_COLOUR),(4,SCREEN_H-16))

        if self.save_msg_timer > 0:
            self.save_msg_timer -= 1
            alpha = min(255, self.save_msg_timer * 4)
            msg_surf = self.small_font.render(self.save_msg, True, (80, 255, 120))
            msg_surf.set_alpha(alpha)
            self.screen.blit(msg_surf, (CANVAS_X + 10, SCREEN_H - 20))

        pygame.display.flip()

if __name__ == "__main__":
    PaintApp().run()