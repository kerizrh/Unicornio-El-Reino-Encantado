extends CanvasLayer

@onready var overlay: Control = %Overlay
@onready var pause_button: Button = %BtnPausa
@onready var resume_button: Button = %BtnContinuar
@onready var restart_button: Button = %BtnReiniciar

func _ready() -> void:
	add_to_group("pause_menu")
	pause_button.pressed.connect(_set_paused.bind(true))
	resume_button.pressed.connect(_set_paused.bind(false))
	restart_button.pressed.connect(_on_restart_pressed)
	overlay.hide()

func _set_paused(value: bool) -> void:
	if get_tree().get_first_node_in_group("fin"):
		return
	get_tree().paused = value
	overlay.visible = value

func _on_restart_pressed() -> void:
	get_tree().paused = false
	get_tree().reload_current_scene()

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_GO_BACK_REQUEST:
		_set_paused(not get_tree().paused)
	elif what == NOTIFICATION_APPLICATION_PAUSED:
		_set_paused(true)
