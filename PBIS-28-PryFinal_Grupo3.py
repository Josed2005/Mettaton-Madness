import pygame
import random
import math
from pygame import mixer
#endregion

# Inicialización
pygame.init()
mixer.init()

#region Pantalla y fondo
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mettaton Madness")
icono_ventana = pygame.image.load("MettatonMadness.webp")
pygame.display.set_icon(icono_ventana)

#Fondo negro
fondo = pygame.Surface((800, 600))
fondo.fill((0, 0, 0))

# Música
mixer.init()
musica_menu = mixer.Sound("Start-Menu.mp3")
musica = mixer.Sound("Anticipation.mp3")

musica_menu.play(loops=-1) #Bucle infinito
#endregion

#region Variables globales
puntaje = 0
salud = 20
salud_maxima = 20
salud2 = 20
salud2_maxima = 20
nivel = 1
enemigos_por_nivel = 10
enemigos_eliminados = 0
puntaje = 0
record = 0
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
#endregion

#region Fuente y textos
fuente = pygame.font.Font("PressStart2P-Regular.ttf", 16)
fuente_final = pygame.font.Font("PressStart2P-Regular.ttf", 20)

def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))
    texto_record = fuente.render(f"Récord: {record}", True, (255, 255, 255))
    pantalla.blit(texto_record, (x, y + 20))

def mostrar_barra_salud(x, y, salud_actual, salud_maxima):
    ancho_unitario = 3  # Ajusta el valor si la barra se vuelve muy grande
    altura = 20
    offset_vertical = 3

    ancho_total = int(salud_maxima * ancho_unitario)
    porcentaje = salud_actual / salud_maxima
    ancho_amarillo = int(ancho_total * porcentaje)
    ancho_rojo = ancho_total - ancho_amarillo

    # Dibujar barras
    pygame.draw.rect(pantalla, (255, 0, 0), (x + ancho_amarillo, y, ancho_rojo, altura))
    pygame.draw.rect(pantalla, (255, 255, 0), (x, y, ancho_amarillo, altura))

    # Dibujar texto desplazado al final de la barra
    texto = fuente.render(f"HP: {salud_actual}/{salud_maxima}", True, (255, 255, 255))
    pantalla.blit(texto, (x + ancho_total + 10, y + offset_vertical))

def mostrar_nivel(x, y, nivel):
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, (255, 255, 255))
    pantalla.blit(texto_nivel, (x, y))

def texto_final():
    mensaje = fuente_final.render(f"¡Juego terminado! Puntaje: {puntaje}", True, (255, 255, 255))
    ancho_texto = mensaje.get_width()
    x = (800 - ancho_texto) // 2 - 15
    pantalla.blit(mensaje, (x, 250))
#endregion

#region Menú principal (funciones del menú)
menu_activo = True
en_ejecucion = True
estado_menu = "principal"  # puede ser 'principal', 'historia' o 'creditos'
modo_juego = "Un Jugador"
opciones_menu = ["Un Jugador", "Multijugador", "Historia", "Créditos", "Salir"]
opcion_actual = 0
opciones_dificultad = ["Principiante", "Normal", "Leyenda", "Volver al Menú"]
dificultad_actual = 0
dificultad = "Normal"

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
#endregion

def mostrar_menu():
    global estado_menu, opcion_actual, menu_activo, modo_juego
    menu_activo = True
    estado_menu = "principal"
    opcion_actual = 0

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
                            seleccionar_dificultad()
                            musica_menu.stop()
                            menu_activo = False
                        elif seleccion == "Multijugador":
                            modo_juego = "Multijugador"
                            seleccionar_dificultad()
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

            # Fin de invulnerabilidad del jugador 2 tras 2 segundos
            #if invulnerable_jugador2 and pygame.time.get_ticks() - tiempo_invulnerabilidad_jugador2 > 2000:
                #invulnerable_jugador2 = False

        pygame.display.update()
#endregion

if not en_ejecucion:
    pygame.mixer.quit()
    pygame.quit()
    exit()

#region Jugador (corazón amarillo)
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
duracion_invulnerabilidad = 3000  # en milisegundos (3 segundos)
sonido_dano = mixer.Sound("snd_hurt1.wav")
sonido_dano.set_volume(0.6)
sonido_pausa = mixer.Sound("snd_item.wav")
sonido_pausa.set_volume(0.5)
#opciones_dificultad = ["Principiante", "Normal", "Leyenda"]
#dificultad_actual = 0
#dificultad = "Normal"

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
for i in range(6):
    num_sprites = 6
    sprite_width = 30
    sprite_height = 108

    for i in range(num_sprites):
        frame = sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
        ataque_sprites.append(pygame.transform.scale(frame, (48, 96)))  # Ajuste visual opcional

ataque_frame = 0
DURACION_ATAQUE_MS = 500        # duración total deseada del ataque (1 segundo)
DURACION_FRAME = max(1, DURACION_ATAQUE_MS // max(1, len(ataque_sprites)))
ATAQUE_FRAME_HIT = 2             # índice (0-based) del frame donde "golpea" (ajústalo)
ataque_hit_done = False          # para que el golpe se aplique solo una vez por ataque

def jugador(x, y):
    if jugador1_activo:
        pantalla.blit(icono_jugador, (x, y))
    elif jugador2_activo:
        jugador2(jugador2_x, jugador2_y)

def jugador2(x, y):
    if jugador2_atacando:
        idx = min(ataque_frame, len(ataque_sprites) - 1)
        pantalla.blit(ataque_sprites[idx], (x - 6, y - 60))  # ajusta offset si lo necesitas
    else:
        pantalla.blit(icono_jugador2, (x, y))
#endregion

#region Balas
balas = []

def disparar_bala(x, y):
    if jugador2_activo:
        return
    for bala in balas:
        pantalla.blit(icono_bala, (bala["x"] + (ancho_heart // 2) - (icono_bala.get_width() // 2), bala["y"]))
#endregion

#region Enemigos
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
estado_explosion = []
tiempo_explosion = []
icono_enemigo = []
cantidad_enemigos = 8  # enemigos en pantalla al mismo tiempo

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
#endregion

#region Invulnerabilidad para el jugador cuando reciba daño
def esta_invulnerable():
    return invulnerable and pygame.time.get_ticks() - tiempo_invulnerabilidad < duracion_invulnerabilidad
if jugador2_activo:
    if invulnerable_jugador2:
        tiempo_actual = pygame.time.get_ticks()
        if (tiempo_actual // 150) % 2 == 0:
            jugador2(jugador2_x, jugador2_y)
    else:
        jugador2(jugador2_x, jugador2_y)
#endregion

#region Colisiones
def hay_colision(x1, y1, x2, y2):
    distancia = math.hypot(x1 - x2, y1 - y2)
    return distancia < 30
#endregion

#region Bucle principal
def jugar():
    global puntaje, salud, jugador_x, jugador_y, jugador2_x, jugador2_y, balas, enemigos_eliminados, record
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
    if dificultad == "Principiante":
        danio_enemigo = 3
    elif dificultad == "Normal":
        danio_enemigo = 4
    elif dificultad == "Leyenda":
        danio_enemigo = 5
    elif dificultad == "Volver al Menú":
        mostrar_menu()

        print("Dificultad seleccionada:", dificultad)

        nivel = 1
        enemigos_por_nivel = 10

        print("=== INICIANDO JUEGO ===")
        print(f"jugador1_activo = {jugador1_activo}")
        print(f"jugador2_activo = {jugador2_activo}")
        print(f"salud = {salud}, salud_maxima = {salud_maxima}")
        print(f"salud2 = {salud2}, salud2_maxima = {salud2_maxima}")

    en_ejecucion = True
    en_pausa = False
    mostrar_play = False
    tiempo_play = 0

    # Reiniciar variables importantes del jugador
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

    puntaje = 0
    enemigos_eliminados = 0
    balas.clear()

    volver_a_menu = False

    # Reiniciar enemigos (posiciones y estados)
    for i in range(cantidad_enemigos):
        enemigo_x[i] = random.randint(0, 736)
        enemigo_y[i] = random.randint(0, 200)
        enemigo_x_cambio[i] = 3.5
        enemigo_y_cambio[i] = 3.5
        estado_explosion[i] = False
        tiempo_explosion[i] = 0

    musica.play(loops=-1)

    while en_ejecucion:
        pantalla.blit(fondo, (0, 0))
        pygame.draw.rect(pantalla, (255, 255, 255), (2, 2, 796, 596), 10)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_ejecucion = False

            if evento.type == pygame.KEYDOWN:
                # Disparo de Corazón Amarillo (Jugador 1)
                if not en_pausa:
                    if jugador1_activo and evento.key == pygame.K_SPACE:
                        balas.append({"x": jugador_x, "y": jugador_y, "velocidad": -7.5})
                        sonido_disparo.play()

                    elif jugador2_activo and evento.key == pygame.K_RETURN:
                        if not jugador2_atacando:
                            jugador2_atacando = True
                            ataque_frame = 0
                            ataque_tiempo = pygame.time.get_ticks()
                            ataque_hit_done = False
                            sonido_disparo.play()

                        # Hacer invulnerable por 2 segundos
                        invulnerable_jugador2 = True
                        tiempo_invulnerabilidad_jugador2 = pygame.time.get_ticks()
                        ataque_frame = 0
                        ataque_tiempo = pygame.time.get_ticks()
                        sonido_disparo.play()

                        if jugador2_activo and not invulnerable_jugador2 and hay_colision(enemigo_x[i], enemigo_y[i],
                                                                                          jugador2_x, jugador2_y):
                            salud2 -= danio_enemigo
                            enemigo_y[i] = random.randint(0, 150)
                            invulnerable_jugador2 = True
                            tiempo_invulnerabilidad_jugador2 = pygame.time.get_ticks()
                            sonido_dano.play()

                if jugador2_activo and jugador2_atacando:
                    for i in range(cantidad_enemigos):
                        if not estado_explosion[i]:
                            if hay_colision(enemigo_x[i], enemigo_y[i], jugador2_x, jugador2_y):
                                sonido_muerte.play()
                                estado_explosion[i] = True
                                enemigo_y[i] = 1000
                                puntaje += 1
                                enemigos_eliminados += 1

                # Ataque de Corazón Rojo (Jugador 2)
                if evento.key == pygame.K_RETURN and not jugador2_atacando and not ataque_en_progreso:
                    jugador2_atacando = True
                    ataque_en_progreso = True
                    ataque_frame = 0
                    ataque_tiempo = pygame.time.get_ticks()

                    sonido_disparo.play()

                if evento.type == pygame.KEYDOWN and jugador2_activo and evento.key == pygame.K_RETURN:
                    if not jugador2_atacando:
                        jugador2_atacando = True
                        ataque_frame = 0
                        ataque_tiempo = pygame.time.get_ticks()
                        sonido_disparo.play()

        # Nota: Con esto, se puede controlar el movimiento continuamente con teclas presionadas
        teclas = pygame.key.get_pressed()
        jugador_x_cambio = 0
        jugador_y_cambio = 0
        jugador2_x_cambio = 0
        jugador2_y_cambio = 0

        # Movimiento Jugador 1 - Corazón Amarillo
        if teclas[pygame.K_a]:
            jugador_x_cambio = -3.5
        elif teclas[pygame.K_d]:
            jugador_x_cambio = 3.5
        if teclas[pygame.K_w]:
            jugador_y_cambio = -3.5
        elif teclas[pygame.K_s]:
            jugador_y_cambio = 3.5

        # Movimiento Jugador 2 - Corazón Rojo
        if teclas[pygame.K_LEFT]:
            jugador2_x_cambio = -3.5
        elif teclas[pygame.K_RIGHT]:
            jugador2_x_cambio = 3.5
        if teclas[pygame.K_UP]:
            jugador2_y_cambio = -3.5
        elif teclas[pygame.K_DOWN]:
            jugador2_y_cambio = 3.5

        if not en_pausa:
            # Movimiento jugador
            if jugador1_activo:
                jugador_x += jugador_x_cambio
                jugador_y += jugador_y_cambio
                borde = 10
            elif jugador2_activo:
                jugador2_x += jugador2_x_cambio
                jugador2_y += jugador2_y_cambio
            ancho_jugador = icono_jugador.get_width()
            alto_jugador = icono_jugador.get_height()
            jugador_x = max(borde, min(jugador_x, 800 - borde - icono_jugador.get_width()))
            jugador_y = max(borde, min(jugador_y, 600 - borde - icono_jugador.get_height()))

            jugador2_x += jugador2_x_cambio
            jugador2_y += jugador2_y_cambio
            jugador2_x = max(borde, min(jugador2_x, 800 - borde - icono_jugador2.get_width()))
            jugador2_y = max(borde, min(jugador2_y, 600 - borde - icono_jugador2.get_height()))

            if jugador2_atacando:
                ahora = pygame.time.get_ticks()
                if ahora - ultimo_cambio_frame >= DURACION_FRAME:
                    ataque_frame += 1
                    ultimo_cambio_frame = ahora

                    if ataque_frame == ATAQUE_FRAME_HIT and not ataque_hit_done:
                        # Aplicar daño a enemigos en este frame
                        for i in range(cantidad_enemigos):
                            if not estado_explosion[i]:
                                if hay_colision(enemigo_x[i], enemigo_y[i], jugador2_x, jugador2_y):
                                    sonido_muerte.play()
                                    estado_explosion[i] = True
                                    enemigo_y[i] = 1000
                                    puntaje += 1
                                    enemigos_eliminados += 1
                        ataque_hit_done = True

                    if ataque_frame >= len(ataque_sprites):
                        jugador2_atacando = False
                        ataque_frame = 0
                        ataque_hit_done = False
                        ataque_en_progreso = False


            # Movimiento balas
            for bala in balas[:]:
                bala["y"] += bala["velocidad"]
                if bala["y"] < 0:
                    balas.remove(bala)

            # Aumentar velocidad de enemigos según puntaje
            incremento_velocidad = puntaje * 0.1
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

                    if not esta_invulnerable():
                        if jugador1_activo and hay_colision(enemigo_x[i], enemigo_y[i], jugador_x, jugador_y):
                            salud -= danio_enemigo
                            enemigo_y[i] = random.randint(0, 150)
                            invulnerable = True
                            tiempo_invulnerabilidad = pygame.time.get_ticks()
                            sonido_dano.play()


                        elif jugador2_activo and not invulnerable_jugador2 and hay_colision(enemigo_x[i], enemigo_y[i], jugador2_x, jugador2_y):
                            salud2 -= danio_enemigo
                            enemigo_y[i] = random.randint(0, 150)
                            invulnerable = True
                            tiempo_invulnerabilidad = pygame.time.get_ticks()
                            sonido_dano.play()

                    for bala in balas:
                        if hay_colision(enemigo_x[i], enemigo_y[i], bala["x"], bala["y"]):
                            try:
                                balas.remove(bala)
                            except:
                                pass
                            sonido_muerte.play()
                            estado_explosion[i] = True
                            enemigo_y[i] = 1000
                            puntaje += 1
                            enemigos_eliminados += 1
                            # Avanzar de nivel cuando se eliminan suficientes enemigos
                            if enemigos_eliminados >= enemigos_por_nivel:
                                if nivel == 3:
                                    # Fin del juego al completar el nivel 3
                                    musica.stop()
                                    sonido_felicitacion.play()

                                    texto_victoria = fuente_final.render("¡Has completado el juego!",True,(255, 255, 0))
                                    pantalla.blit(texto_victoria, ((800 - texto_victoria.get_width()) // 2, 250))
                                    pygame.display.update()
                                    pygame.time.wait(2500)

                                    # Mostrar pantalla de final como si fuera una derrota, pero es victoria
                                    esperando_respuesta = True
                                    while esperando_respuesta:
                                        pantalla.fill((0, 0, 0))
                                        mensaje0 = fuente.render(f"Puntaje: {puntaje}", True, (255,255,255))
                                        mensaje1 = fuente.render("¿Qué deseas hacer?", True, (255, 255, 255))
                                        mensaje2 = fuente.render("Y = Reintentar", True, (255, 255, 255))
                                        mensaje3 = fuente.render("M = Menú Principal", True, (255, 255, 255))
                                        mensaje4 = fuente.render("N = Salir", True, (255, 255, 255))

                                        pantalla.blit(mensaje0, ((800 - mensaje0.get_width()) // 2, 210))
                                        pantalla.blit(mensaje1, ((800 - mensaje1.get_width()) // 2, 250))
                                        pantalla.blit(mensaje2, ((800 - mensaje2.get_width()) // 2, 290))
                                        pantalla.blit(mensaje3, ((800 - mensaje3.get_width()) // 2, 330))
                                        pantalla.blit(mensaje4, ((800 - mensaje4.get_width()) // 2, 370))

                                        pygame.display.update()

                                        for evento in pygame.event.get():
                                            if evento.type == pygame.QUIT:
                                                esperando_respuesta = False
                                                en_ejecucion = False

                                            if evento.type == pygame.KEYDOWN:
                                                if evento.key == pygame.K_y:
                                                    puntaje = 0
                                                    salud = salud_maxima
                                                    jugador_x = 368
                                                    jugador_y = 520
                                                    balas.clear()
                                                    enemigos_eliminados = 0
                                                    nivel = 1
                                                    enemigos_por_nivel = 10
                                                    for i in range(cantidad_enemigos):
                                                        enemigo_x[i] = random.randint(0, 736)
                                                        enemigo_y[i] = random.randint(0, 200)
                                                        estado_explosion[i] = False
                                                    musica.play(loops=-1)
                                                    esperando_respuesta = False

                                                elif evento.key == pygame.K_m:
                                                    musica_menu.play(loops=-1)
                                                    esperando_respuesta = False
                                                    en_ejecucion = False
                                                    volver_a_menu = True

                                                elif evento.key == pygame.K_n:
                                                    esperando_respuesta = False
                                                    en_ejecucion = False
                                    continue

                                # Si no es el nivel 3, seguir normalmente
                                nivel += 1
                                enemigos_eliminados = 0
                                enemigos_por_nivel += 5

                                salud += 10
                                if salud > salud_maxima:
                                    salud = salud_maxima

                                for i in range(cantidad_enemigos):
                                    enemigo_x_cambio[i] *= 1.1
                                    enemigo_y_cambio[i] *= 1.1

                                texto_nivel = fuente.render(f"Nivel {nivel - 1} completado. ¡Nivel {nivel}!", True,
                                                            (255, 255, 0))
                                pantalla.blit(texto_nivel, ((800 - texto_nivel.get_width()) // 2, 280))
                                pygame.display.update()
                                pygame.time.wait(2000)

                                # Aumentar salud y salud máxima
                                salud_maxima += 10
                                salud = min(salud + 10, salud_maxima)

                                # Aumentar velocidad de enemigos ligeramente
                                for i in range(cantidad_enemigos):
                                    enemigo_x_cambio[i] *= 1.1
                                    enemigo_y_cambio[i] *= 1.1

                                # Mostrar mensaje de nivel completado
                                texto_nivel = fuente.render(f"Nivel {nivel - 1} completado. ¡Nivel {nivel}!", True,
                                                            (255, 255, 0))
                                pantalla.blit(texto_nivel, ((800 - texto_nivel.get_width()) // 2, 280))
                                pygame.display.update()
                                pygame.time.wait(2000)

                                # Preparar aparición de jefe en nivel 3 (más adelante)
                                if nivel == 3:
                                    # Aquí luego invocar una función tipo `iniciar_boss()`
                                    print("Nivel 3 alcanzado - se activará el jefe (pendiente de implementar)")

            # Verificar si terminó el juego
            if modo_juego == "Un Jugador":
                if jugador1_activo and salud <= 0:
                    print("Jugador 1 ha muerto.")
                    musica.stop()
                    if puntaje > record:
                        sonido_felicitacion.play()
                        record = puntaje
                    elif puntaje == record:
                        sonido_victoria_equivocada.play()
                    else:
                        sonido_derrota.play()

                    for bala in balas:
                        disparar_bala(bala["x"], bala["y"])

                    for i in range(cantidad_enemigos):
                        if not estado_explosion[i]:
                            controla_enemigo(enemigo_x[i], enemigo_y[i], i)

                    if esta_invulnerable():
                        tiempo_actual = pygame.time.get_ticks()
                        if (tiempo_actual // 150) % 2 == 0:
                            jugador(jugador_x, jugador_y)
                    else:
                        jugador(jugador_x, jugador_y)

                    texto_final()
                    pygame.display.update()
                    pygame.time.wait(2000)

                    esperando_respuesta = True
                    while esperando_respuesta:
                        pantalla.fill((0, 0, 0))
                        mensaje1 = fuente.render("¿Qué deseas hacer?", True, (255, 255, 255))
                        mensaje2 = fuente.render("Y = Reintentar", True, (255, 255, 255))
                        mensaje3 = fuente.render("M = Menú Principal", True, (255, 255, 255))
                        mensaje4 = fuente.render("N = Salir", True, (255, 255, 255))

                        pantalla.blit(mensaje1, ((800 - mensaje1.get_width()) // 2, 250))
                        pantalla.blit(mensaje2, ((800 - mensaje2.get_width()) // 2, 290))
                        pantalla.blit(mensaje3, ((800 - mensaje3.get_width()) // 2, 330))
                        pantalla.blit(mensaje4, ((800 - mensaje4.get_width()) // 2, 370))

                        pygame.display.update()

                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                esperando_respuesta = False
                                en_ejecucion = False

                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_y:
                                    # Reintentar
                                    puntaje = 0
                                    salud = salud_maxima
                                    jugador_x = 368
                                    jugador_y = 520
                                    balas.clear()
                                    enemigos_eliminados = 0
                                    for i in range(cantidad_enemigos):
                                        enemigo_x[i] = random.randint(0, 736)
                                        enemigo_y[i] = random.randint(0, 200)
                                        estado_explosion[i] = False
                                    musica.play(loops=-1)
                                    esperando_respuesta = False

                                elif evento.key == pygame.K_m:
                                    # Volver al menú
                                    musica.stop()
                                    musica_menu.play(loops=-1)
                                    esperando_respuesta = False
                                    en_ejecucion = False
                                    volver_a_menu = True

                                elif evento.key == pygame.K_n:
                                    # Salir del juego
                                    esperando_respuesta = False
                                    en_ejecucion = False
            elif modo_juego == "Multijugador":
                if jugador1_activo and salud <= 0:
                    print("Jugador 1 ha muerto. Activando Jugador 2...")
                    jugador1_activo = False
                    jugador2_activo = True
                    salud2 = salud2_maxima
                    jugador2_x, jugador2_y = 400, 500
                    balas.clear()
                    pygame.time.wait(1500)
                    continue

                elif jugador2_activo and salud2 <= 0:
                    print("Jugador 2 ha muerto. Fin del juego.")
                    jugador2_activo = False
                    en_ejecucion = False
                    volver_a_menu = True
                    continue  # Esto previene que el resto del bucle se ejecute

                    if jugador1_activo:
                        jugador1_activo = False
                        jugador2_activo = True
                        jugador2_x, jugador2_y = 400, 500
                        balas.clear()
                        pygame.time.wait(1500)  # Pequeña pausa para el cambio de turno
                        continue
                    elif jugador2_activo:
                            jugador2_activo = False
                            en_ejecucion = False  # Ambos jugadores muertos → fin del juego
                            volver_a_menu = True

                    musica.stop()
                    if puntaje > record:
                        sonido_felicitacion.play()
                        record = puntaje
                    elif puntaje == record:
                        sonido_victoria_equivocada.play()
                    else:
                        sonido_derrota.play()

                    for bala in balas:
                        disparar_bala(bala["x"], bala["y"])

                    for i in range(cantidad_enemigos):
                        if not estado_explosion[i]:
                            controla_enemigo(enemigo_x[i], enemigo_y[i], i)

                    if esta_invulnerable():
                        tiempo_actual = pygame.time.get_ticks()
                        if (tiempo_actual // 150) % 2 == 0:
                            jugador(jugador_x, jugador_y)
                    else:
                        jugador(jugador_x, jugador_y)

                    texto_final()
                    pygame.display.update()
                    pygame.time.wait(2000)

                    esperando_respuesta = True
                    while esperando_respuesta:
                        pantalla.fill((0, 0, 0))
                        mensaje1 = fuente.render("¿Qué deseas hacer?", True, (255, 255, 255))
                        mensaje2 = fuente.render("Y = Reintentar", True, (255, 255, 255))
                        mensaje3 = fuente.render("M = Menú Principal", True, (255, 255, 255))
                        mensaje4 = fuente.render("N = Salir", True, (255, 255, 255))

                        pantalla.blit(mensaje1, ((800 - mensaje1.get_width()) // 2, 250))
                        pantalla.blit(mensaje2, ((800 - mensaje2.get_width()) // 2, 290))
                        pantalla.blit(mensaje3, ((800 - mensaje3.get_width()) // 2, 330))
                        pantalla.blit(mensaje4, ((800 - mensaje4.get_width()) // 2, 370))

                        pygame.display.update()

                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                esperando_respuesta = False
                                en_ejecucion = False

                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_y:
                                    # Reintentar
                                    puntaje = 0
                                    salud = salud_maxima
                                    jugador_x = 368
                                    jugador_y = 520
                                    balas.clear()
                                    enemigos_eliminados = 0
                                    for i in range(cantidad_enemigos):
                                        enemigo_x[i] = random.randint(0, 736)
                                        enemigo_y[i] = random.randint(0, 200)
                                        estado_explosion[i] = False
                                    musica.play(loops=-1)
                                    esperando_respuesta = False

                                elif evento.key == pygame.K_m:
                                    # Volver al menú
                                    musica.stop()
                                    musica_menu.play(loops=-1)
                                    esperando_respuesta = False
                                    en_ejecucion = False
                                    volver_a_menu = True

                                elif evento.key == pygame.K_n:
                                    # Salir del juego
                                    esperando_respuesta = False
                                    en_ejecucion = False


        # Mostrar siempre: jugador, enemigos, balas
        if esta_invulnerable():
            tiempo_actual = pygame.time.get_ticks()
            if (tiempo_actual // 150) % 2 == 0:
                jugador(jugador_x, jugador_y)
        else:
            jugador(jugador_x, jugador_y)

        for bala in balas:
            disparar_bala(bala["x"], bala["y"])

        for i in range(cantidad_enemigos):
            if not estado_explosion[i]:
                controla_enemigo(enemigo_x[i], enemigo_y[i], i)
        # Si bien no hay un fondo, hay bordes blancos para que haga entender al jugador que hay una especie de zona de combate
        margen_borde = 30
        mostrar_puntaje(margen_borde, margen_borde)
        if jugador1_activo:
            mostrar_barra_salud(margen_borde, margen_borde + 40, salud, salud_maxima)
        else:
            mostrar_barra_salud(margen_borde, margen_borde + 40, salud2, salud2_maxima)
        mostrar_nivel(margen_borde, margen_borde + 80, nivel)


        # Mostrar pausa
        if en_pausa:
            texto_mensaje = fuente.render("PAUSADO", True, (255, 255, 255))
            pantalla.blit(texto_mensaje, ((800 - texto_mensaje.get_width()) // 2, 280))

        pygame.display.update()
        pygame.time.Clock().tick(60)

def mostrar_menu_pantalla():
    pantalla.fill((0, 0, 0))
    titulo = fuente.render("Mettaton Madness: Rebooted", True, (255, 255, 255))
    pantalla.blit(titulo, ((800 - titulo.get_width()) // 2, 80))

    for i, texto in enumerate(opciones_menu):
        color = (255, 255, 255) if i == opcion_actual else (180, 180, 180)
        render = fuente.render(texto, True, color)
        pantalla.blit(render, ((800 - render.get_width()) // 2, 180 + i * 40))

# Bucle principal del programa
while True:
    mostrar_menu()  # Mostrar el menú
    jugar()         # Iniciar el juego al elegir "Iniciar Juego"
    if volver_a_menu:
        continue
    else:
        break

