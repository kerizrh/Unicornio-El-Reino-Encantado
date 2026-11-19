extends CanvasLayer

const BTN_SIZE := 140.0
const MARGIN := 40.0

# Activalo en el Inspector para ver los botones en el PC.
@export var always_show := false

@onready var btn_left: TouchScreenButton = $BtnIzquierda
@onready var btn_right: TouchScreenButton = $BtnDerecha
@onready var btn_jump: TouchScreenButton = $BtnSaltar

func _ready() -> void:
	add_to_group("touch_controls")
	# solo en móvil (en PC se juega con flechas y Espacio)
	visible = always_show or OS.has_feature("mobile")
	get_viewport().size_changed.connect(_layout)
	_layout()

func _layout() -> void:
	var vp := get_viewport().get_visible_rect().size
	var inset := SafeArea.insets(get_viewport())
	var y := vp.y - MARGIN - BTN_SIZE - inset.w
	btn_left.position = Vector2(MARGIN + inset.x, y)
	btn_right.position = Vector2(MARGIN * 2.0 + BTN_SIZE + inset.x, y)
	btn_jump.position = Vector2(vp.x - MARGIN - BTN_SIZE - inset.z, y)
