extends Area2D

### Hongo arcoíris: al caer o caminar sobre él, lanza al unicornio muy alto.

@export var impulso := 820.0

@onready var sprite: Sprite2D = $Sprite

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
	if body is Personaje and body.velocity.y >= 0.0:
		body.velocity.y = -impulso
		$Sonido.play()
		# el hongo se aplasta y rebota
		var t := create_tween()
		t.tween_property(sprite, "scale", Vector2(1.25, 0.7), 0.07)
		t.tween_property(sprite, "scale", Vector2(0.9, 1.15), 0.1)
		t.tween_property(sprite, "scale", Vector2.ONE, 0.12)
