***Sistema OdontoCare prompt***

*Trabajo Final escuela de programación Python: Sistema OdontoCare* 
# Introducción 
El ejercicio consiste en implementar un sistema que combine los siguientes componentes fundamentales: 

1. **Framework Backend:** Desarrollo de una API REST utilizando Flask, organizada de forma profesional mediante Blueprints para asegurar modularidad y escalabilidad. 
1. **Persistencia de Datos:** Uso de una base de datos SQLite**,** gestionada a través de  SQLAlchemy como ORM para modelar entidades, relaciones y operaciones CRUD1**.** 
1. **Seguridad:** Implementación de un mecanismo de autenticación basado en tokens, garantizando el acceso seguro a los diferentes recursos del sistema. 
1. **Cliente Externo**: Creación de un script independiente en Python que consuma los servicios de la API utilizando la biblioteca requests, demostrando la correcta interacción entre cliente y servidor. 
1. **Arquitectura Distribuida y Comunicación entre Servicios**: Crear imágenes en docker. 
# Escenario del Proyecto 
Una red de clínicas dentales ha decidido modernizar sus operaciones creando una aplicación a medida para gestionar las citas de los pacientes y la disponibilidad de los odontólogos. 

Actualmente, el sistema se gestiona de forma manual, lo que provoca errores frecuentes, duplicidad de información y falta de trazabilidad en los procesos administrativos. 

Como desarrollador backend asignado al proyecto, tu misión consiste en diseñar y construir una solución integral, robusta y escalable, que permita cubrir todas las necesidades del nuevo sistema de gestión OdontoCare. 

Para ello, se requiere el desarrollo de una API RESTful profesional, siguiendo buenas prácticas de arquitectura de software, seguridad y persistencia de datos. 

El sistema debe permitir la administración eficiente de la información mediante los siguientes módulos esenciales: 

1. Pacientes 
1. Doctores 
1. Centros médicos o clínicas 
1. Citas médicas 

Toda la información gestionada por la API debe persistir en una base de datos fiable. 

Además, el acceso a los recursos debe estar controlado mediante un **mecanismo de autenticación** basado en tokens (JWT o similar), garantizando que sólo los usuarios autorizados puedan interactuar con los datos. 

El formato de comunicación de todos los servicios será exclusivamente JSON, por lo que cada endpoint debe responder consistentemente en este formato, tanto en operaciones exitosas como en gestión de errores. 

El sistema debe contar con una estructura de proyecto adecuadamente definida que permita y fomente un mantenimiento adecuado 

Adicionalmente, deberá incluir un archivo **requirements.txt** para cada proyecto, en el que se especifiquen todas las librerías y dependencias necesarias, incorporando aquellas que considere pertinentes para el correcto desarrollo de la actividad. 
# Objetivos principales del sistema 
1. Diseñar una API RESTful organizada, modular y mantenible. 
1. Implementar operaciones CRUD para pacientes, doctores, centros y citas. 
1. Garantizar la persistencia de la información en una base de datos (SQL o NoSQL). 
1. Incorporar un sistema de autenticación segura por tokens. 
1. Asegurar que todas las respuestas se entreguen en formato JSON. 
1. Aplicar buenas prácticas como validación de datos, gestión de excepciones, paginación y documentación básica de la API. 
1. Implementar una arquitectura distribuida basada en contenedores Docker. 
# Arquitectura de la Solución** 
Para garantizar un desarrollo ordenado, escalable y alineado con buenas prácticas de ingeniería de software, la API debe implementarse utilizando una arquitectura modular basada en Blueprints de Flask. 

Esto permitirá separar la lógica del sistema por dominios funcionales, facilitando su mantenimiento, comprensión y reutilización. 

La solución no debe concentrar todo el código en un solo archivo. En su lugar, se exige una estructura organizada que distribuya la lógica en módulos claros y coherentes. 

La API deberá estructurarse, como mínimo, con los siguientes componentes: 

**auth\_bp** — Autenticación y Gestión de Usuarios 

Encargado de todas las operaciones relacionadas con el acceso seguro al sistema. Debe incluir: 

- Registro de usuarios autorizados. 
- Inicio de sesión mediante validación de credenciales. 
- Generación y validación de tokens de autenticación (JWT). 
- Gestión de errores de acceso. 

Este módulo garantiza que todas las acciones dentro del sistema sean realizadas sólo por usuarios autenticados. 

**admin\_bp** — Administración y Gestión de Centros, Pacientes y Doctores 

Módulo orientado a tareas administrativas, encargado de configurar los elementos base del sistema. Debe incluir: 

- Creación de entidades principales: centros médicos, pacientes y doctores. 
- Carga de datos, tanto masiva como individual, utilizando archivos en formato JSON cuando sea requerido. 
- Opciones de consulta para todos los tipos de registros, permitiendo: 
  - ○ Busqueda individual por ID. 
  - ○ Visualización opcional de una lista completa de registros. 

Este módulo está diseñado para usuarios con roles administrativos o de gestión. 

**citas\_bp** — Gestión Operativa de Citas 

Responsable del núcleo funcional de OdontoCare: la planificación, administración y control de citas médicas. Debe incluir: 

- Creación, actualización, consulta y eliminación de citas. 
- Facturación de disponibilidad de doctores y centros. 
- Reglas operativas para evitar conflictos en la agenda. 
- Respuestas en formato JSON con mensajes claros y estructurados. 

Este módulo será el más utilizado durante la operación diaria del sistema. 
# Modelo de Datos (SQLAlchemy) 
Debes definir al menos las siguientes tablas/modelos. Puede ser necesaria la creación de estructuras adicionales al modelo; eso queda en libertad del estudiante. 

**Usuario** 

- id\_user (HP) 
- nombre de usuario 
- contraseña 
- rol (admin, médico, secretario/a, paciente) 

**Paciente - Datos mínimos del paciente:** 

- id\_pacient (HP) 
- id\_user (FK opcional) 
- nombre 
- teléfono 
- estado(ACTIVO/INACTIVO) 

**Doctor** 

- id\_doctor (PK) 
- id\_user (FK opcional) 
- nombre 
- especialidad 

**Centro Médico** 

- id\_centro (HP) 
- nombre 
- dirección 

**Cita Médica:** Relaciona paciente, doctor y centro: 

- id\_cita (PK) 
- fecha 
- motivo 
- estado 
- id\_paciente (FK) 
- id\_doctor (FK) 
- id\_centro (FK) 
- id\_user\_registrado (FK) 
# Funcionalidades Detalladas 
**Autenticación y Seguridad** 

El sistema no puede confiar en un simple campo JSON. Debe incluir: 

- POST /auth/login 
- Verificación de usuario y contraseña. 
- Retorno de un token válido. 
- Envío obligatorio del token al header:  Autorización: Portador <token> 
- Todos los endpoints protegidos deben validar este token. 
# Carga Inicial de Datos — Múltiples Endpoints 
El sistema debe permitir cargar datos desde un archivo local CSV, sin embargo: 

- El servidor NO recibe un archivo CSV. 
- Se programa un cliente en python que procesa los ficheros de datos .csv creados con datos sinteticos con los datos iniciales y los envia a los endpoints registro a registro. 

Puntos finales: 

- crear usuarios POST /admin/usuario 
  - Rol requerido: Admin. Registra un usuario (y crea un usuario con rol "admin" o "secretaría"). 
- crear doctores POST /admin/doctores 
  - Rol requerido: Admin. Registra un doctor (y crea un usuario con rol "médico"). 
- crear paciente POST /admin/pacientes 
  - Rol requerido: Admin. Registra un paciente (y crea un usuario con rol "paciente"). 
- crear centro POST /admin/centros 
  - Rol requerido: Admin. Registra un centro médico. 
# Gestión de Citas (Core) 
Las reglas de negocio deben consultar la base de datos. 

**Programa cita — POST /citas** 

- Roles: Cliente y Admin 
- Validaciones obligatorias: 
  - El doctor existe. 
  - El centro médico existe. 
  - El paciente existe y está activo. 
  - No se puede agendar una cita si el doctor ya tiene otra en la misma fecha y hora (evitar doble reserva). 

**Listar Citas** — **GET /citas** 

- Doctor: sólo ve sus propias citas. 
- Secretaría: puede consultar citas filtrando por fecha. 
- Admin: puede filtrar por doctor, centro, fecha, estado o paciente. 
- Se usan query paramos para aplicar los filtros. 
- Cliente: solo ve sus propias citas

**Cancelar cita** — **PUT /citas/<id>** 

- Roles permitidos: Cliente,Secretaría y Admin. 
- Validaciones: 
  - La cita existe. 
  - No está cancelada. 
- Se cambia el estado a "Cancelada" y se devuelve un mensaje JSON confirmando la acción. 

**Cambiar cita** — PUT /citas/<id> 

- Roles permitidos: Cliente, Secretaría y Admin. 
- Validaciones obligatorias: 
  - La cita existe 
  - La cita no esta cancelada
  - El doctor existe. 
  - El centro médico existe. 
  - El paciente existe y está activo. 
  - No se puede agendar una cita si el doctor ya tiene otra en la misma fecha y hora (evitar doble reserva). 
  - Si se ha podido cambiar la cita  
  - Se cancela la cita previa y se devuelve un mensaje JSON confirmando la acción. 
  - En caso contrario no se cancela la cita anterior y se devuelve un mensaje JSON indicando que no se ha podido cambiar la cita Archivo de Prueba (datos.csv) 

El ejercicio debe crear TRES ARCHIVOS con formación ficticia con datos sinteticos generados según la estructura documentada anteriormente de cada una de estas entidades que permita la carga inicial de datos del sistema: 

- Cargar usuarios. usuarios.csv 
- Cargar doctores: doctores.csv 
- Cargar pacientes: pacientes.csv 
- Cargar centros: centros.csv con 

Estos archivos serán leidos y cargados por un python cliente enviado a la API. 
# Python cliente 
El ejercicio  debe entregar un script: carga\_inicial.py, que: 

- Realice login con un usuario admin (del CSV). 
- Procese y envíe los registros de los archivos: usuarios.csv, doctores.csv, pacientes.csv y centros.csv enviando registro a registro a cada uno de los endpoints correspondiente dependiendo del fichero .csv que este procesando: usuario, doctores, centros, 
- Cree una cita médica. 
- Imprima en la consola el JSON con la cita creada. 
# Arquitectura Distribuida y Comunicación entre Servicios 


Además de los módulos principales del sistema, la actividad requiere implementar una arquitectura distribuida basada en contenedores Docker, donde cada componente clave funcione como un microservicio independiente. El ejercicio deberá diseñar y desplegar el sistema OdontoCare como un conjunto de servicios autónomos, cada uno ejecutándose en su propio contenedor Docker y comunicándose únicamente mediante servicios REST, sin compartir bases de datos ni acceso directo entre ellos. 

Los módulos se separan de la siguiente manera: 

- **Servicio de Gestión de Usuarios y Registro Administrativo** 
- **Servicio de Gestión de Citas** 

El servicio de citas no debe acceder directamente a las bases de datos de los otros módulos. En su lugar, debe obtener toda la información necesaria únicamente mediante los servicios REST expuestos por los demás microservicios. Esto garantiza un intercambio de información adecuado, seguro y coherente con la arquitectura distribuida definida para la actividad. 

El ejercicio podrá realizar los ajustes necesarios en el diseño para cumplir con los requisitos de: 

- Intercomunicación entre los diferentes servicios. 
- Independencia de bases de datos. 
- Aislamiento y responsabilidad única de cada módulo. 


# Requisitos de Entrega y Demostración 
La entrega final del proyecto no sólo incluye el código, sino también la demostración práctica y la evidencia del funcionamiento del sistema de microservicios. 

**Código Funcional (fork Git)** 



El requisito fundamental es la entrega del código fuente completo y funcional. 

- **Plataforma**: El código debe estar alojado en un repositorio Git. 
- **Contenido:** Debe incluir todos los componentes del sistema OdontoCare, siguiendo la arquitectura distribuida definida (servicios de Usuarios y Citas). 

El estudiante debe desarrollar y presentar un conjunto de scripts que demuestren de forma práctica el funcionamiento de los servicios. 

**Pruebas de Integración (Opcional)** 

Opcionalmente se pueden incluir o desarrollar pruebas de integración que validen la comunicación entre los servicios y el acceso externo a los endpoints. 

Las pruebas de integración podrán incluir cualquiera de los siguientes métodos: 

- **Scripts** que realicen llamamientos directos a los endpoints del servicio (usando librerías HTTP o pedidos como curl). 
- Implementación de pruebas unitarias utilizando unittest o el módulo flask.testing. 

**Documentación de pruebas de Endpoints** 



Entrega de documentación o scripts con la siguiente información claramente indicada para cada prueba de endpoint: 

1. El Endpoint Utilizado: **La ruta completa del servicio REST**. 
1. El Archivo de Entrada: **El cuerpo de la solicitud enviado, obligatoriamente en formato JSON**. 

