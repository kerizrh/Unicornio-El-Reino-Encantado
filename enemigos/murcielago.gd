class_name Murcielago
extends Area2D

### Murciélago de la torre: patrulla volando en ondas y se lanza en picada
### contra el unicornio cuando lo ve cerca. Tras morder se retira un momento.
### Con el poder del Cristal, si el unicornio le cae encima queda eliminado.

@export var ancho_patrulla := 250.0
@export var velocidad := 110.0
@export var vision := 260.0
@export var velocidad_ataque := 175.0
@export var descanso := 2.0

const ESCENA_CHISPAS = preload("res://enemigos/explosion_chispas.tscn")
const SONIDO_PISOTON = preload("res://assets/audio/efectos/rebote.wav")

var muerto := false

@onready var sprite: AnimatedSprite2D = $Sprite

var origen := Vector2.ZERO
var dir := 1.0
var tiempo := 0.0
var cansado := 0.0
var objetivo: Node2D

func _ready() -> void:
	origen = position
	objetivo = get_tree().get_first_node_in_group("jugador")
	body_entered.connect(_on_body_entered)

func _physics_process(delta: float) -> void:
	if muerto:
		return
	tiempo += delta
	cansado = maxf(0.0, cansado - delta)
	var antes := position
	if _ve_al_jugador():
		position += (objetivo.global_position - global_position).normalized() * velocidad_ataque * delta
	else:
		position.x += dir * velocidad * delta
		if position.x > origen.x + ancho_patrulla:
			dir = -1.0
		elif position.x < origen.x - ancho_patrulla:
			dir = 1.0
		position.y = move_toward(position.y, origen.y + sin(tiempo * 3.0) * 22.0, 90.0 * delta)
	if absf(position.x - antes.x) > 0.01:
		sprite.flip_h = position.x < antes.x

func _ve_al_jugador() -> bool:
	return cansado <= 0.0 and objetivo != null \
		and global_position.distance_to(objetivo.global_position) < vision

func _on_body_entered(body: Node2D) -> void:
	if not body is Personaje or muerto:
		return
	# si el unicornio cae desde arriba, aplasta al murciélago y rebota
	if body.puede_aplastar(self):
		body.rebotar_sobre_enemigo()
		_eliminar()
	else:
		body.damage_received()
		cansado = descanso

### El murciélago desaparece en una nube de chispas
func _eliminar() -> void:
	muerto = true
	set_deferred("monitoring", false)
	var chispas: CPUParticles2D = ESCENA_CHISPAS.instantiate()
	chispas.modulate = Color(0.8, 0.6, 1.0)
	chispas.global_position = global_position
	get_parent().add_child(chispas)
	chispas.emitting = true
	# sonido que sigue sonando aunque el murciélago ya no exista
	var sonido := AudioStreamPlayer.new()
	sonido.stream = SONIDO_PISOTON
	sonido.pitch_scale = 1.4
	sonido.volume_db = -4.0
	sonido.finished.connect(sonido.queue_free)
	get_parent().add_child(sonido)
	sonido.play()
	var t := create_tween().set_parallel()
	t.tween_property(sprite, "scale", Vector2(1.4, 0.3), 0.15)
	t.tween_property(sprite, "modulate:a", 0.0, 0.2)
	t.chain().tween_callback(queue_free)
