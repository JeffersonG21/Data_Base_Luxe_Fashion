# Data Base Luxe Fashion 👗🛍️  
Sistema de gestión de productos, materiales, órdenes y servicios para la empresa Luxe Fashion.  
Proyecto desarrollado en **Flask + SQLAlchemy + MySQL**, completamente dockerizado con **Docker Compose**.

---

## 🚀 Tecnologías utilizadas

- **Python 3**
- **Flask**
- **SQLAlchemy**
- **MySQL 8 (Docker)**
- **Docker & Docker Compose**
- **HTML (Jinja Templates)**

---

## Estructura de la Base de Datos

La base de datos de **Luxe Fashion** está organizada en varias tablas principales con relaciones que reflejan la gestión de productos, materiales, órdenes y servicios.

### Tablas principales y relaciones

- **Suppliers**  
  Almacena los proveedores de materiales.  

- **Materials**  
  Contiene los materiales disponibles para producción.  

- **Customers**  
  Información de los clientes que realizan órdenes.  

- **Products**  
  Productos que ofrece la empresa.  

- **GarmentBatches**  
  Lotes de prendas producidas de un producto específico.  

- **Orders**  
  Órdenes realizadas por los clientes.  

- **OrderDetails**  
  Detalles de cada orden, incluyendo productos y servicios asociados.

- **Services**  
  Servicios que se pueden agregar a las órdenes (por ejemplo, ajustes o personalizaciones).

- **MaterialUsed**  
  Relaciona materiales con lotes de prendas (**GarmentBatches**) indicando la cantidad utilizada.

---

Esta estructura permite llevar un **registro completo de la producción, inventario y ventas**, asegurando integridad y trazabilidad de los productos desde el proveedor hasta el cliente.

