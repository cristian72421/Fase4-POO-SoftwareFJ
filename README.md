# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

## Descripción del Proyecto
Este proyecto es una aplicación desarrollada en Python para la empresa Software FJ. Su objetivo es gestionar clientes, servicios (reservas de salas, alquiler de equipos y asesorías especializadas) y reservas. El sistema está construido bajo una arquitectura estrictamente Orientada a Objetos (POO) y no utiliza bases de datos externas, operando completamente en memoria.

## Características Técnicas Implementadas
En cumplimiento con los requerimientos de la Fase 4, el sistema incluye:
* **Abstracción y Encapsulamiento:** Implementación de clases abstractas (`EntidadGeneral`, `Servicio`) y protección estricta de datos personales en la clase `Cliente`.
* **Herencia y Polimorfismo:** Clases derivadas especializadas (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) que sobrescriben métodos para describir y calcular costos.
* **Sobrecarga de Métodos:** Flexibilidad en el cálculo de costos mediante el uso de parámetros opcionales (impuestos, descuentos, seguros).
* **Manejo Robusto de Excepciones:** Uso de bloques `try/except/else/finally` y excepciones personalizadas (`DatoInvalidoError`, `OperacionNoPermitidaError`) para evitar caídas del sistema ante datos erróneos.
* **Sistema de Logs:** Registro automático de errores y excepciones en el archivo `sistema_errores.log` para auditoría y trazabilidad.

## Autor
* **Estudiante:** Cristian Camilo Rodriguez Cagueñas
* **Programa:** Ingeniería de Sistemas
* **Curso:** Programación (213023)
* **Universidad:** Universidad Nacional Abierta y a Distancia (UNAD)

## Instrucciones de Ejecución
Para probar la aplicación y ejecutar la simulación de las 10 operaciones requeridas:

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone [https://github.com/cristian72421/Fase4-POO-SoftwareFJ.git](https://github.com/cristian72421/Fase4-POO-SoftwareFJ.git)