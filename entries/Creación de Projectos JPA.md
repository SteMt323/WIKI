# Guía: Crear un proyecto básico con JPA (Java Persistence API)

Esta guía paso a paso te muestra cómo crear un proyecto Java con **JPA** usando **Maven** y **Hibernate** como proveedor de JPA. Incluye desde las dependencias de Maven hasta ejemplos de código funcionales y cómo ejecutar el proyecto. Está pensada para ser clara y práctica para iniciarte rápido.

---

## Requisitos previos

- Java JDK 11+ instalado.
- Maven instalado (o usar el wrapper `mvnw`).
- IDE (IntelliJ IDEA, Eclipse, VS Code, etc.).
- Conexión a una base de datos (ejemplos con **H2** en memoria y **MySQL**).

---

## 1. Estructura mínima recomendada del proyecto

```
mi-proyecto-jpa/
├─ src/
│  ├─ main/
│  │  ├─ java/com/ejemplo/
│  │  │  ├─ App.java
│  │  │  ├─ model/Empleado.java
│  │  │  └─ repository/EmpleadoRepository.java
│  │  └─ resources/
│  │     └─ META-INF/persistence.xml
├─ pom.xml
```

---

## 2. `pom.xml` (dependencias principales)

Copia estas dependencias en tu `pom.xml`. Ajusta las versiones si lo necesitas.

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
             http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.ejemplo</groupId>
  <artifactId>mi-proyecto-jpa</artifactId>
  <version>1.0-SNAPSHOT</version>

  <properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
    <jakarta.persistence.version>3.1.0</jakarta.persistence.version>
    <hibernate.version>6.4.0.Final</hibernate.version>
  </properties>

  <dependencies>
    <!-- API de JPA (Jakarta Persistence) -->
    <dependency>
      <groupId>jakarta.persistence</groupId>
      <artifactId>jakarta.persistence-api</artifactId>
      <version>${jakarta.persistence.version}</version>
    </dependency>

    <!-- Hibernate (implementación de JPA) -->
    <dependency>
      <groupId>org.hibernate.orm</groupId>
      <artifactId>hibernate-core</artifactId>
      <version>${hibernate.version}</version>
    </dependency>

    <!-- Controlador H2 (base de datos en memoria, útil para pruebas) -->
    <dependency>
      <groupId>com.h2database</groupId>
      <artifactId>h2</artifactId>
      <version>2.1.214</version>
      <scope>runtime</scope>
    </dependency>

    <!-- (Opcional) Driver MySQL para usar MySQL en lugar de H2 -->
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>8.1.0</version>
      <scope>runtime</scope>
    </dependency>

    <!-- (Opcional) Logger para ver SQL en consola -->
    <dependency>
      <groupId>org.jboss.logging</groupId>
      <artifactId>jboss-logging</artifactId>
      <version>3.5.1.Final</version>
    </dependency>
  </dependencies>
</project>
```

> **Nota:** Las versiones mostradas son ejemplos estables; si usas versiones distintas, actualiza `hibernate.version` y `jakarta.persistence.version` según tu entorno.

---

## 3. Archivo de configuración `persistence.xml`

Crea el archivo `src/main/resources/META-INF/persistence.xml`. Abajo hay dos ejemplos: uno con **H2 (memoria)** y otro con **MySQL**.

### a) `persistence.xml` — H2 (rápido para pruebas)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<persistence xmlns="https://jakarta.ee/xml/ns/persistence"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="https://jakarta.ee/xml/ns/persistence https://jakarta.ee/xml/ns/persistence/persistence_3_0.xsd"
             version="3.0">
  <persistence-unit name="MiUnidadPersistencia" transaction-type="RESOURCE_LOCAL">
    <class>com.ejemplo.model.Empleado</class>
    <properties>
      <property name="jakarta.persistence.jdbc.url" value="jdbc:h2:mem:mi_bd;DB_CLOSE_DELAY=-1"/>
      <property name="jakarta.persistence.jdbc.driver" value="org.h2.Driver"/>
      <property name="jakarta.persistence.jdbc.user" value="sa"/>
      <property name="jakarta.persistence.jdbc.password" value=""/>

      <!-- Propiedades de Hibernate -->
      <property name="hibernate.dialect" value="org.hibernate.dialect.H2Dialect"/>
      <property name="hibernate.hbm2ddl.auto" value="update"/>
      <property name="hibernate.show_sql" value="true"/>
      <property name="hibernate.format_sql" value="true"/>
    </properties>
  </persistence-unit>
</persistence>
```

### b) `persistence.xml` — MySQL (producción/local)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<persistence xmlns="https://jakarta.ee/xml/ns/persistence"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="https://jakarta.ee/xml/ns/persistence https://jakarta.ee/xml/ns/persistence/persistence_3_0.xsd"
             version="3.0">
  <persistence-unit name="MiUnidadPersistencia" transaction-type="RESOURCE_LOCAL">
    <class>com.ejemplo.model.Empleado</class>
    <properties>
      <property name="jakarta.persistence.jdbc.url" value="jdbc:mysql://localhost:3306/mi_bd?useSSL=false&amp;serverTimezone=UTC"/>
      <property name="jakarta.persistence.jdbc.driver" value="com.mysql.cj.jdbc.Driver"/>
      <property name="jakarta.persistence.jdbc.user" value="root"/>
      <property name="jakarta.persistence.jdbc.password" value="tu_password"/>

      <!-- Propiedades de Hibernate -->
      <property name="hibernate.dialect" value="org.hibernate.dialect.MySQL8Dialect"/>
      <property name="hibernate.hbm2ddl.auto" value="update"/>
      <property name="hibernate.show_sql" value="true"/>
      <property name="hibernate.format_sql" value="true"/>
    </properties>
  </persistence-unit>
</persistence>
```

---

## 4. Clase entidad (Ejemplo `Empleado`)

Crea `src/main/java/com/ejemplo/model/Empleado.java`:

```java
package com.ejemplo.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Column;

@Entity
@Table(name = "empleados")
public class Empleado {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String nombre;

    private String puesto;

    public Empleado() {}

    public Empleado(String nombre, String puesto) {
        this.nombre = nombre;
        this.puesto = puesto;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getPuesto() { return puesto; }
    public void setPuesto(String puesto) { this.puesto = puesto; }

    @Override
    public String toString() {
        return "Empleado{" +
               "id=" + id +
               ", nombre='" + nombre + '\'' +
               ", puesto='" + puesto + '\'' +
               '}';
    }
}
```

---

## 5. Repositorio sencillo usando `EntityManager`

Crea `src/main/java/com/ejemplo/repository/EmpleadoRepository.java`:

```java
package com.ejemplo.repository;

import com.ejemplo.model.Empleado;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import java.util.List;

public class EmpleadoRepository {

    private final EntityManager em;

    public EmpleadoRepository(EntityManager em) {
        this.em = em;
    }

    public Empleado guardar(Empleado e) {
        em.getTransaction().begin();
        em.persist(e);
        em.getTransaction().commit();
        return e;
    }

    public Empleado buscarPorId(Long id) {
        return em.find(Empleado.class, id);
    }

    public List<Empleado> listarTodos() {
        TypedQuery<Empleado> q = em.createQuery("SELECT e FROM Empleado e", Empleado.class);
        return q.getResultList();
    }

    public Empleado actualizar(Empleado e) {
        em.getTransaction().begin();
        Empleado merged = em.merge(e);
        em.getTransaction().commit();
        return merged;
    }

    public void eliminar(Long id) {
        em.getTransaction().begin();
        Empleado e = em.find(Empleado.class, id);
        if (e != null) {
            em.remove(e);
        }
        em.getTransaction().commit();
    }
}
```

---

## 6. Clase `App` con ejemplo de uso

Crea `src/main/java/com/ejemplo/App.java`:

```java
package com.ejemplo;

import com.ejemplo.model.Empleado;
import com.ejemplo.repository.EmpleadoRepository;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import java.util.List;

public class App {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("MiUnidadPersistencia");
        EntityManager em = emf.createEntityManager();

        EmpleadoRepository repo = new EmpleadoRepository(em);

        // Crear y guardar
        Empleado ana = new Empleado("Ana López", "Analista");
        repo.guardar(ana);
        System.out.println("Guardado: " + ana);

        // Listar
        List<Empleado> empleados = repo.listarTodos();
        System.out.println("Empleados en BD: " + empleados);

        // Buscar por id
        Empleado e = repo.buscarPorId(ana.getId());
        System.out.println("Encontrado por ID: " + e);

        // Actualizar
        e.setPuesto("Senior Analyst");
        repo.actualizar(e);
        System.out.println("Actualizado: " + repo.buscarPorId(e.getId()));

        // Eliminar
        repo.eliminar(e.getId());
        System.out.println("Después de eliminar, lista: " + repo.listarTodos());

        em.close();
        emf.close();
    }
}
```

---

## 7. Comandos Maven útiles

- Compilar: `mvn clean compile`  
- Ejecutar el `main` (si usas plugin exec): `mvn exec:java -Dexec.mainClass="com.ejemplo.App"`  
- Empaquetar: `mvn package`

Si usas IntelliJ o Eclipse, puedes ejecutar la clase `App` directamente desde el IDE.

---

## 8. Consejos y buenas prácticas

- Para aplicaciones reales, considera usar **DataSource** administrado y transacciones gestionadas (JTA) si aplicable.  
- Evita usar `hibernate.hbm2ddl.auto = update` en producción; prefieres migraciones controladas (Flyway o Liquibase).  
- Usa `try/finally` o `try-with-resources` para garantizar el cierre del `EntityManager` y `EntityManagerFactory`.  
- Separa la lógica de persistencia (repositorios/DAOs) de la lógica de negocio.  
- Considera usar Spring Data JPA si trabajas en aplicaciones Spring para simplificar la implementación de repositorios.

---

## 9. Solución de problemas comunes

- **No se encuentra la unidad de persistencia:** Asegúrate de que `persistence.xml` esté en `src/main/resources/META-INF/`.  
- **Errores de driver JDBC:** Verifica la dependencia del driver (H2 o MySQL) y la URL de conexión.  
- **DDL no aplicado:** Revisa `hibernate.hbm2ddl.auto` y los logs (`hibernate.show_sql`).

---

## 10. Recursos adicionales

- Documentación de Jakarta Persistence (JPA)  
- Documentación de Hibernate ORM  
- Tutoriales y ejemplos oficiales de tu proveedor de base de datos

---

¡Listo! Con esto tienes una guía completa y funcional para crear un proyecto básico con JPA usando Maven y Hibernate. Sigue los pasos, copia los fragmentos y adapta la configuración a tu base de datos preferida.