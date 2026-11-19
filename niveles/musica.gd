extends AudioStreamPlayer

### Música de fondo: se repite indefinidamente mientras dure la partida.

func _ready() -> void:
	if stream is AudioStreamWAV:
		# bucle sin cortes: la pista está compuesta para enlazar el final con el inicio
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		stream.loop_begin = 0
		stream.loop_end = int(stream.get_length() * stream.mix_rate)
	# respaldo: si por algún motivo termina, vuelve a sonar
	finished.connect(play)
	if not playing:
		play()
