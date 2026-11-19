class_name Roca
extends RigidBody2D

### Roca que lanza el troll. Rueda por las plataformas gracias a la física
### (RigidBody2D: gravedad, fricción y rebote los calcula el motor).
### Para que no se acumulen, la roca se desmorona cuando:
###   - lleva demasiado tiempo en el nivel,
###   - se queda atascada (casi quieta) un rato,
###   - golpea al unicornio,
###   - sale de los límites del nivel.

const ROCA_ARDIENTE = preload("res://assets/fantasia/roca_ardiente.png")
const ESCENA_POLVO = preload("res://enemigos/explosion_chispas.tscn")

@export var demasiado_abajo := 800.0
@export var limite_izquierdo := -60.0
@export var limite_derecho := 1220.0
## Segundos máximos que una roca vive en el nivel
@export var max_lifetime := 14.0
## Si va más lento que esto (px/s) se considera atascada
@export var velocidad_atascada := 12.0
## Segundos atascada antes de desmoronarse
@export var tiempo_atascada := 2.5

## Roca saltarina: avanza dando botes (más difícil de esquivar)
var saltarina := false
@export var fuerza_bote := 330.0
var botar := false
var enfriamiento := 0.0

var damage_done := false
var desmoronando := false
var vida := 0.0
var quieta := 0.0

func _ready() -> void:
	add_to_group("rocas")
	if saltarina:
		$Sprite.modulate = Color(0.85, 0.65, 1.2)

### Aplica el bote dentro del paso de física (forma segura de cambiar la velocidad)
func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
	if botar:
		botar = false
		state.linear_velocity.y = -fuerza_bote

func _physics_process(delta: float) -> void:
	if desmoronando:
		return
	vida += delta
	enfriamiento = maxf(0.0, enfriamiento - delta)
	if linear_velocity.length() < velocidad_atascada:
		quieta += delta
	else:
		quieta = 0.0

	var fuera := position.y > demasiado_abajo \
		or global_position.x < limite_izquierdo or global_position.x > limite_derecho
	if fuera:
		queue_free()
	elif vida > max_lifetime or quieta > tiempo_atascada:
		desmoronar()

### Detecta colisión con el unicornio: le quita una vida, se pone al rojo vivo y se rompe
func _on_body_entered(body: Node) -> void:
	# la roca saltarina rebota cada vez que toca el suelo
	if saltarina and not desmoronando and body is StaticBody2D and enfriamiento <= 0.0:
		botar = true
		enfriamiento = 0.5
	if body is Personaje and not damage_done:
		damage_done = true
		$Sprite.texture = ROCA_ARDIENTE
		body.damage_received()
		desmoronar(0.25)

### La roca se rompe en polvo y desaparece (deja de ser peligrosa al instante)
func desmoronar(espera := 0.0) -> void:
	if desmoronando:
		return
	desmoronando = true
	remove_from_group("rocas")
	set_deferred("contact_monitor", false)
	set_deferred("collision_mask", 1)  # ya no daña al unicornio
	if espera > 0.0:
		await get_tree().create_timer(espera, false).timeout
	var polvo: CPUParticles2D = ESCENA_POLVO.instantiate()
	polvo.modulate = Color(0.75, 0.7, 0.8)
	polvo.global_position = global_position
	get_parent().add_child(polvo)
	polvo.emitting = true
	var t := create_tween()
	t.tween_property(self, "scale", Vector2(0.2, 0.2), 0.25)
	t.parallel().tween_property(self, "modulate:a", 0.0, 0.25)
	t.tween_callback(queue_free)
