extends MarginContainer

@export var base_margin := 16

func _ready() -> void:
	var i := SafeArea.insets(get_viewport())
	add_theme_constant_override("margin_left", base_margin + int(i.x))
	add_theme_constant_override("margin_top", base_margin + int(i.y))
	add_theme_constant_override("margin_right", base_margin + int(i.z))
	add_theme_constant_override("margin_bottom", base_margin + int(i.w))
