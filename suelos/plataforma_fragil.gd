extends StaticBody2D

### Cristal frágil: al PARARSE encima tiembla, se rompe y cae.
### Mientras está roto se ve su silueta, y reaparece con un destello.

@export var tiempo_aviso := 1.0
@export var tiempo_reaparecer := 2.0

@onready var sprite: Sprite2D = $Sprite
@onready var forma: CollisionShape2D = $CollisionShape2D

var rompiendo := false

func _physics_process(_delta: float) -> void:
	if rompiendo:
		return
	# solo se rompe si el unicornio está PARADO encima (no al atravesarlo saltando)
	for cuerpo in $Sensor.get_overlapping_bodies():
		if cuerpo is Personaje and cuerpo.is_on_floor() and cuerpo.global_position.y < global_position.y:
			_romper()
			return

func _romper() -> void:
	rompiendo = true
	# aviso: tiembla
	var temblor := create_tween().set_loops(int(tiempo_aviso / 0.08))
	temblor.tween_property(sprite, "position:x", 3.0, 0.04)
	temblor.tween_property(sprite, "position:x", -3.0, 0.04)
	await get_tree().create_timer(tiempo_aviso, false).timeout
	temblor.kill()
	# se rompe y cae
	$Sonido.play()
	forma.set_deferred("disabled", true)
	var caer := create_tween().set_parallel()
	caer.tween_property(sprite, "position", Vector2(0, 60), 0.5).set_ease(Tween.EASE_IN)
	caer.tween_property(sprite, "modulate:a", 0.0, 0.5)
	caer.tween_property(sprite, "rotation", 0.3, 0.5)
	await caer.finished
	# silueta: indica que volverá a aparecer aquí
	sprite.position = Vector2.ZERO
	sprite.rotation = 0.0
	sprite.modulate = Color(0.7, 0.9, 1.0, 0.25)
	await get_tree().create_timer(tiempo_reaparecer - 0.5, false).timeout
	# reaparece con destello
	forma.set_deferred("disabled", false)
	$Brillo.play()
	sprite.modulate = Color(2.0, 2.0, 2.0, 1.0)
	sprite.scale = Vector2(1.2, 1.2)
	var volver := create_tween().set_parallel()
	volver.tween_property(sprite, "modulate", Color.WHITE, 0.35)
	volver.tween_property(sprite, "scale", Vector2.ONE, 0.35)
	await volver.finished
	rompiendo = false
