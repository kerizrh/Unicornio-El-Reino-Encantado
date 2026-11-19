extends AnimatableBody2D

### Plataforma mágica que va y viene (horizontal o vertical).
### AnimatableBody2D arrastra al unicornio cuando está encima.

## Hacia dónde se mueve desde su posición inicial (px)
@export var desplazamiento := Vector2(240, 0)
## Segundos que tarda en cada trayecto
@export var duracion := 2.2
## Pausa en cada extremo
@export var pausa := 0.4
## Retraso antes de empezar (para desfasar varias plataformas)
@export var retraso := 0.0

func _ready() -> void:
	var inicio := position
	if retraso > 0.0:
		await get_tree().create_timer(retraso, false).timeout
	var t := create_tween().set_loops().set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)
	t.tween_property(self, "position", inicio + desplazamiento, duracion) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	t.tween_interval(pausa)
	t.tween_property(self, "position", inicio, duracion) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	t.tween_interval(pausa)
