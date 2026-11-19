class_name Lobo
extends CharacterBody2D

### Lobo sombrío: NPC que patrulla su plataforma y CORRE para atacar
### cuando ve al unicornio cerca y a su misma altura.
### Con el poder del Cristal, si el unicornio le cae encima queda eliminado.

const ESCENA_CHISPAS = preload("res://enemigos/explosion_chispas.tscn")
const SONIDO_PISOTON = preload("res://assets/audio/efectos/golpe.wav")

@export var velocidad_patrulla := 90.0
@export var velocidad_ataque := 230.0
@export var distancia_vision := 320.0
@export var limite_izquierdo := 40.0
@export var limite_derecho := 1110.0
@export var gravity := 1000.0

@onready var sprite: AnimatedSprite2D = $Sprite

var direccion := -1.0
var muerto := false
var objetivo: Node2D

func _ready() -> void:
	objetivo = get_tree().get_first_node_in_group("jugador")

func _physics_process(delta: float) -> void:
	if muerto:
		return
	var vel := velocidad_patrulla
	if _ve_al_jugador():
		direccion = signf(objetivo.global_position.x - global_position.x)
		vel = velocidad_ataque
	if global_position.x < limite_izquierdo:
		if vel == velocidad_ataque and direccion < 0.0:
			vel = 0.0  # no sale de su zona: espera al borde gruñendo
		else:
			direccion = 1.0
	elif global_position.x > limite_derecho:
		if vel == velocidad_ataque and direccion > 0.0:
			vel = 0.0
		else:
			direccion = -1.0

	velocity.x = direccion * vel
	if not is_on_floor():
		velocity.y += gravity * delta
	move_and_slide()

	sprite.flip_h = direccion < 0.0
	sprite.speed_scale = maxf(vel, 30.0) / velocidad_patrulla

func _ve_al_jugador() -> bool:
	if objetivo == null:
		return false
	var dif := objetivo.global_position - global_position
	return absf(dif.y) < 60.0 and absf(dif.x) < distancia_vision and absf(dif.x) > 4.0

func _on_mordida_body_entered(body: Node2D) -> void:
	if not body is Personaje or muerto:
		return
	if body.puede_aplastar(self):
		body.rebotar_sobre_enemigo()
		_eliminar()
	else:
		body.damage_received()

### El lobo queda aplastado y desaparece en una nube de chispas
func _eliminar() -> void:
	muerto = true
	$Mordida.set_deferred("monitoring", false)
	$CollisionShape2D.set_deferred("disabled", true)
	sprite.stop()
	var chispas: CPUParticles2D = ESCENA_CHISPAS.instantiate()
	chispas.modulate = Color(0.7, 0.6, 1.0)
	chispas.global_position = global_position
	get_parent().add_child(chispas)
	chispas.emitting = true
	var sonido := AudioStreamPlayer.new()
	sonido.stream = SONIDO_PISOTON
	sonido.pitch_scale = 1.3
	sonido.volume_db = -3.0
	sonido.finished.connect(sonido.queue_free)
	get_parent().add_child(sonido)
	sonido.play()
	var t := create_tween().set_parallel()
	t.tween_property(sprite, "scale", Vector2(sprite.scale.x * 1.3, sprite.scale.y * 0.25), 0.15)
	t.tween_property(sprite, "position:y", sprite.position.y + 12.0, 0.15)
	t.tween_property(sprite, "modulate:a", 0.0, 0.3)
	t.chain().tween_callback(queue_free)
