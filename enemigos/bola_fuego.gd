class_name BolaFuego
extends RigidBody2D

### Bola de fuego que cae del cielo (NPC que "cae").
### Usa la gravedad del motor de físicas; atraviesa las plataformas
### y solo choca con el unicornio.

const ESCENA_CHISPAS = preload("res://enemigos/explosion_chispas.tscn")

@export var demasiado_abajo := 900

func _process(_delta: float) -> void:
	if position.y > demasiado_abajo:
		queue_free()

func _on_body_entered(body: Node) -> void:
	if body is Personaje:
		body.damage_received()
		explotar()

func explotar() -> void:
	var chispas: CPUParticles2D = ESCENA_CHISPAS.instantiate()
	chispas.position = position
	get_parent().add_child(chispas)
	chispas.emitting = true
	queue_free()
