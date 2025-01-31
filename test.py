# Bibliotheken laden
#Lichtschranke
#from machine import Pin
#Onboard LED
#from machine import Pin
from time import sleep

# Initialisierung von GPIO16 als Eingang
#sensor_d = Pin(16, Pin.IN)
# Initialisierung von GPIO25 als Ausgang
#led_onboard = Pin(25, Pin.OUT)

# Zähler
count = 0

# Funktion: Interrupt-Behandlung
def sensor_irq(pin):
    global count
    count += 1
    print(count)
#
# Interrupt-Steuerung
#sensor_d.irq(trigger=Pin.IRQ_RISING, handler=sensor_irq)


print("Hello WOrld")



#code zur onboard led

# LED einschalten
#led_onboard.on()

# 5 Sekunden warten
#sleep(5)

# LED ausschalten
#led_onboard.off()