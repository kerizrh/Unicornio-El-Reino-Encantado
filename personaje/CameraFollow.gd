extends Camera2D

@export var object_to_follow: CharacterBody2D

func _ready() -> void:
	process_callback = Camera2D.CAMERA2D_PROCESS_PHYSICS

var temblor := 0.0

func _physics_process(delta: float) -> void:
	if object_to_follow:
		position = object_to_follow.position
	# sacudida de cámara que se apaga poco a poco
	if temblor > 0.0:
		temblor = maxf(0.0, temblor - 40.0 * delta)
		offset = Vector2(randf_range(-temblor, temblor), randf_range(-temblor, temblor))
	else:
		offset = Vector2.ZERO

### Sacude la cámara (se usa al recibir un golpe)
func sacudir(intensidad := 10.0) -> void:
	temblor = intensidad
