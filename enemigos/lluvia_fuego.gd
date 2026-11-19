extends Node2D

### Generador de bolas de fuego que caen del cielo en posiciones aleatorias.
### Empieza tras unos segundos y cada vez caen más seguido.

const ESCENA_BOLA = preload("res://enemigos/bola_fuego.tscn")

@export var retraso_inicial := 8.0
@export var x_min := 40.0
@export var x_max := 1110.0
@export var altura := -120.0
@export var espera_inicial := 5.0
@export var espera_minima := 2.0
## En niveles verticales: las bolas nacen por encima de lo que muestra la cámara
@export var seguir_camara := false

var espera := 0.0

const AVISO = preload("res://assets/fantasia/aviso_fuego.png")
## Segundos que se muestra el aviso "!" antes de que caiga la bola
@export var tiempo_aviso := 0.9

func _ready() -> void:
	add_to_group("furia")
	espera = espera_inicial
	$Timer.timeout.connect(_on_timer_timeout)
	$Timer.start(retraso_inicial)

func _on_timer_timeout() -> void:
	_soltar_bola()
	espera = maxf(espera_minima, espera - 0.25)
	$Timer.start(randf_range(espera * 0.6, espera))

### En la furia del troll caen bolas de fuego más seguido
func activar_furia() -> void:
	espera_minima *= 0.6
	espera = maxf(espera_minima, espera * 0.6)
	if $Timer.time_left > 1.5:
		$Timer.start(1.0)

func _soltar_bola() -> void:
	var x := randf_range(x_min, x_max)
	var camara := get_viewport().get_camera_2d()
	# aviso parpadeante en el borde superior de la pantalla
	if camara:
		var aviso := Sprite2D.new()
		aviso.texture = AVISO
		add_child(aviso)
		aviso.global_position = Vector2(x, camara.get_screen_center_position().y - 324.0 + 60.0)
		var t := aviso.create_tween().set_loops(int(tiempo_aviso / 0.3))
		t.tween_property(aviso, "modulate:a", 0.3, 0.15)
		t.tween_property(aviso, "modulate:a", 1.0, 0.15)
		await get_tree().create_timer(tiempo_aviso, false).timeout
		aviso.queue_free()
	var bola: RigidBody2D = ESCENA_BOLA.instantiate()
	var y := altura
	if seguir_camara and camara:
		y = camara.get_screen_center_position().y - 420.0
	bola.position = Vector2(x, y)
	bola.linear_velocity = Vector2(randf_range(-30, 30), 0)
	add_child(bola)
