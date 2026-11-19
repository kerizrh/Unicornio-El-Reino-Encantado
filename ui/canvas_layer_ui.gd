extends CanvasLayer

### Interfaz del jugador: contador de tiempo (pergamino) y barra de vida.
### Recibe las señales del GameController.

const COLOR_TIEMPO := Color(0.36, 0.2, 0.12)
const COLOR_URGENTE := Color(0.85, 0.1, 0.15)

@onready var label_tiempo: Label = $TextureRect/LabelTiempo
@onready var barra: ProgressBar = $BarraVida/ProgressBar
@onready var label_vida: Label = $BarraVida/ProgressBar/LabelVida

func _ready() -> void:
	# respeta la zona segura (muesca de la camara) en la esquina superior derecha
	var inset := SafeArea.insets(get_viewport())
	for node in [$TextureRect, $BarraVida]:
		node.offset_left -= inset.z
		node.offset_right -= inset.z
		node.offset_top += inset.y
		node.offset_bottom += inset.y
	# el mensaje de misión desaparece poco a poco
	var tween := create_tween()
	tween.tween_interval(3.5)
	tween.tween_property($Mision, "modulate:a", 0.0, 1.0)

func _on_game_controller_player_health_updated(new_player_health: int) -> void:
	var vida := maxi(new_player_health, 0)
	label_vida.text = "VIDA %d/%d" % [vida, int(barra.max_value)]
	# la barra baja de forma animada y tiembla
	var tween := create_tween()
	tween.tween_property(barra, "value", float(vida), 0.3)
	var shake := create_tween()
	for i in 4:
		shake.tween_property($BarraVida, "position:x", $BarraVida.position.x + (6 if i % 2 == 0 else -6), 0.04)
	shake.tween_property($BarraVida, "position:x", $BarraVida.position.x, 0.04)

### Mensaje grande y temporal en el centro de la pantalla
func mostrar_aviso(texto: String) -> void:
	var label := Label.new()
	label.text = texto
	label.add_theme_font_size_override("font_size", 46)
	label.add_theme_color_override("font_color", Color(1, 0.45, 0.4))
	label.add_theme_color_override("font_outline_color", Color(0.15, 0.05, 0.1))
	label.add_theme_constant_override("outline_size", 14)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(label)
	label.set_anchors_and_offsets_preset(Control.PRESET_CENTER_TOP)
	label.offset_left = -400
	label.offset_right = 400
	label.offset_top = 150
	label.offset_bottom = 214
	label.pivot_offset = Vector2(400, 32)
	label.scale = Vector2(0.3, 0.3)
	var t := create_tween()
	t.tween_property(label, "scale", Vector2.ONE, 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	t.tween_interval(1.8)
	t.tween_property(label, "modulate:a", 0.0, 0.6)
	t.tween_callback(label.queue_free)

func _on_game_controller_time_updated(seconds_left: int) -> void:
	label_tiempo.text = str(seconds_left)
	if seconds_left <= 10:
		label_tiempo.add_theme_color_override("font_color", COLOR_URGENTE)
		var tween := create_tween()
		tween.tween_property(label_tiempo, "scale", Vector2(1.3, 1.3), 0.12)
		tween.tween_property(label_tiempo, "scale", Vector2.ONE, 0.2)
	else:
		label_tiempo.add_theme_color_override("font_color", COLOR_TIEMPO)
