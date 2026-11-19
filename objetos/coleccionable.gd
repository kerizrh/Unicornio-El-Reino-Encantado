extends Area2D

### Objeto que el unicornio puede recoger:
###   - "tiempo": gema arcoíris, suma segundos al contador.
###   - "vida": corazón, recupera una vida (máximo 3).

@export_enum("tiempo", "vida") var tipo := "tiempo"
@export var segundos := 5

@onready var sprite: Sprite2D = $Sprite

var recogido := false

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	# flota y brilla suavemente
	var flotar := create_tween().set_loops()
	flotar.tween_property(sprite, "position:y", -6.0, 0.7).set_trans(Tween.TRANS_SINE)
	flotar.tween_property(sprite, "position:y", 0.0, 0.7).set_trans(Tween.TRANS_SINE)

func _on_body_entered(body: Node2D) -> void:
	if recogido or not body is Personaje:
		return
	var gc := get_tree().get_first_node_in_group("game_controller")
	if gc == null:
		return
	var texto := ""
	if tipo == "tiempo":
		gc.sumar_tiempo(segundos)
		texto = "+%d s" % segundos
	else:
		if not gc.sumar_vida():
			return  # vida llena: el corazón se queda para después
		texto = "+1 VIDA"
	recogido = true
	$Sonido.play()
	_mostrar_texto(texto)
	var t := create_tween().set_parallel()
	t.tween_property(sprite, "scale", Vector2(1.8, 1.8), 0.25)
	t.tween_property(sprite, "modulate:a", 0.0, 0.25)
	await $Sonido.finished
	queue_free()

func _mostrar_texto(texto: String) -> void:
	var label := Label.new()
	label.text = texto
	label.add_theme_font_size_override("font_size", 24)
	label.add_theme_color_override("font_color", Color(1, 0.95, 0.6))
	label.add_theme_color_override("font_outline_color", Color(0.2, 0.13, 0.28))
	label.add_theme_constant_override("outline_size", 8)
	label.position = Vector2(-36, -50)
	add_child(label)
	var t := create_tween().set_parallel()
	t.tween_property(label, "position:y", -95.0, 0.8)
	t.tween_property(label, "modulate:a", 0.0, 0.8).set_delay(0.3)
