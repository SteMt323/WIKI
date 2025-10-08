# 🗃️ Java Persistence API (JPA) — Conceptos Básicos

La **Java Persistence API (JPA)** es una especificación de Java que permite **gestionar la persistencia de datos** en aplicaciones mediante **mapeo objeto-relacional (ORM)**.  
Su objetivo principal es facilitar la interacción entre objetos Java y las tablas de una base de datos relacional sin necesidad de escribir sentencias SQL manualmente.

---

## ¿Qué es la Persistencia?

La **persistencia** se refiere a la capacidad de **almacenar y recuperar el estado de los objetos** en una base de datos u otro medio de almacenamiento permanente.

Por ejemplo, un objeto `Empleado` creado en una aplicación Java puede almacenarse como un registro en la tabla `empleados` de la base de datos.

---


### Entidades

Una **entidad** es una clase Java que representa una tabla en la base de datos.  
Cada instancia de la clase corresponde a una fila (registro) de dicha tabla.

**Características principales:**
- Debe estar anotada con `@Entity`.
- Debe tener un campo identificado como clave primaria con `@Id`.
- Debe tener un constructor público o protegido sin parámetros.

**Ejemplo:**

```java
import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Empleado {
    @Id
    private int id;
    private String nombre;
    private String puesto;

    // Constructor vacío requerido por JPA
    public Empleado() {}

    // Constructor con parámetros
    public Empleado(int id, String nombre, String puesto) {
        this.id = id;
        this.nombre = nombre;
        this.puesto = puesto;
    }

    // Getters y setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getPuesto() { return puesto; }
    public void setPuesto(String puesto) { this.puesto = puesto; }
}
```

---


### Unidad de Persistencia y `persistence.xml`

La **unidad de persistencia** define la configuración necesaria para que JPA se comunique con la base de datos.  
Esta configuración se declara en un archivo llamado `persistence.xml`, ubicado en `META-INF`.

**Ejemplo:**

```xml
<persistence xmlns="https://jakarta.ee/xml/ns/persistence"
             version="3.0">
  <persistence-unit name="MiUnidadPersistencia">
    <class>com.ejemplo.Empleado</class>
    <properties>
      <property name="jakarta.persistence.jdbc.url" value="jdbc:postgresql://localhost:3306/empresa"/>
      <property name="jakarta.persistence.jdbc.user" value="root"/>
      <property name="jakarta.persistence.jdbc.password" value="1234"/>
      <property name="jakarta.persistence.jdbc.driver" value="com.postgresql.cj.jdbc.Driver"/>
      <property name="hibernate.hbm2ddl.auto" value="update"/>
    </properties>
  </persistence-unit>
</persistence>
```



---



### Mapeo de Relaciones

JPA permite mapear relaciones entre entidades usando anotaciones específicas:

| Tipo de relación | Anotación | Ejemplo |
|------------------|-----------|---------|
| Uno a uno        | `@OneToOne` | Un empleado tiene un solo usuario |
| Uno a muchos     | `@OneToMany` | Un departamento tiene varios empleados |
| Muchos a uno     | `@ManyToOne` | Muchos empleados pertenecen a un departamento |
| Muchos a muchos  | `@ManyToMany` | Un proyecto puede tener varios empleados y viceversa |


**Ejemplo:**

```java
@Entity
public class Departamento {
    @Id
    private int id;
    private String nombre;

    @OneToMany(mappedBy = "departamento")
    private List<Empleado> empleados;
}
```

```java
@Entity
public class Empleado {
    @Id
    private int id;
    private String nombre;

    @ManyToOne
    private Departamento departamento;
}
```



---


### Anotaciones más comunes en JPA

| Anotación | Descripción |
|-----------|-------------|
| `@Entity` | Declara una clase como entidad persistente |
| `@Table` | Especifica el nombre de la tabla en la base de datos |
| `@Id` | Marca el campo como clave primaria |
| `@GeneratedValue` | Genera valores automáticamente para el campo ID |
| `@Column` | Define propiedades específicas de una columna |
| `@Transient` | Excluye un atributo de la persistencia |
| `@JoinColumn` | Define la columna usada en una relación |
| `@OneToOne`, `@OneToMany`, `@ManyToOne`, `@ManyToMany` | Mapean relaciones entre entidades |

**Ejemplo práctico:**

```java
@Entity
@Table(name = "empleados")
public class Empleado {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(name = "nombre", nullable = false, length = 100)
    private String nombre;

    @Transient
    private int edadTemporal; // No se guarda en la BD
}
```


---


### Ciclo de Vida de una Entidad

El ciclo de vida de un objeto en JPA se gestiona a través del **EntityManager**, que controla su estado:

| Estado | Descripción |
|---------|--------------|
| **New (transient)** | El objeto se ha creado, pero aún no está gestionado por JPA. |
| **Managed (persisted)** | El objeto está siendo gestionado y sincronizado con la base de datos. |
| **Detached** | El objeto fue gestionado, pero ahora está fuera del contexto de persistencia. |
| **Removed** | El objeto se ha marcado para ser eliminado de la base de datos. |

---

**Ejemplo con `EntityManager`:**

```java
EntityManagerFactory emf = Persistence.createEntityManagerFactory("MiUnidadPersistencia");
EntityManager em = emf.createEntityManager();

em.getTransaction().begin();

Empleado emp = new Empleado(1, "Ana López", "Analista");
em.persist(emp); // Estado: managed

em.getTransaction().commit();
em.close(); // emp pasa a detached
```


---

## Conclusión

JPA simplifica enormemente el manejo de bases de datos en Java, eliminando la necesidad de escribir SQL manual y proporcionando una forma **orientada a objetos y declarativa** de trabajar con datos persistentes.  
Entender las **entidades**, las **relaciones** y el **ciclo de vida** es fundamental para dominar esta tecnología.

---

<div class="highlight">
<b>Consejo:</b> Usa JPA junto con un framework como <code>Hibernate</code> para aprovechar sus capacidades avanzadas de ORM y caching.
</div>