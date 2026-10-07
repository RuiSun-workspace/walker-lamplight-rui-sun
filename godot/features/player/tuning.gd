extends Resource
## walker-jumpman GDD 0.2.0 values scaled x2 for the 1280x720 viewport (CHANGE-BRIEF revision 2026-10-07).
## Pixel quantities double, tick counts stay, so the jump arc and timing feel the same.
@export var speed: float = 320.0
@export var acceleration: float = 2560.0
@export var deceleration: float = 3840.0
@export var jump_velocity: float = -640.0
@export var gravity: float = 1920.0
@export var terminal_velocity: float = 960.0
@export var coyote_ticks: int = 6
@export var buffer_ticks: int = 6
