extends CanvasLayer

### Pantalla de GAME OVER: aparece sobre el nivel congelado cuando el unicornio
### se queda sin vidas o sin tiempo. Permite reiniciar la partida.

func _ready() -> void:
	add_to_group("fin")
	get_tree().call_group("touch_controls", "hide")
	get_tree().call_group("pause_menu", "hide")
	%BtnReintentar.pressed.connect(_on_reintentar)
	%BtnSalir.pressed.connect(_on_salir)
	%BtnReintentar.grab_focus()  # Enter o Espacio reinician directamente
	_animar_entrada()

### motivo: "vidas" o "tiempo"
func set_motivo(motivo: String) -> void:
	if motivo == "tiempo":
		$Centro/Panel/VBox/Motivo.text = "¡Se acabó el tiempo!"
		$Centro/Panel/VBox/Consejo.text = "Consejo: sube por los extremos de las plataformas."
	else:
		$Centro/Panel/VBox/Motivo.text = "¡Te quedaste sin vidas!"
		$Centro/Panel/VBox/Consejo.text = "Consejo: salta las rocas y aléjate de los lobos."

func _animar_entrada() -> void:
	var panel: Control = $Centro/Panel
	var troll: Control = $Centro/Panel/VBox/Troll
	panel.modulate.a = 0.0
	await get_tree().process_frame  # espera a que se calculen los tamaños
	panel.pivot_offset = panel.size / 2.0
	troll.pivot_offset = troll.size / 2.0
	panel.scale = Vector2(0.8, 0.8)
	var t := create_tween().set_parallel()
	t.tween_property(panel, "modulate:a", 1.0, 0.35)
	t.tween_property(panel, "scale", Vector2.ONE, 0.45).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	# el troll se ríe (se balancea)
	var risa := create_tween().set_loops()
	risa.tween_property(troll, "rotation", 0.08, 0.25)
	risa.tween_property(troll, "rotation", -0.08, 0.25)

func _on_reintentar() -> void:
	get_tree().paused = false
	get_tree().reload_current_scene()  # reintenta el mismo nivel

func _on_salir() -> void:
	get_tree().quit()
