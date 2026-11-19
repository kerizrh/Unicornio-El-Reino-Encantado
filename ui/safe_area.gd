class_name SafeArea
extends RefCounted

# Devuelve los margenes de la zona segura (izquierda, arriba, derecha, abajo)
# en unidades del viewport. En escritorio devuelve cero.
static func insets(viewport: Viewport) -> Vector4:
	if not OS.has_feature("mobile"):
		return Vector4.ZERO
	var screen := Vector2(DisplayServer.window_get_size())
	if screen.x <= 0.0 or screen.y <= 0.0:
		return Vector4.ZERO
	var safe := DisplayServer.get_display_safe_area()
	var vp := viewport.get_visible_rect().size
	var sx := vp.x / screen.x
	var sy := vp.y / screen.y
	return Vector4(
		safe.position.x * sx,
		safe.position.y * sy,
		(screen.x - safe.end.x) * sx,
		(screen.y - safe.end.y) * sy)
