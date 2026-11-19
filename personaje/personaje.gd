class_name Personaje
extends CharacterBody2D

### Unicornio protagonista.
### Mecánicas: izquierda / derecha (flechas o A-D), salto (Espacio o flecha arriba)
### y caída por gravedad cuando no está sobre una superficie.

signal player_hit()

@export var gravity := 1000.0
@export var jump_speed := 520.0
@export var speed := 200.0
## Segundos de invulnerabilidad tras recibir un golpe (evita perder varias vidas de golpe)
@export var invulnerable_time := 1.2
## Poder del Cristal: permite vencer a lobos y murciélagos cayéndoles encima
@export var poder_cristal := false
## Impulso hacia arriba al aplastar a un enemigo
@export var rebote_aplastar := 380.0
## Si el unicornio cae más abajo que esto, reaparece en el último suelo firme y pierde una vida
@export var limite_caida := 750.0

@onready var sprite: AnimatedSprite2D = $Sprite
@onready var estela: CPUParticles2D = $EstelaMagica

var invulnerable := false
var ultimo_suelo_seguro := Vector2.ZERO

func _ready() -> void:
	add_to_group("jugador")
	ultimo_suelo_seguro = global_position
	if poder_cristal:
		# la estela mágica se vuelve turquesa: señal de que tiene el poder
		estela.color = Color(0.5, 1.0, 1.0)
		estela.amount = 24

func _physics_process(delta: float) -> void:
	# movimiento horizontal
	var direction := Input.get_axis("izquierda", "derecha")
	velocity.x = speed * direction
	if direction != 0.0:
		sprite.flip_h = direction < 0.0
		estela.position.x = 20.0 if direction < 0.0 else -20.0

	# gravedad: si no hay suelo debajo, el unicornio cae
	if not is_on_floor():
		velocity.y += gravity * delta

	# salto
	if Input.is_action_just_pressed("saltar") and is_on_floor():
		velocity.y = -jump_speed
		$SonidoSalto.play()

	move_and_slide()
	_recordar_suelo_seguro()
	if global_position.y > limite_caida:
		_caer_al_vacio()
	_actualizar_animacion(direction)

### Guarda la posición cuando pisa suelo firme (no plataformas móviles ni frágiles)
func _recordar_suelo_seguro() -> void:
	if not is_on_floor():
		return
	for i in get_slide_collision_count():
		var choque := get_slide_collision(i)
		var suelo := choque.get_collider()
		if choque.get_normal().y < -0.7 and suelo is StaticBody2D and not suelo.has_method("_romper"):
			ultimo_suelo_seguro = global_position
			return

### Red de seguridad: si cae por un precipicio vuelve al último suelo firme
func _caer_al_vacio() -> void:
	global_position = ultimo_suelo_seguro + Vector2(0, -10)
	velocity = Vector2.ZERO
	var camara := get_viewport().get_camera_2d()
	if camara:
		camara.reset_smoothing()
	if invulnerable:
		return
	damage_received()

func _actualizar_animacion(direction: float) -> void:
	if not is_on_floor():
		sprite.play("salto")
	elif direction != 0.0:
		sprite.play("caminar")
	else:
		sprite.play("quieto")

func _on_area_2d_body_entered(_body: Node2D) -> void:
	# el unicornio ha llegado al Cristal del Reino (lo gestiona el GameController)
	pass

### ¿Puede aplastar a este enemigo? Solo con el poder del Cristal,
### cayendo (no parado en el suelo) y estando por encima de él.
func puede_aplastar(enemigo: Node2D) -> bool:
	return poder_cristal and not is_on_floor() and velocity.y > 50.0 \
		and global_position.y < enemigo.global_position.y - 12.0

### Rebote al aplastar a un enemigo
func rebotar_sobre_enemigo() -> void:
	velocity.y = -rebote_aplastar
	var camara := get_viewport().get_camera_2d()
	if camara and camara.has_method("sacudir"):
		camara.sacudir(4.0)

### Llamado por los NPCs (rocas, bolas de fuego, lobos) al tocar al unicornio.
### Emite la señal player_hit que procesa el GameController.
func damage_received() -> void:
	if invulnerable:
		return
	invulnerable = true
	player_hit.emit()
	$SonidoGolpe.play()
	var camara := get_viewport().get_camera_2d()
	if camara and camara.has_method("sacudir"):
		camara.sacudir(10.0)
	velocity.y = -260.0  # pequeño rebote al ser golpeado
	# parpadeo mientras es invulnerable
	var tween := create_tween().set_loops(6)
	tween.tween_property(sprite, "modulate:a", 0.25, invulnerable_time / 12.0)
	tween.tween_property(sprite, "modulate:a", 1.0, invulnerable_time / 12.0)
	await get_tree().create_timer(invulnerable_time).timeout
	invulnerable = false
	sprite.modulate.a = 1.0
