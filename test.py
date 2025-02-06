# Bibliotheken laden
import pigpio
import time
# Raspberry Pi GPIO initialisieren
pi = pigpio.pi()       # pi accesses the local Pi's GPIO

# GPIO-Pins definieren für Stepper
DIR_PIN = 17  # Richtungspin
STEP_PIN = 27  # Steppin
ENA_PIN = 22    #Enable

#GPIO-Pin definieren für Lichtschranke
LS_PIN = 23    #Lichtschranke

# Pins als Ausgang setzen
pi.set_mode(DIR_PIN, pigpio.OUTPUT)
pi.set_mode(STEP_PIN, pigpio.OUTPUT)
pi.set_mode(ENA_PIN, pigpio.OUTPUT)
pi.write(ENA_PIN, 0)
pi.write(DIR_PIN, 0)

# Initialisierung von GPIO16 als Eingang für Lichtschranke
pi.set_mode( LS_PIN, pigpio.INPUT)  # GPIO  16 as input

#funktion zum ansteuern des Steppers
def move_motor(steps, direction, delay):
    # Richtung setzen
    pi.write(DIR_PIN, direction)

    # Schritte ausführen
    for _ in range(steps):
        pi.write(STEP_PIN, 1)
        time.sleep(delay)
        pi.write(STEP_PIN, 0)
        time.sleep(delay)

# Motor testweise ansteuern
move_motor(2000, 1, 0.001)


#print("Zustand der Lichtschranke:", pi.read(LS_PIN))

pi.stop()




