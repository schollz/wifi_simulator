# Wifi Simulator

Instead of [solving Helmholtz equation](https://en.wikipedia.org/wiki/Helmholtz_equation) with various boundary conditions I wrote this program to do Ray tracing to get an approximate behavior.

For example, after ray tracing with a room with open doors you'll get:

![Ray tracing with doors open](https://i.imgur.com/4x2Iy7L.png)

And if you close the doors you'll get:

![Ray tracing with doors closed](https://i.imgur.com/E0SCOyr.png)

As you can see, the neighbooring rooms are slightly brighter meaning that its more helpful to keep the doors for WiFi to transmit completely.

## To Do

- Make more user friendly (command line help)
- Add in parameter for transmission/reflection coefficient
