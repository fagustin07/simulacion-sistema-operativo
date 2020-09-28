# Práctica 3
## Multiprogramación


En esta versión, la __CPU__ no accede directamente a la __Memoria__, como hace la __CPU__ para fetchear la instruccion?? Por que??

Existe un componente de hardware llamado Memory Management Unit (__MMU__) que se encarga de transformar las direcciones lógicas (relativas)  en direcciones físicas (absolutas)



## Interrupciones de I/O y Devices

En esta version del emulador agregamos los I/O Devices y el manejo de los mismos

Un I/O device es un componente de hardware (interno o externo) que realiza operaciones específicas.

Una particularidad que tienen estos dispositivos es los tiempos de ejecucion son mas extensos que los de CPU, ej: bajar un archivo de internet, imprimir un archivo, leer desde un DVD, etc.
Por otro lado, solo pueden ejecutar una operacion a la vez, con lo cual nuestro S.O. debe garantizar que no se "choquen" los pedidos de ejecucion.

Para ello implementamos un __IoDeviceController__ que es el encargado de "manejar" el device, encolando los pedidos para ir sirviendolos a medida que el dispositivo se libere.


También se incluyeron 2 interrupciones 

- __#IO_IN__
- __#IO_OUT__



## Lo que tenemos que hacer es:

- __1:__ Describir como funciona el __MMU__ y que datos necesitamos para correr un proceso

<em>El  MMU es el encargado de manejar la transformacion de direcciones logicas del cpu en la direccion fisica real del programa. 
Cuando la CPU intenta acceder a una direccion logica de memoria, el MMU realiza la operación llamada “fetch” que se encarga de buscar la siguiente instrucción del programa en ejecucion en la memoria, haciendo el mencionado traspaso de direccion logica a direccion fisica para obtener la direccion real de la instrucción. Posteriormente, realiza la lectura de la direccion fisica en memoria. </em>

- __2:__ Entender las clases __IoDeviceController__, __PrinterIODevice__ y poder explicar como funcionan

<em>El IODeviceController es el encargado de ejecutar las instrucciones IO que se le encarguen. Cuenta con una lista waiting, en donde iran a parar las instrucciones que esten esperando un lugar en el IO device.</em>

- __3:__ Explicar cómo se llegan a ejecutar __IoInInterruptionHandler.execute()__ y  __IoOutInterruptionHandler.execute()__

<em> Luego de que la CPU lee la direccion de memoria del programa(realizando el procedimiento previamente mencionado donde el MMU forma parte), y luego de que se decodifica esta instruccion(en nuestro simulador aun no se realiza la decodificacion) la instrucción del programa es ejecutada y en su ejecucion se lleva a cabo un determinado chequeo para constatar el tipo de instrucción del cual se trata. Si esta instrucción fuera de IOIN, la CPU genera una interrupcion de tipo IoInInterruption, la cual es manejada por el vector de interrupciones que se encarga de gestionar todas las interrupciones existentes. Este vector recibe la instrucción IO del programa y ejecuta el metodo correspondiente proveniente del IoInInterruptionHandler.</em>  

<em> Luego de que el IoInInterruptionHandler guarde la informacion del estado actual del programa, cambie su estado a Waiting y le indique al IODeviceController que corra la instrucción IO (la cual sera ejecutada por el IO device siempre y cuando este no tenga ninguna otra instrucción corriendo, caso contrario se agregara a la waiting queue), el IO device levanta una interrupcion IoOutInterruption la cual es gestionada nuevamente por el vector de interrupciones. Este realiza el execute del IoOutInterruptionHandler, el cual se encarga de poner el programa de nuevo en cpu o el la ready queue.  </em>

- __4:__    Hagamos un pequeño ejercicio (sin codificarlo):

- __4.1:__ Que esta haciendo el CPU mientras se ejecuta una operación de I/O??

<em> El cpu mientras se ejecuta una instrucción IO puede estar en estado NOOP, o puede estar ejecutando la instrucción de otro programa(siempre que exista otro programa cargado en memoria). </em>

- __4.2:__ Si la ejecucion de una operacion de I/O (en un device) tarda 3 "ticks", cuantos ticks necesitamos para ejecuar el siguiente batch?? Cómo podemos mejorarlo??
    (tener en cuenta que en el emulador consumimos 1 tick para mandar a ejecutar la operacion a I/O)

    ```python
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])
    ```

<em>Si la ejecucion de una operación IO tardara 3 ticks, y considerando que cada operación CPU tarda 1 tick, ademas del tick de reloj que se pierde por mandar a ejecutar cada operación IO, se tardarian 27 ticks en ejecutar el batch dado. Para mejorar ese tiempo, se podria ejecutar concurrentemente una instrucción de CPU de otro programa mientras el IO device estuviera ejecutando una instrucción IO, asi la CPU siempre estaria activa y se reducirian considerablemente la cantidad de ticks para ejecutar el batch. </em>


- __5:__ Hay que tener en cuenta que los procesos se van a intentar ejecutar todos juntos ("concurrencia"), pero como solo tenemos un solo CPU, vamos a tener que administrar su uso de forma óptima.
      Como el S.O. es una "maquina de estados", donde las cosas "pasan" cada vez que se levanta una interrupcion (IRQ) vamos a tener que programar las 4 interrupciones que conocemos:  
    
    - Cuando se crea un proceso (__#NEW__) se debe intentar hacerlo correr en la CPU, pero si la CPU ya esta ocupada, debemos mantenerlo en la cola de Ready.
    - Cuando un proceso entre en I/O (__#IO_IN__), debemos cambiar el proceso corriendo en CPU (__"running"__) por otro, para optimizar el uso de __CPU__
    - Cuando un proceso sale en I/O (__#IO_OUT__), se debe intentar hacerlo correr en la CPU, pero si la CPU ya esta ocupada, debemos mantenerlo en la cola de Ready.
    - Cuando un proceso termina (__#KILL__), debemos cambiar el proceso corriendo en CPU (__"running"__) por otro, para optimizar el uso de __CPU__

.

- __6:__ Ahora si, a programar... tenemos que "evolucionar" nuestro S.O. para que soporte __multiprogramación__  

- __6.1:__ Implementar la interrupción #NEW
    ```python
    # Kernel.run() debe lanzar una interrupcion de #New para que se resuelva luego por el S.O. 
    ###################

    ## emulates a "system call" for programs execution
    def run(self, program):
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, program)
        self._interruptVector.handle(newIRQ)
    ```

- __6.2:__ Implementar los compoenentes del S.O.: 
    - Loader
    - Dispatcher
    - PCB
    - PCB Table
    - Ready Queue
    - Las 4 interrupciones: 
        - __#NEW__ 
        - __#IO_IN__
        - __#IO_OUT__
        - __#KILL__



- __6.3:__        Implementar una version con __multiprogramación__ (donde todos los procesos se encuentran en memoria a la vez)


    ```python
    # Ahora vamos a intentar ejecutar 3 programas a la vez
    ###################
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])

    # executamos los programas "concurrentemente"
    kernel.run(prg1)
    kernel.run(prg2)
    kernel.run(prg3)

    ## start
    HARDWARE.switchOn()

    ```
