class_name Troll
extends Node2D

### Troll de la montaña: NPC jefe que lanza rocas cada cierto tiempo.
### La animación "lanzar" llama a launch_rock() en el momento exacto del lanzamiento.
### Custodia el Cristal del Reino: su cuerpo es sólido y tocarlo quita una vida,
### así que hay que SALTAR por encima de él para llegar al cristal.

const ESCENA_ROCA = preload("res://enemigos/roca.tscn")

@export var espera_min := 2.0
@export var espera_max := 4.5
## Impulso horizontal inicial de la roca (hacia la derecha)
@export var impulso := 120.0
## Máximo de rocas rodando a la vez en todo el nivel
@export var max_rocas := 6
## Si es verdadero el troll mira y lanza hacia la izquierda
@export var mirar_izquierda := false

@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
	add_to_group("furia")
	if mirar_izquierda:
		scale.x = -1.0
	$Timer.timeout.connect(_on_timer_timeout)

## Probabilidad de que la roca sea saltarina (avanza dando botes)
@export var prob_saltarina := 0.3

func launch_rock() -> void:
	var roca: RigidBody2D = ESCENA_ROCA.instantiate()
	roca.saltarina = randf() < prob_saltarina
	var sentido := -1.0 if mirar_izquierda else 1.0
	# la roca se agrega al nivel (no al troll) para que su física sea independiente
	get_parent().add_child(roca)
	roca.global_position = $Cuerpo/Mano.global_position
	roca.linear_velocity = Vector2(impulso * sentido, -40)
	roca.angular_velocity = 6.0 * sentido
	animation_player.play("reposo")

func _on_timer_timeout() -> void:
	$Timer.wait_time = randf_range(espera_min, espera_max)
	# límite de rocas en el nivel: si ya hay muchas, el troll espera su turno
	if get_tree().get_nodes_in_group("rocas").size() >= max_rocas:
		return
	animation_player.play("lanzar")

### Tocar al troll quita una vida
func _on_golpe_body_entered(body: Node2D) -> void:
	if body is Personaje:
		body.damage_received()

### Fase de furia (la activa el GameController en los últimos segundos):
### lanza más rápido, más rocas a la vez y más rocas saltarinas.
func activar_furia() -> void:
	espera_min *= 0.55
	espera_max *= 0.55
	max_rocas += 2
	prob_saltarina = 0.5
	$Rugido.play()
	var t := create_tween()
	for i in 4:
		t.tween_property($Cuerpo, "modulate", Color(1.4, 0.6, 0.6), 0.15)
		t.tween_property($Cuerpo, "modulate", Color(1, 1, 1), 0.15)
	t.tween_property($Cuerpo, "modulate", Color(1.15, 0.85, 0.85), 0.2)
	$Timer.start(0.3)
