import pygame
import random
import math
from pygame import mixer
#endregion

#region Inicialización
pygame.init()
mixer.init()
#endregion

#region Pantalla y fondo
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mettaton Madness")
icono_ventana = pygame.image.load("MettatonMadness.webp")
pygame.display.set_icon(icono_ventana)

#Fondo negro
fondo = pygame.Surface((800, 600))
fondo.fill((0, 0, 0))
#endregion

#region Música
mixer.init()
musica_menu = mixer.Sound("Start-Menu.mp3")
musica = mixer.Sound("Anticipation.mp3")

musica_menu.play(loops=-1) #Bucle infinito
#endregion

#region Variables globales
nombre_j1 = ""
nombre_j2 = ""
puntaje_j1 = 0
puntaje_j2 = 0
salud = 20
salud_maxima = 20
salud2 = 20
salud2_maxima = 20
nivel = 1
enemigos_por_nivel = 10
enemigos_eliminados = 0
record = 0
record_j1 = 0
record_j2 = 0
en_pausa = False
mostrar_play = False
tiempo_play = 0
DURACION_PLAY = 800
jugador1_activo = True
jugador2_activo = False
jugador2_atacando = False
ataque_frame = 0
ultimo_cambio_frame = 0
duracion_frame_ms = 150
ataque_en_progreso = False
ATAQUE_FRAME_HIT = 3
ataque_hit_done = False
modo_multijugador = False
ultimo_modo = None
volver_a_menu = False  # para el bucle principal
en_ejecucion = True
estado_menu = "principal"
modo_juego = "Un Jugador"
opciones_menu = ["Un Jugador", "Multijugador", "Historia", "Créditos", "Salir"]
opcion_actual = 0
opciones_dificultad = ["Principiante", "Normal", "Leyenda", "Volver al Menú"]
dificultad_actual = 0
dificultad = "Normal"

# --- ESTADÍSTICAS / TRACKING ---
tiempo_inicio_partida = 0
tiempo_inicio_vida_j1 = 0
tiempo_inicio_vida_j2 = 0

vidas_perdidas_j1 = 0
vidas_perdidas_j2 = 0

enemigos_total_j1 = 0
enemigos_total_j2 = 0

# Listas por vida (se llenan al perder una vida)
enemigos_por_vida_j1 = []
enemigos_por_vida_j2 = []
puntos_por_vida_j1 = []
puntos_por_vida_j2 = []

# Acumuladores de la vida actual
kills_vida_actual_j1 = 0
kills_vida_actual_j2 = 0
puntos_vida_actual_j1 = 0
puntos_vida_actual_j2 = 0

record_por_vida_j1 = 0
record_por_vida_j2 = 0
#endregion

#region Fuente y textos
fuente = pygame.font.Font("PressStart2P-Regular.ttf", 16)
fuente_final = pygame.font.Font("PressStart2P-Regular.ttf", 20)

def mostrar_puntaje(x, y):
    texto_j1 = fuente.render(f"{nombre_j1}: {puntaje_j1}  Rec: {record_j1}", True, (255, 255, 255))
    pantalla.blit(texto_j1, (x, y))
    if modo_juego == "Multijugador":
        texto_j2 = fuente.render(f"{nombre_j2}: {puntaje_j2}  Rec: {record_j2}", True, (255, 255, 255))
        pantalla.blit(texto_j2, (x, y + 20))

def mostrar_barra_salud(x, y, salud_actual, salud_maxima):
    ancho_unitario = 3
    altura = 20
    offset_vertical = 3

    ancho_total = int(salud_maxima * ancho_unitario)
    porcentaje = salud_actual / salud_maxima if salud_maxima > 0 else 0
    ancho_amarillo = int(ancho_total * porcentaje)
    ancho_rojo = ancho_total - ancho_amarillo

    pygame.draw.rect(pantalla, (255, 0, 0), (x + ancho_amarillo, y, ancho_rojo, altura))
    pygame.draw.rect(pantalla, (255, 255, 0), (x, y, ancho_amarillo, altura))

    texto = fuente.render(f"HP: {salud_actual}/{salud_maxima}", True, (255, 255, 255))
    pantalla.blit(texto, (x + ancho_total + 10, y + offset_vertical))

def mostrar_nivel(x, y, nivel):
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, (255, 255, 255))
    pantalla.blit(texto_nivel, (x, y))
#endregion

def comprobar_subida_nivel():
    global nivel, enemigos_eliminados, enemigos_por_nivel, salud, salud_maxima
    global cantidad_enemigos
    if enemigos_eliminados >= enemigos_por_nivel:
        if nivel == 3:
            musica.stop()
            sonido_felicitacion.play()

            texto_victoria = fuente_final.render("¡Has completado el juego!", True, (255, 255, 0))
            pantalla.blit(texto_victoria, ((800 - texto_victoria.get_width()) // 2, 150))
            # Menú de victoria con opción de estadísticas
            esperando_respuesta = True
            while esperando_respuesta:
                pantalla.fill((0, 0, 0))
                titulo = fuente_final.render("¡Has completado el juego!", True, (255, 255, 0))
                pantalla.blit(titulo, ((800 - titulo.get_width()) // 2, 150))

                puntaje1 = fuente.render(f"{nombre_j1}: {puntaje_j1} punto(s)", True, (255, 255, 255))
                pantalla.blit(puntaje1, ((800 - puntaje1.get_width()) // 2, 210))
                if modo_juego == "Multijugador":
                    puntaje2 = fuente.render(f"{nombre_j2}: {puntaje_j2} punto(s)", True, (255, 255, 255))
                    pantalla.blit(puntaje2, ((800 - puntaje2.get_width()) // 2, 240))

                mensaje1 = fuente.render("¿Qué deseas hacer?", True, (255, 255, 255))
                mensaje2 = fuente.render("Y = Reintentar", True, (255, 255, 255))
                mensaje3 = fuente.render("M = Menú Principal", True, (255, 255, 255))
                mensaje4 = fuente.render("N = Salir", True, (255, 255, 255))
                mensaje5 = fuente.render("E = Estadísticas por jugador", True, (255, 255, 255))

                pantalla.blit(mensaje1, ((800 - mensaje1.get_width()) // 2, 290))
                pantalla.blit(mensaje2, ((800 - mensaje2.get_width()) // 2, 330))
                pantalla.blit(mensaje3, ((800 - mensaje3.get_width()) // 2, 360))
                pantalla.blit(mensaje4, ((800 - mensaje4.get_width()) // 2, 390))
                pantalla.blit(mensaje5, ((800 - mensaje5.get_width()) // 2, 420))

                pygame.display.update()

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        esperando_respuesta = False
                        pygame.quit()
                        exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_y:
                            resetear_partida_interna()
                            musica.play(loops=-1)
                            esperando_respuesta = False
                        elif evento.key == pygame.K_m:
                            musica_menu.play(loops=-1)
                            esperando_respuesta = False
                            return
                        elif evento.key == pygame.K_n:
                            esperando_respuesta = False
                            pygame.quit()
                            exit()
                        elif evento.key == pygame.K_e:
                            mostrar_estadisticas()  # NUEVO: pantalla de estadísticas
            return

        # Sube nivel
        nivel += 1
        enemigos_eliminados = 0
        enemigos_por_nivel += 5

        # Recompensa de vida
        salud_maxima += 10
        salud = min(salud + 10, salud_maxima)

        # Aumentar velocidad enemigos
        for k in range(cantidad_enemigos):
            enemigo_x_cambio[k] *= 1.1
            enemigo_y_cambio[k] *= 1.1

        texto_nivel = fuente.render(f"Nivel {nivel - 1} completado. ¡Nivel {nivel}!", True, (255, 255, 0))
        pantalla.blit(texto_nivel, ((800 - texto_nivel.get_width()) // 2, 280))
        pygame.display.update()
        pygame.time.wait(2000)

def resetear_partida_interna():
    global puntaje_j1, puntaje_j2, salud, salud2, jugador_x, jugador_y, jugador2_x, jugador2_y
    global balas, enemigos_eliminados, nivel, enemigos_por_nivel, cantidad_enemigos
    global jugador1_activo, jugador2_activo, invulnerable, invulnerable_jugador2
    global ataque_en_progreso, jugador2_atacando, ataque_frame, ataque_hit_done
    global salud_maxima, salud2_maxima

    salud_maxima = 20
    salud2_maxima = 20

    puntaje_j1 = 0
    puntaje_j2 = 0
    salud = salud_maxima
    salud2 = salud2_maxima
    jugador_x = 368
    jugador_y = 520
    jugador2_x = 400
    jugador2_y = 520
    balas.clear()
    enemigos_eliminados = 0
    nivel = 1
    enemigos_por_nivel = 10
    jugador1_activo = True
    jugador2_activo = False
    invulnerable = False
    invulnerable_jugador2 = False
    ataque_en_progreso = False
    jugador2_atacando = False
    ataque_frame = 0
    ataque_hit_done = False

    for j in range(cantidad_enemigos):
        enemigo_x[j] = random.randint(0, 736)
        enemigo_y[j] = random.randint(0, 200)
        estado_explosion[j] = False
        tiempo_explosion[j] = 0

#region Menú principal (funciones del menú)
def mostrar_menu_pantalla():
    pantalla.fill((0, 0, 0))
    titulo = fuente.render("Mettaton Madness: Rebooted", True, (255, 255, 255))
    pantalla.blit(titulo, ((800 - titulo.get_width()) // 2, 80))

    for i, texto in enumerate(opciones_menu):
        color = (255, 255, 255) if i == opcion_actual else (180, 180, 180)
        render = fuente.render(texto, True, color)
        pantalla.blit(render, ((800 - render.get_width()) // 2, 180 + i * 40))

def seleccionar_dificultad():
    global dificultad, dificultad_actual
    seleccionando = True

    while seleccionando:
        pantalla.fill((0, 0, 0))
        titulo = fuente.render("Selecciona la dificultad", True, (255, 255, 255))
        pantalla.blit(titulo, ((800 - titulo.get_width()) // 2, 80))

        for i, texto in enumerate(opciones_dificultad):
            color = (255, 255, 255) if i == dificultad_actual else (180, 180, 180)
            render = fuente.render(texto, True, color)
            pantalla.blit(render, ((800 - render.get_width()) // 2, 180 + i * 40))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
               if evento.key in [pygame.K_UP, pygame.K_w]:
                dificultad_actual = (dificultad_actual - 1) % len(opciones_dificultad)
               elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                dificultad_actual = (dificultad_actual + 1) % len(opciones_dificultad)
               elif evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                dificultad = opciones_dificultad[dificultad_actual]
                seleccionando = False  # salir de la selección

def ingresar_nombre_jugador(jugador_numero=1):
    global nombre_j1, nombre_j2
    nombre = ""
    max_caracteres = 10
    escribiendo = True

    while escribiendo:
        pantalla.fill((0, 0, 0))

        titulo = fuente.render(f"Jugador {jugador_numero}, ingresa tu nombre:", True, (255, 255, 255))
        pantalla.blit(titulo, ((800 - titulo.get_width()) // 2, 200))

        texto_nombre = fuente.render(nombre, True, (255, 255, 0))
        pantalla.blit(texto_nombre, ((800 - texto_nombre.get_width()) // 2, 300))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre != "":
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < max_caracteres and evento.unicode.isprintable():
                        nombre += evento.unicode

    if jugador_numero == 1:
        nombre_j1 = nombre
    else:
        nombre_j2 = nombre

def mostrar_historia():
    pantalla.fill((0, 0, 0))
    historia = [
        "Después de los eventos de",
        "Mettaton Madness, el alma del",
        "jugador regresa para enfrentar",
        "una nueva amenaza digital.",
        "",
        "Presiona ESC para volver"
    ]
    for i, linea in enumerate(historia):
        render = fuente.render(linea, True, (255, 255, 255))
        pantalla.blit(render, (60, 80 + i * 35))

def mostrar_creditos():
    pantalla.fill((0, 0, 0))
    creditos = [
        "Creado por:",
        "Jose Daniel Morales Segura",
        "Ricardo Sebastián González Mora",
        "Esteban Mora Matamoros",
        "Josué Geovanny Arias Madrigal",
        "Jeison Daniel Bermúdez Mora",
        "",
        "Presiona ESC para volver"
    ]
    for i, linea in enumerate(creditos):
        render = fuente.render(linea, True, (255, 255, 255))
        pantalla.blit(render, (60, 80 + i * 35))

def mostrar_menu():
    global estado_menu, opcion_actual, en_ejecucion, modo_juego, modo_multijugador
    global salud_maxima, salud2_maxima, volver_a_menu
    menu_activo = True
    estado_menu = "principal"
    opcion_actual = 0
    volver_a_menu = False

    if not pygame.mixer.get_busy():
        musica_menu.play(loops=-1)

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if estado_menu == "principal":
                    if evento.key in [pygame.K_UP, pygame.K_w]:
                        opcion_actual = (opcion_actual - 1) % len(opciones_menu)
                    elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                        opcion_actual = (opcion_actual + 1) % len(opciones_menu)
                    elif evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        seleccion = opciones_menu[opcion_actual]
                        if seleccion == "Un Jugador":
                            modo_juego = "Un Jugador"
                            modo_multijugador = False
                            salud_maxima = 20
                            salud2_maxima = 20
                            seleccionar_dificultad()
                            ingresar_nombre_jugador(1)
                            musica_menu.stop()
                            menu_activo = False
                        elif seleccion == "Multijugador":
                            modo_juego = "Multijugador"
                            modo_multijugador = True
                            salud_maxima = 20
                            salud2_maxima = 20
                            seleccionar_dificultad()
                            ingresar_nombre_jugador(1)
                            ingresar_nombre_jugador(2)
                            musica_menu.stop()
                            menu_activo = False
                        elif seleccion == "Historia":
                            estado_menu = "historia"
                        elif seleccion == "Créditos":
                            estado_menu = "creditos"
                        elif seleccion == "Salir":
                            pygame.quit()
                            exit()
                else:
                    if evento.key == pygame.K_ESCAPE:
                        estado_menu = "principal"

        if estado_menu == "principal":
            mostrar_menu_pantalla()
        elif estado_menu == "historia":
            mostrar_historia()
        elif estado_menu == "creditos":
            mostrar_creditos()

        pygame.display.update()
#endregion

#region Jugadores, balas, enemigos, colisiones
icono_jugador = pygame.image.load("YellowHeart.png").convert_alpha()
icono_jugador = pygame.transform.scale(icono_jugador, (35, 35))
ancho_heart = icono_jugador.get_width()
icono_bala = pygame.image.load("HeartBullet.png").convert_alpha()
icono_bala = pygame.transform.scale(icono_bala, (30, 30))
sonido_disparo = mixer.Sound("mus_sfx_a_bullet.wav")
sonido_disparo.set_volume(0.4)
sonido_muerte = mixer.Sound("mus_sfx_a_lithit.wav")
sonido_muerte.set_volume(0.2)
sonido_felicitacion = mixer.Sound("mus_mett_cheer.ogg")
sonido_felicitacion.set_volume(0.5)
sonido_derrota = mixer.Sound("mus_wawa.ogg")
sonido_derrota.set_volume(0.5)
sonido_victoria_equivocada = mixer.Sound("snd_wrongvictory.wav")
sonido_victoria_equivocada.set_volume(0.5)
jugador_x = 368
jugador_y = 520
jugador_x_cambio = 0
jugador_y_cambio = 0
invulnerable = False
tiempo_invulnerabilidad = 0
duracion_invulnerabilidad = 3000  # ms
sonido_dano = mixer.Sound("snd_hurt1.wav")
sonido_dano.set_volume(0.6)
sonido_pausa = mixer.Sound("snd_item.wav")
sonido_pausa.set_volume(0.5)

# Jugador 2 (corazón rojo)
icono_jugador2 = pygame.image.load("RedHeart.png").convert_alpha()
icono_jugador2 = pygame.transform.scale(icono_jugador2, (35, 35))
jugador2_x = 400
jugador2_y = 520
jugador2_x_cambio = 0
jugador2_y_cambio = 0
jugador2_atacando = False
tiempo_ultimo_ataque = 0
indice_animacion_ataque = 0
invulnerable_jugador2 = False
tiempo_invulnerabilidad_jugador2 = 0

# Sprites de ataque del jugador 2
ataque_sprites = []
sprite_sheet = pygame.image.load("RedAttackSprites.png").convert_alpha()
for _ in range(6):
    num_sprites = 6
    sprite_width = 30
    sprite_height = 108
    for i in range(num_sprites):
        frame = sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
        ataque_sprites.append(pygame.transform.scale(frame, (48, 96)))

ataque_frame = 0
DURACION_ATAQUE_MS = 500
DURACION_FRAME = max(1, DURACION_ATAQUE_MS // max(1, len(ataque_sprites)))
ultimo_cambio_frame = 0

ALCANCE_ATAQUE_MS = 60
ALCANCE_ATAQUE_J2 = 80
HITBOX_J2_REDUCIDO = 18
ATAQUE_FRAME_HIT = 2
ataque_hit_done = False

def jugador(x, y):
    if jugador1_activo:
        pantalla.blit(icono_jugador, (x, y))
    elif jugador2_activo:
        jugador2(x, y)

def jugador2(x, y):
    if jugador2_atacando:
        idx = min(ataque_frame, len(ataque_sprites) - 1)
        pantalla.blit(ataque_sprites[idx], (x - 6, y - 60))
    else:
        if esta_invulnerable_jugador2():
            tiempo_actual = pygame.time.get_ticks()
            if (tiempo_actual // 150) % 2 == 0:  # Parpadeo
                pantalla.blit(icono_jugador2, (x, y))
        else:
            pantalla.blit(icono_jugador2, (x, y))

# Balas
balas = []

def disparar_bala(x, y):
    if jugador2_activo:
        return
    for bala in balas:
        pantalla.blit(icono_bala, (bala["x"] + (ancho_heart // 2) - (icono_bala.get_width() // 2), bala["y"]))

# Enemigos
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
estado_explosion = []
tiempo_explosion = []
icono_enemigo = []
cantidad_enemigos = 8  # enemigos en pantalla

TIEMPO_EXPLOSION = 20

imagen_mini_mettaton = pygame.image.load("MiniMettaton.png")
imagen_mini_mettaton = pygame.transform.scale(imagen_mini_mettaton, (50, 50))
enemigo_ancho = imagen_mini_mettaton.get_width()
enemigo_alto = imagen_mini_mettaton.get_height()

for e in range(cantidad_enemigos):
    icono_enemigo.append(imagen_mini_mettaton.copy())
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(0, 200))
    enemigo_x_cambio.append(3.5)
    enemigo_y_cambio.append(3.5)
    estado_explosion.append(False)
    tiempo_explosion.append(0)

def controla_enemigo(x, y, ene):
    pantalla.blit(icono_enemigo[ene], (x, y))

# Invulnerabilidad
def esta_invulnerable():
    return invulnerable and (pygame.time.get_ticks() - tiempo_invulnerabilidad < duracion_invulnerabilidad)

def esta_invulnerable_jugador2():
    return invulnerable_jugador2 and (pygame.time.get_ticks() - tiempo_invulnerabilidad_jugador2 < duracion_invulnerabilidad)

# Colisiones
def hay_colision(x1, y1, x2, y2, umbral=25):
    distancia = math.hypot(x1 - x2, y1 - y2)
    return distancia < umbral
#endregion

# --------- HELPERS DE ESTADÍSTICAS ----------
def _fmt_tiempo(segundos):
    segundos = max(0, int(segundos))
    m, s = divmod(segundos, 60)
    return f"{m:02d}:{s:02d}"

def _registrar_fin_de_vida(j):
    global vidas_perdidas_j1, vidas_perdidas_j2
    global enemigos_por_vida_j1, enemigos_por_vida_j2, puntos_por_vida_j1, puntos_por_vida_j2
    global kills_vida_actual_j1, kills_vida_actual_j2, puntos_vida_actual_j1, puntos_vida_actual_j2
    global record_por_vida_j1, record_por_vida_j2

    if j == 1:
        vidas_perdidas_j1 += 1
        enemigos_por_vida_j1.append(kills_vida_actual_j1)
        puntos_por_vida_j1.append(puntos_vida_actual_j1)
        record_por_vida_j1 = max(record_por_vida_j1, puntos_vida_actual_j1)
        kills_vida_actual_j1 = 0
        puntos_vida_actual_j1 = 0
    else:
        vidas_perdidas_j2 += 1
        enemigos_por_vida_j2.append(kills_vida_actual_j2)
        puntos_por_vida_j2.append(puntos_vida_actual_j2)
        record_por_vida_j2 = max(record_por_vida_j2, puntos_vida_actual_j2)
        kills_vida_actual_j2 = 0
        puntos_vida_actual_j2 = 0

def _listas_con_vida_actual(lista, actual):
    """Devuelve una copia de lista con el valor 'actual' añadido si > 0 (para mostrar la vida que no se perdió)."""
    lst = list(lista)
    if actual > 0:
        lst = lst + [actual]
    return lst

def _mostrar_resumen_final():
    total_seg = (pygame.time.get_ticks() - tiempo_inicio_partida) / 1000.0
    total_txt = _fmt_tiempo(int(total_seg))

    pantalla.fill((0,0,0))
    titulo = fuente_final.render("RESUMEN DE PARTIDA", True, (255,255,0))
    pantalla.blit(titulo, ((800 - titulo.get_width()) // 2, 40))

    y = 100
    esp = 26

    # Panel J1
    pantalla.blit(icono_jugador, (60, y-6))
    nom1 = nombre_j1 if nombre_j1 else "Jugador 1"
    pantalla.blit(fuente.render(f"{nom1}", True, (255,255,255)), (100, y))
    y += esp
    pantalla.blit(fuente.render(f"a) Vidas perdidas: {vidas_perdidas_j1}", True, (200,200,200)), (60, y)); y += esp
    pantalla.blit(fuente.render(f"b) Adversarios eliminados: {enemigos_total_j1}", True, (200,200,200)), (60, y)); y += esp
    pantalla.blit(fuente.render(f"c) Tiempo total: {total_txt}", True, (200,200,200)), (60, y)); y += esp
    pantalla.blit(fuente.render(f"d) Récord global: {record_j1}", True, (200,200,200)), (60, y)); y += esp

    # e) récord por vida y desglose (incluye vida actual si no se perdió)
    puntos_j1_show = _listas_con_vida_actual(puntos_por_vida_j1, puntos_vida_actual_j1)
    kills_j1_show  = _listas_con_vida_actual(enemigos_por_vida_j1, kills_vida_actual_j1)
    rec_vida_j1 = max([0] + puntos_j1_show)
    pantalla.blit(fuente.render(f"e) Récord por vida: {rec_vida_j1}", True, (200,200,200)), (60, y)); y += esp
    pantalla.blit(fuente.render(f"   Puntos por vida: {puntos_j1_show}", True, (180,180,180)), (60, y)); y += esp
    pantalla.blit(fuente.render(f"   Eliminados por vida: {kills_j1_show}", True, (180,180,180)), (60, y)); y += esp

    # Si hay J2
    if modo_juego == "Multijugador":
        y += 10
        pantalla.blit(icono_jugador2, (60, y-6))
        nom2 = nombre_j2 if nombre_j2 else "Jugador 2"
        pantalla.blit(fuente.render(f"{nom2}", True, (255,255,255)), (100, y))
        y += esp
        pantalla.blit(fuente.render(f"a) Vidas perdidas: {vidas_perdidas_j2}", True, (200,200,200)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"b) Adversarios eliminados: {enemigos_total_j2}", True, (200,200,200)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"c) Tiempo total: {total_txt}", True, (200,200,200)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"d) Récord global: {record_j2}", True, (200,200,200)), (60, y)); y += esp

        puntos_j2_show = _listas_con_vida_actual(puntos_por_vida_j2, puntos_vida_actual_j2)
        kills_j2_show  = _listas_con_vida_actual(enemigos_por_vida_j2, kills_vida_actual_j2)
        rec_vida_j2 = max([0] + puntos_j2_show)
        pantalla.blit(fuente.render(f"e) Récord por vida: {rec_vida_j2}", True, (200,200,200)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"   Puntos por vida: {puntos_j2_show}", True, (180,180,180)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"   Eliminados por vida: {kills_j2_show}", True, (180,180,180)), (60, y)); y += esp

    y += 10
    # Pie con la nueva opción E
    linea = "Presiona Y=reintentar, M=menú, N=salir, E=estadísticas"
    pantalla.blit(fuente.render(linea, True, (255,255,255)), ((800 - 8*len(linea))//2, y))

def mostrar_estadisticas():
    """Pantalla de estadísticas por jugador (accesible con E desde victoria o game over)."""
    mostrando = True
    while mostrando:
        total_seg = (pygame.time.get_ticks() - tiempo_inicio_partida) / 1000.0
        total_txt = _fmt_tiempo(int(total_seg))

        pantalla.fill((0,0,0))
        titulo = fuente_final.render("ESTADÍSTICAS POR JUGADOR", True, (255,255,0))
        pantalla.blit(titulo, ((800 - titulo.get_width()) // 2, 40))

        y = 90
        esp = 24

        # Bloque de tiempo general
        pantalla.blit(fuente.render(f"Tiempo total: {total_txt}", True, (200,200,200)), (60, y)); y += esp + 6

        # J1
        pantalla.blit(icono_jugador, (60, y-6))
        nom1 = nombre_j1 if nombre_j1 else "Jugador 1"
        pantalla.blit(fuente.render(nom1, True, (255,255,255)), (100, y)); y += esp
        pantalla.blit(fuente.render(f"Vidas perdidas: {vidas_perdidas_j1}", True, (200,200,200)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"Eliminados: {enemigos_total_j1}", True, (200,200,200)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"Récord global: {record_j1}", True, (200,200,200)), (60, y)); y += esp

        puntos_j1_show = _listas_con_vida_actual(puntos_por_vida_j1, puntos_vida_actual_j1)
        kills_j1_show  = _listas_con_vida_actual(enemigos_por_vida_j1, kills_vida_actual_j1)
        rec_vida_j1 = max([0] + puntos_j1_show)
        pantalla.blit(fuente.render(f"Récord por vida: {rec_vida_j1}", True, (200,200,200)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"Puntos por vida: {puntos_j1_show}", True, (180,180,180)), (60, y)); y += esp
        pantalla.blit(fuente.render(f"Kills por vida:  {kills_j1_show}", True, (180,180,180)), (60, y)); y += esp

        # J2 si aplica
        if modo_juego == "Multijugador":
            y += 10
            pantalla.blit(icono_jugador2, (60, y-6))
            nom2 = nombre_j2 if nombre_j2 else "Jugador 2"
            pantalla.blit(fuente.render(nom2, True, (255,255,255)), (100, y)); y += esp
            pantalla.blit(fuente.render(f"Vidas perdidas: {vidas_perdidas_j2}", True, (200,200,200)), (60, y)); y += esp
            pantalla.blit(fuente.render(f"Eliminados: {enemigos_total_j2}", True, (200,200,200)), (60, y)); y += esp
            pantalla.blit(fuente.render(f"Récord global: {record_j2}", True, (200,200,200)), (60, y)); y += esp

            puntos_j2_show = _listas_con_vida_actual(puntos_por_vida_j2, puntos_vida_actual_j2)
            kills_j2_show  = _listas_con_vida_actual(enemigos_por_vida_j2, kills_vida_actual_j2)
            rec_vida_j2 = max([0] + puntos_j2_show)
            pantalla.blit(fuente.render(f"Récord por vida: {rec_vida_j2}", True, (200,200,200)), (60, y)); y += esp
            pantalla.blit(fuente.render(f"Puntos por vida: {puntos_j2_show}", True, (180,180,180)), (60, y)); y += esp
            pantalla.blit(fuente.render(f"Kills por vida:  {kills_j2_show}", True, (180,180,180)), (60, y)); y += esp

        # Pie y control
        pie = "Volver: ESC o B"
        pantalla.blit(fuente.render(pie, True, (255,255,255)), ((800 - 8*len(pie))//2, 560))

        pygame.display.update()
        pygame.time.Clock().tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                mostrando = False
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_ESCAPE, pygame.K_b]:
                    mostrando = False
# -------------------------------------------

#region Bucle principal del juego
def jugar():
    global puntaje_j1, puntaje_j2, salud, jugador_x, jugador_y, jugador2_x, jugador2_y, balas, enemigos_eliminados, record_j1, record_j2
    global nivel, enemigos_por_nivel
    global en_ejecucion, volver_a_menu, en_pausa, mostrar_play, tiempo_play
    global invulnerable, tiempo_invulnerabilidad
    global enemigo_x, enemigo_y, estado_explosion, enemigo_x_cambio, enemigo_y_cambio
    global danio_enemigo, salud_maxima
    global jugador2_atacando, ataque_frame, ataque_tiempo
    global jugador1_activo, jugador2_activo
    global salud2, salud2_maxima
    global invulnerable_jugador2, tiempo_invulnerabilidad_jugador2
    global ultimo_cambio_frame
    global ataque_en_progreso, ataque_hit_done
    global tiempo_inicio_partida, tiempo_inicio_vida_j1, tiempo_inicio_vida_j2
    global vidas_perdidas_j1, vidas_perdidas_j2
    global enemigos_total_j1, enemigos_total_j2
    global enemigos_por_vida_j1, enemigos_por_vida_j2, puntos_por_vida_j1, puntos_por_vida_j2
    global kills_vida_actual_j1, kills_vida_actual_j2, puntos_vida_actual_j1, puntos_vida_actual_j2
    global record_por_vida_j1, record_por_vida_j2

    if dificultad == "Principiante":
        danio_enemigo = 3
    elif dificultad == "Normal":
        danio_enemigo = 4
    elif dificultad == "Leyenda":
        danio_enemigo = 5
    elif dificultad == "Volver al Menú":
        mostrar_menu()

    en_ejecucion = True
    en_pausa = False
    mostrar_play = False
    tiempo_play = 0

    # asegurar máximas
    salud_maxima = 20
    salud2_maxima = 20

    # Reiniciar jugadores
    jugador1_activo = True
    jugador2_activo = False

    salud = salud_maxima
    salud2 = salud2_maxima
    jugador_x = 368
    jugador_y = 520
    jugador2_x = 400
    jugador2_y = 520
    invulnerable = False
    tiempo_invulnerabilidad = 0
    invulnerable_jugador2 = False
    tiempo_invulnerabilidad_jugador2 = 0
    ultimo_cambio_frame = 0

    puntaje_j1 = 0
    puntaje_j2 = 0
    enemigos_eliminados = 0
    balas.clear()

    volver_a_menu = False

    # Reiniciar enemigos
    for i in range(cantidad_enemigos):
        enemigo_x[i] = random.randint(0, 736)
        enemigo_y[i] = random.randint(0, 200)
        enemigo_x_cambio[i] = 3.5
        enemigo_y_cambio[i] = 3.5
        estado_explosion[i] = False
        tiempo_explosion[i] = 0

    # --- INICIO TRACKING ---
    tiempo_inicio_partida = pygame.time.get_ticks()
    tiempo_inicio_vida_j1 = tiempo_inicio_partida
    tiempo_inicio_vida_j2 = tiempo_inicio_partida

    vidas_perdidas_j1 = 0
    vidas_perdidas_j2 = 0

    enemigos_total_j1 = 0
    enemigos_total_j2 = 0

    enemigos_por_vida_j1.clear()
    enemigos_por_vida_j2.clear()
    puntos_por_vida_j1.clear()
    puntos_por_vida_j2.clear()

    kills_vida_actual_j1 = 0
    kills_vida_actual_j2 = 0
    puntos_vida_actual_j1 = 0
    puntos_vida_actual_j2 = 0

    record_por_vida_j1 = 0
    record_por_vida_j2 = 0
    # --- FIN INICIO TRACKING ---

    musica.play(loops=-1)

    while en_ejecucion:
        pantalla.blit(fondo, (0, 0))
        ahora_tiempo = pygame.time.get_ticks()
        if invulnerable and ahora_tiempo - tiempo_invulnerabilidad >= duracion_invulnerabilidad:
            invulnerable = False
        if invulnerable_jugador2 and ahora_tiempo - tiempo_invulnerabilidad_jugador2 >= duracion_invulnerabilidad:
            invulnerable_jugador2 = False
        pygame.draw.rect(pantalla, (255, 255, 255), (2, 2, 796, 596), 10)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_ejecucion = False

            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_ESCAPE, pygame.K_e]:
                    en_pausa = not en_pausa
                    sonido_pausa.play()

            if evento.type == pygame.KEYDOWN:
                if not en_pausa:
                    # Disparo J1
                    if jugador1_activo and evento.key == pygame.K_SPACE:
                        balas.append({"x": jugador_x, "y": jugador_y, "velocidad": -7.5})
                        sonido_disparo.play()

                    # Ataque J2
                    if jugador2_activo and evento.key == pygame.K_RETURN:
                        if not jugador2_atacando and not ataque_en_progreso:
                            globals()['jugador2_atacando'] = True
                            globals()['ataque_en_progreso'] = True
                            globals()['ataque_frame'] = 0
                            globals()['ataque_tiempo'] = pygame.time.get_ticks()
                            globals()['ataque_hit_done'] = False
                            globals()['invulnerable_jugador2'] = True  # invulnerable durante ataque (opcional)
                            globals()['tiempo_invulnerabilidad_jugador2'] = pygame.time.get_ticks()
                            sonido_disparo.play()

        # Teclas pulsadas (movimiento continuo)
        teclas = pygame.key.get_pressed()
        jugador_x_cambio = 0
        jugador_y_cambio = 0
        jugador2_x_cambio = 0
        jugador2_y_cambio = 0

        if teclas[pygame.K_a]:
            jugador_x_cambio = -3.5
        elif teclas[pygame.K_d]:
            jugador_x_cambio = 3.5
        if teclas[pygame.K_w]:
            jugador_y_cambio = -3.5
        elif teclas[pygame.K_s]:
            jugador_y_cambio = 3.5

        if teclas[pygame.K_LEFT]:
            jugador2_x_cambio = -3.5
        elif teclas[pygame.K_RIGHT]:
            jugador2_x_cambio = 3.5
        if teclas[pygame.K_UP]:
            jugador2_y_cambio = -3.5
        elif teclas[pygame.K_DOWN]:
            jugador2_y_cambio = 3.5

        if not en_pausa:
            # Movimiento jugadores
            borde = 10
            if jugador1_activo:
                jugador_x += jugador_x_cambio
                jugador_y += jugador_y_cambio
            elif jugador2_activo:
                jugador2_x += jugador2_x_cambio
                jugador2_y += jugador2_y_cambio

            jugador_x = max(borde, min(jugador_x, 800 - borde - icono_jugador.get_width()))
            jugador_y = max(borde, min(jugador_y, 600 - borde - icono_jugador.get_height()))
            jugador2_x = max(borde, min(jugador2_x, 800 - borde - icono_jugador2.get_width()))
            jugador2_y = max(borde, min(jugador2_y, 600 - borde - icono_jugador2.get_height()))

            # Animación/daño del ataque J2
            if jugador2_atacando:
                ahora = pygame.time.get_ticks()
                if ahora - ultimo_cambio_frame >= DURACION_FRAME:
                    globals()['ataque_frame'] = ataque_frame + 1
                    globals()['ultimo_cambio_frame'] = ahora

                    if ataque_frame == ATAQUE_FRAME_HIT and not ataque_hit_done:
                        for i in range(cantidad_enemigos):
                            if not estado_explosion[i]:
                                enemigo_cx = enemigo_x[i] + enemigo_ancho / 2
                                enemigo_cy = enemigo_y[i] + enemigo_alto / 2
                                jugador2_cx = jugador2_x + icono_jugador2.get_width() / 2
                                jugador2_cy = jugador2_y + icono_jugador2.get_height() / 2

                                if hay_colision(enemigo_cx, enemigo_cy, jugador2_cx, jugador2_cy, umbral=ALCANCE_ATAQUE_J2):
                                    sonido_muerte.play()
                                    estado_explosion[i] = True
                                    enemigo_y[i] = 1000
                                    puntaje_j2 += 1
                                    enemigos_eliminados += 1
                                    # Tracking J2
                                    enemigos_total_j2 += 1
                                    kills_vida_actual_j2 += 1
                                    puntos_vida_actual_j2 += 1
                                    comprobar_subida_nivel()
                        globals()['ataque_hit_done'] = True

                    if ataque_frame >= len(ataque_sprites):
                        globals()['jugador2_atacando'] = False
                        globals()['ataque_frame'] = 0
                        globals()['ataque_hit_done'] = False
                        globals()['ataque_en_progreso'] = False

            # Movimiento balas J1
            for bala in balas[:]:
                bala["y"] += bala["velocidad"]
                if bala["y"] < 0:
                    balas.remove(bala)
                    continue

            # Movimiento/enemigos + colisiones
            incremento_velocidad = (puntaje_j1 + puntaje_j2) * 0.1
            for i in range(cantidad_enemigos):
                velocidad_base = 3.5 + incremento_velocidad
                enemigo_x_cambio[i] = math.copysign(velocidad_base, enemigo_x_cambio[i])
                enemigo_y_cambio[i] = math.copysign(velocidad_base, enemigo_y_cambio[i])

                if estado_explosion[i]:
                    tiempo_explosion[i] += 1
                    if tiempo_explosion[i] > TIEMPO_EXPLOSION:
                        estado_explosion[i] = False
                        tiempo_explosion[i] = 0
                        enemigo_x[i] = random.randint(0, 736)
                        enemigo_y[i] = random.randint(0, 150)
                else:
                    enemigo_x[i] += enemigo_x_cambio[i]
                    enemigo_y[i] += enemigo_y_cambio[i]

                    if enemigo_x[i] <= borde or enemigo_x[i] >= 800 - borde - enemigo_ancho:
                        enemigo_x_cambio[i] *= -1
                    if enemigo_y[i] <= borde or enemigo_y[i] >= 600 - borde - enemigo_alto:
                        enemigo_y_cambio[i] *= -1

                    # Daño al jugador activo por contacto
                    if jugador1_activo and not esta_invulnerable() and hay_colision(enemigo_x[i], enemigo_y[i], jugador_x, jugador_y):
                        salud -= danio_enemigo
                        enemigo_y[i] = random.randint(0, 150)
                        globals()['invulnerable'] = True
                        globals()['tiempo_invulnerabilidad'] = pygame.time.get_ticks()
                        sonido_dano.play()

                    if jugador2_activo and not esta_invulnerable_jugador2() and hay_colision(enemigo_x[i], enemigo_y[i], jugador2_x, jugador2_y):
                        salud2 -= danio_enemigo
                        enemigo_y[i] = random.randint(0, 150)
                        globals()['invulnerable_jugador2'] = True
                        globals()['tiempo_invulnerabilidad_jugador2'] = pygame.time.get_ticks()
                        sonido_dano.play()

                    # Impacto de balas J1
                    for bala in balas[:]:
                        if hay_colision(enemigo_x[i], enemigo_y[i], bala["x"], bala["y"]):
                            try:
                                balas.remove(bala)
                            except:
                                pass
                            sonido_muerte.play()
                            estado_explosion[i] = True
                            enemigo_y[i] = 1000
                            puntaje_j1 += 1
                            enemigos_eliminados += 1
                            # Tracking J1
                            enemigos_total_j1 += 1
                            kills_vida_actual_j1 += 1
                            puntos_vida_actual_j1 += 1

                            comprobar_subida_nivel()

            # Verificar fin de juego
            if modo_juego == "Un Jugador":
                if jugador1_activo and salud <= 0:
                    # Registrar vida J1
                    _registrar_fin_de_vida(1)

                    musica.stop()
                    if puntaje_j1 > record_j1:
                        sonido_felicitacion.play()
                        record_j1 = puntaje_j1
                    elif puntaje_j1 == record_j1:
                        sonido_victoria_equivocada.play()
                    else:
                        sonido_derrota.play()

                    # Bucle de resumen/espera con opción E
                    esperando_respuesta = True
                    while esperando_respuesta:
                        _mostrar_resumen_final()
                        pygame.display.update()
                        pygame.time.Clock().tick(60)

                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                esperando_respuesta = False
                                en_ejecucion = False

                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_y:
                                    resetear_partida_interna()
                                    globals()['salud'] = salud_maxima
                                    globals()['jugador_x'] = 368
                                    globals()['jugador_y'] = 520
                                    balas.clear()
                                    globals()['enemigos_eliminados'] = 0
                                    for i in range(cantidad_enemigos):
                                        enemigo_x[i] = random.randint(0, 736)
                                        enemigo_y[i] = random.randint(0, 200)
                                        estado_explosion[i] = False
                                    musica.play(loops=-1)
                                    esperando_respuesta = False

                                elif evento.key == pygame.K_m:
                                    globals()['record_j1'] = 0
                                    globals()['nivel'] = 1
                                    musica.stop()
                                    musica_menu.play(loops=-1)
                                    esperando_respuesta = False
                                    en_ejecucion = False
                                    globals()['volver_a_menu'] = True

                                elif evento.key == pygame.K_n:
                                    esperando_respuesta = False
                                    en_ejecucion = False
                                    globals()['volver_a_menu'] = False

                                elif evento.key == pygame.K_e:
                                    mostrar_estadisticas()  # NUEVO

                    continue  # salir del loop de esta partida

            elif modo_juego == "Multijugador":
                if jugador1_activo and salud <= 0:
                    _registrar_fin_de_vida(1)

                    if puntaje_j1 > record_j1:
                        sonido_felicitacion.play()
                        record_j1 = puntaje_j1
                    elif puntaje_j1 == record_j1:
                        sonido_victoria_equivocada.play()
                    else:
                        sonido_derrota.play()

                    globals()['jugador1_activo'] = False
                    globals()['jugador2_activo'] = True
                    globals()['salud2'] = salud2_maxima
                    globals()['invulnerable'] = False
                    globals()['invulnerable_jugador2'] = True
                    globals()['tiempo_invulnerabilidad_jugador2'] = pygame.time.get_ticks()
                    balas.clear()
                    pygame.time.wait(1500)
                    continue

                elif jugador2_activo and salud2 <= 0:
                    globals()['jugador2_activo'] = False

                    _registrar_fin_de_vida(2)

                    musica.stop()
                    if puntaje_j2 > record_j2:
                        sonido_felicitacion.play()
                        record_j2 = puntaje_j2
                    elif puntaje_j2 == record_j2:
                        sonido_victoria_equivocada.play()
                    else:
                        sonido_derrota.play()

                    # Bucle de resumen/espera con opción E
                    esperando_respuesta = True
                    while esperando_respuesta:
                        _mostrar_resumen_final()
                        pygame.display.update()
                        pygame.time.Clock().tick(60)

                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                esperando_respuesta = False
                                en_ejecucion = False

                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_y:
                                    resetear_partida_interna()
                                    globals()['salud'] = salud_maxima
                                    globals()['salud2'] = salud2_maxima
                                    globals()['jugador_x'] = 368
                                    globals()['jugador_y'] = 520
                                    balas.clear()
                                    globals()['enemigos_eliminados'] = 0
                                    for i in range(cantidad_enemigos):
                                        enemigo_x[i] = random.randint(0, 736)
                                        enemigo_y[i] = random.randint(0, 200)
                                        estado_explosion[i] = False
                                    musica.play(loops=-1)
                                    esperando_respuesta = False

                                elif evento.key == pygame.K_m:
                                    globals()['record_j1'] = 0
                                    globals()['record_j2'] = 0
                                    globals()['nivel'] = 1
                                    musica.stop()
                                    musica_menu.play(loops=-1)
                                    esperando_respuesta = False
                                    en_ejecucion = False
                                    globals()['volver_a_menu'] = True

                                elif evento.key == pygame.K_n:
                                    esperando_respuesta = False
                                    en_ejecucion = False
                                    globals()['volver_a_menu'] = False

                                elif evento.key == pygame.K_e:
                                    mostrar_estadisticas()  # NUEVO

                    continue  # salir del loop de esta partida

        # Dibujo base
        if jugador1_activo:
            if esta_invulnerable():
                tiempo_actual = pygame.time.get_ticks()
                if (tiempo_actual // 150) % 2 == 0:
                    pantalla.blit(icono_jugador, (jugador_x, jugador_y))
            else:
                pantalla.blit(icono_jugador, (jugador_x, jugador_y))
        elif jugador2_activo:
            jugador2(jugador2_x, jugador2_y)

        for bala in balas:
            disparar_bala(bala["x"], bala["y"])

        for i in range(cantidad_enemigos):
            if not estado_explosion[i]:
                controla_enemigo(enemigo_x[i], enemigo_y[i], i)

        margen_borde = 30
        mostrar_puntaje(margen_borde, margen_borde)
        if jugador1_activo:
            mostrar_barra_salud(margen_borde, margen_borde + 40, salud, salud_maxima)
        else:
            mostrar_barra_salud(margen_borde, margen_borde + 40, salud2, salud2_maxima)
        mostrar_nivel(margen_borde, margen_borde + 80, nivel)

        if en_pausa:
            texto_mensaje = fuente.render("PAUSADO", True, (255, 255, 255))
            pantalla.blit(texto_mensaje, ((800 - texto_mensaje.get_width()) // 2, 280))

        pygame.display.update()
        pygame.time.Clock().tick(60)
#endregion

# Bucle principal del programa
while True:
    mostrar_menu()  # Mostrar el menú
    jugar()         # Iniciar el juego al elegir "Iniciar Juego"
    if volver_a_menu:
        continue
    else:
        break
