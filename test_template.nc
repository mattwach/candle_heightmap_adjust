(CNC Regtangle Test File)

G{unit_code}                            (Units in {units}) 
G90                                     (Absolute positioning)
G94                                     (Units per minute feed rate mode)

G01 F{z_dwell_feedrate}                 (Move to starting position)
G01 Z{z_initial_height}
G00 X0.0 Y0.0
M03 S{spindle_speed}                    (Start motor)
G01 Z{z_preplunge_height}                   (Move to dwell height)

G01 F{z_plunge_feedrate}                (Approach material)
G01 Z0.0
G01 F{xy_feedrate}                      (Draw rectangle)
G01 X{width}
G01 Y{height}
G01 X0.0
G01 Y0.0

G01 F{z_dwell_feedrate}
G01 Z{z_initial_height}                 (Exit material)
M05                                     (Stop motor)
(Test complete, EOF)

