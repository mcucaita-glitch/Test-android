import os
import json
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
clock = pygame.time.Clock()

# ---------- Rutas ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def asset(*parts):
    return os.path.join(BASE_DIR, "assets", *parts)


def get_user_dir():
    # En Android p4a define ANDROID_PRIVATE (carpeta escribible de la app).
    path = os.environ.get("ANDROID_PRIVATE")
    if not path:
        try:
            from android.storage import app_storage_path
            path = app_storage_path()
        except Exception:
            path = BASE_DIR
    return path


# ---------- Pruebas ----------
results = []


def check(name, fn):
    try:
        detail = fn()
        results.append((name, True, detail or ""))
    except Exception as e:
        results.append((name, False, f"{type(e).__name__}: {e}"))


state = {}


def t_jpg():
    img = pygame.image.load(asset("stage_test.jpg")).convert()
    state["stage"] = pygame.transform.smoothscale(img, (1050, 400))
    return f"{img.get_width()}x{img.get_height()}"


def t_font():
    state["font"] = pygame.font.Font(asset("font.ttf"), 26)
    state["font_small"] = pygame.font.Font(asset("font.ttf"), 20)
    return "ttf ok"


def t_alpha():
    img = pygame.image.load(asset("icon_alpha.png")).convert_alpha()
    state["icon"] = img
    corner = img.get_at((0, 0))[3]
    center = img.get_at((32, 32))[3]
    if corner != 0 or center != 255:
        raise ValueError(f"alfa raro: esquina={corner} centro={center}")
    return "alfa ok"


def t_mask_colors():
    mask = pygame.image.load(asset("stage_test_mask.png")).convert()
    # Reescalado SIN suavizado, como se haria con una mascara reducida
    big = pygame.transform.scale(mask, (2100, 800))
    expected = {
        "calle": ((400, 400), (255, 255, 255)),
        "salida": ((220, 400), (0, 255, 255)),
        "meta": ((1890, 400), (250, 0, 250)),
        "fuera": ((10, 10), (0, 0, 0)),
    }
    bad = []
    for name, (pos, color) in expected.items():
        got = tuple(big.get_at(pos))[:3]
        if got != color:
            bad.append(f"{name}:{got}")
    if bad:
        raise ValueError("colores alterados " + ", ".join(bad))
    state["mask"] = big
    return "colores exactos"


def t_pixelmask():
    mask = state["mask"]
    m = pygame.mask.from_threshold(mask, (250, 0, 250), (1, 1, 1, 255))
    n = m.count()
    if n == 0:
        raise ValueError("from_threshold no encontro la meta")
    return f"meta={n}px"


def t_json():
    with open(asset("data.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["teams"][0]["name"]


def t_save():
    path = os.path.join(get_user_dir(), "test_save.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"slot": 1, "week": 7}, f)
    with open(path, "r", encoding="utf-8") as f:
        back = json.load(f)
    if back["week"] != 7:
        raise ValueError("lectura distinta")
    return path


check("JPG", t_jpg)
check("Fuente TTF", t_font)
check("PNG alfa", t_alpha)
check("Mascara colores", t_mask_colors)
check("pygame.mask", t_pixelmask)
check("JSON", t_json)
check("Guardar en carpeta usuario", t_save)

font = state.get("font") or pygame.font.Font(None, 30)
font_small = state.get("font_small") or pygame.font.Font(None, 22)
pos = (640, 600)
SAFE_TOP = 70

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            pos = event.pos

    screen.fill((16, 18, 28))

    if "stage" in state:
        screen.blit(state["stage"], (115, 330))

    y = SAFE_TOP
    for name, ok, detail in results:
        color = (80, 220, 100) if ok else (230, 80, 80)
        mark = "OK  " if ok else "FALLA"
        screen.blit(font.render(f"{mark}  {name}", True, color), (40, y))
        screen.blit(font_small.render(detail[:70], True, (160, 170, 190)), (420, y + 4))
        y += 34

    if "icon" in state:
        screen.blit(state["icon"], (pos[0] - 32, pos[1] - 32))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
