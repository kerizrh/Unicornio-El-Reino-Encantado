extends Node2D

### GameController: controla las reglas de la partida.
###  - Contador de tiempo de 120 segundos para terminar el nivel.
###  - Vidas del unicornio (barra de vida): bajan con cada choque contra un NPC.
###  - Fin de partida: escena Game Over (permite reiniciar) o victoria.

const SCENE_FINISH_FILE := "res://ui/scene_finish.tscn"
const SCENE_GAME_OVER_FILE := "res://ui/game_over.tscn"

### Definición de señales con sus variables y tipo de dato
signal player_health_updated(new_player_health: int)
signal time_updated(seconds_left: int)

### variables globales del juego
@export var player_health := 3
@export var time_seconds := 120
## Nombre y misión que se muestran al empezar el nivel
@export var nombre_nivel := "NIVEL 1 · Las Murallas del Reino"
@export_multiline var mision := "¡Sube a la cima, salta sobre el troll\ny toca el Cristal del Reino!"
## Escena a la que se pasa al ganar (vacío = fin del juego)
@export_file("*.tscn") var siguiente_nivel := ""
## Vidas máximas (los corazones no pasan de aquí)
@export var max_health := 3
## Segundos restantes en los que el troll se enfurece (0 = nunca)
@export var tiempo_furia := 70

var finished := false
var furioso := false

func _ready() -> void:
	add_to_group("game_controller")
	var label_mision := get_parent().get_node_or_null("CanvasLayerUI/Mision") as Label
	if label_mision:
		label_mision.text = nombre_nivel + "\n" + mision
	# muestra los valores iniciales en la interfaz
	player_health_updated.emit.call_deferred(player_health)
	time_updated.emit.call_deferred(time_seconds)

### Muestra la pantalla de GAME OVER sobre el nivel congelado.
### motivo: "vidas" (sin vidas) o "tiempo" (se acabaron los 120 s)
func game_over(motivo := "vidas") -> void:
	if finished:
		return
	finished = true
	$Timer.stop()
	_detener_musica_nivel()
	var game_over_instance = preload(SCENE_GAME_OVER_FILE).instantiate()
	game_over_instance.set_motivo(motivo)
	add_child(game_over_instance)
	get_tree().paused = true

### Muestra la pantalla de victoria (con su propia música)
func game_victory() -> void:
	if finished:
		return
	finished = true
	$Timer.stop()
	_detener_musica_nivel()
	var scene_finish_instance = preload(SCENE_FINISH_FILE).instantiate()
	scene_finish_instance.configurar(siguiente_nivel)
	add_child(scene_finish_instance)
	get_tree().paused = true

### Apaga la música del nivel para que suene la de victoria o derrota
func _detener_musica_nivel() -> void:
	var musica := get_parent().get_node_or_null("Musica") as AudioStreamPlayer
	if musica:
		musica.stop()
	var mision := get_parent().get_node_or_null("CanvasLayerUI/Mision") as CanvasItem
	if mision:
		mision.hide()

### Se ejecuta cuando un NPC golpea al unicornio: resta una vida.
### Si las vidas llegan a cero se llama al método game_over()
func _on_personaje_player_hit() -> void:
	if finished:
		return
	player_health -= 1
	player_health_updated.emit(player_health)
	if player_health <= 0:
		game_over()

### El unicornio tocó el Cristal del Reino
func _on_area_2d_body_entered(body: Node2D) -> void:
	if body is Personaje:
		game_victory()

### Controla el tiempo de la partida y actualiza los segundos restantes.
func _on_timer_timeout() -> void:
	if finished:
		return
	if time_seconds > 0:
		time_seconds -= 1
	time_updated.emit(time_seconds)
	if time_seconds <= 0:
		game_over("tiempo")
	elif not furioso and time_seconds <= tiempo_furia:
		_activar_furia()

### Gema arcoíris: suma segundos al contador
func sumar_tiempo(segundos: int) -> void:
	if finished:
		return
	time_seconds += segundos
	time_updated.emit(time_seconds)

### Corazón: recupera una vida. Devuelve false si la vida ya estaba llena.
func sumar_vida() -> bool:
	if finished or player_health >= max_health:
		return false
	player_health += 1
	player_health_updated.emit(player_health)
	return true

### Fase final: el troll ruge, todo se acelera y la música sube de tono
func _activar_furia() -> void:
	furioso = true
	get_tree().call_group("furia", "activar_furia")
	var ui := get_parent().get_node_or_null("CanvasLayerUI")
	if ui and ui.has_method("mostrar_aviso"):
		ui.mostrar_aviso("¡EL TROLL ESTÁ FURIOSO!")
	var musica := get_parent().get_node_or_null("Musica") as AudioStreamPlayer
	if musica:
		create_tween().tween_property(musica, "pitch_scale", musica.pitch_scale * 1.12, 1.5)
