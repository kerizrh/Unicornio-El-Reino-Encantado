extends CanvasLayer

### Escena de fin de partida (Game Over o victoria).
### El botón reinicia la partida cargando de nuevo el nivel.

const LEVEL_1_FILE := "res://niveles/level_1.tscn"

func _ready() -> void:
	add_to_group("fin")
	get_tree().call_group("touch_controls", "hide")
	get_tree().call_group("pause_menu", "hide")
	$Centro/VBoxContainer/Button.grab_focus()
	# el unicornio flota suavemente
	var tween := create_tween().set_loops()
	tween.tween_property($Centro/VBoxContainer/Unicornio, "modulate", Color(1, 0.85, 1), 0.8)
	tween.tween_property($Centro/VBoxContainer/Unicornio, "modulate", Color.WHITE, 0.8)

var siguiente := ""

### Si hay un siguiente nivel el botón lleva a él; si no, el juego terminó.
func configurar(siguiente_nivel: String) -> void:
	siguiente = siguiente_nivel
	if siguiente != "":
		set_title("¡NIVEL SUPERADO!")
		set_subtitle("¡El Cristal te dio su PODER: ahora puedes vencer a lobos y murciélagos\nsaltando sobre ellos! Te espera la Torre de las Nubes.")
		$Centro/VBoxContainer/Button.text = "SIGUIENTE NIVEL"
	else:
		set_title("¡ERES UNA LEYENDA!")
		set_subtitle("Superaste la Torre de las Nubes: el reino entero está a salvo.")
		$Centro/VBoxContainer/Button.text = "VOLVER A JUGAR"

func set_title(title: String) -> void:
	$Centro/VBoxContainer/Label.text = title

func set_subtitle(subtitle: String) -> void:
	$Centro/VBoxContainer/Subtitulo.text = subtitle

func _on_button_button_down() -> void:
	get_tree().paused = false
	get_tree().change_scene_to_file(siguiente if siguiente != "" else LEVEL_1_FILE)
