@tool
extends StaticBody2D

### Tramo de muralla de ancho ajustable (se ve en el editor al cambiar "ancho").
### Recorta la textura de la plataforma y ajusta su colisión.

@export_range(80.0, 930.0, 10.0) var ancho := 400.0:
	set(valor):
		ancho = valor
		_aplicar()

func _ready() -> void:
	_aplicar()

func _aplicar() -> void:
	if not is_node_ready():
		return
	var sprite: Sprite2D = $Sprite
	sprite.region_enabled = true
	sprite.region_rect = Rect2(0, 0, ancho, 49)
	var forma: RectangleShape2D = $CollisionShape2D.shape
	forma.size = Vector2(ancho - 4.0, 20.0)
