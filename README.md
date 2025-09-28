# 🛒 E-commerce Django - Tienda Online Completa

> **Una tienda online profesional construida con Django, integrada con MercadoPago para pagos y generación automática de facturas PDF.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 **¿Qué es este proyecto?**

Este es un **e-commerce completo** que incluye:

- ✅ **Catálogo de productos** con imágenes y categorías
- ✅ **Carrito de compras** persistente por usuario  
- ✅ **Sistema de usuarios** (registro, login, perfiles)
- ✅ **Pagos con MercadoPago** (tarjetas, transferencias)
- ✅ **Generación de facturas PDF** automática
- ✅ **Panel de administración** para gestionar productos
- ✅ **Sistema de descuentos** y control de stock
- ✅ **Responsive design** adaptado a móviles

---

## 🚀 **Instalación Paso a Paso**

### **Requisitos Previos**

Antes de empezar, asegúrate de tener instalado:

- **Python 3.8 o superior** → [Descargar aquí](https://www.python.org/downloads/)
- **Git** → [Descargar aquí](https://git-scm.com/downloads)

> **💡 Tip:** Para verificar si los tienes instalados, abre una terminal y ejecuta:
> ```bash
> python --version
> git --version
> ```

---

### **Paso 1: Descargar el Proyecto**

**Opción A: Con Git (Recomendado)**
```bash
git clone https://github.com/SantyCalz/ProyectoEcommerce.git
cd ProyectoEcommerce
```

**Opción B: Descarga Manual**
1. Ve a [https://github.com/SantyCalz/ProyectoEcommerce](https://github.com/SantyCalz/ProyectoEcommerce)
2. Haz clic en "Code" → "Download ZIP"
3. Extrae el archivo y navega a la carpeta

---

### **Paso 2: Crear Entorno Virtual**

**En Windows:**
```powershell
python -m venv env
env\Scripts\Activate.ps1
```

**En macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

> **✅ Sabrás que está activado** cuando veas `(env)` al inicio de tu terminal.

---

### **Paso 3: Instalar Dependencias**

Con el entorno virtual activado, instala todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

> **⏳ Esto puede tardar 1-2 minutos** mientras descarga Django, MercadoPago SDK, ReportLab y otras dependencias.

---

### **Paso 4: Configurar la Base de Datos**

Django necesita crear las tablas en la base de datos:

```bash
python manage.py migrate
```

> **💾 Esto creará automáticamente** el archivo `db.sqlite3` con todas las tablas necesarias.

---

### **Paso 5: Crear Administrador (Opcional pero Recomendado)**

Para acceder al panel de administración y agregar productos:

```bash
python manage.py createsuperuser
```

Te pedirá:
- **Username:** (elige el que quieras, ej: admin)
- **Email:** (tu email)
- **Password:** (mínimo 8 caracteres)

---

### **Paso 6: ¡Iniciar el Servidor!**

```bash
python manage.py runserver
```

> **🎉 ¡Listo!** Abre tu navegador y ve a: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🎯 **Primeros Pasos Después de la Instalación**

### **1. Acceder al Panel de Administración**
- Ve a: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- Usa las credenciales que creaste en el Paso 5
- Desde aquí puedes agregar productos, categorías y gestionar pedidos

### **2. Agregar Productos de Prueba**
1. En el admin, haz clic en "Categorias" → "Agregar"
2. Crea categorías como: "Electrónicos", "Ropa", "Libros"
3. Luego ve a "Productos" → "Agregar" y crea algunos productos

### **3. Probar la Tienda**
- Ve a la página principal: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Navega por los productos
- Regístrate como usuario
- Agrega productos al carrito
- Prueba el proceso de checkout

---

## 💳 **Sobre los Pagos**

> **ℹ️ El proyecto viene configurado** con credenciales de prueba de MercadoPago, así que puedes probar el checkout sin configurar nada adicional. Los pagos no serán reales, solo para demostración.

---

## 📁 **Estructura del Proyecto**

```
ProyectoEcommerce/
├── 📁 tienda/              # Configuración principal de Django
│   ├── settings.py         # Configuraciones del proyecto
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Para deployment
├── 📁 productos/           # Aplicación principal del e-commerce
│   ├── models.py          # Modelos de datos (Producto, Usuario, Carrito, etc.)
│   ├── views.py           # Lógica de negocio
│   ├── urls.py            # URLs de la aplicación
│   ├── forms.py           # Formularios
│   ├── admin.py           # Configuración del panel admin
│   └── templates/         # Plantillas HTML
├── 📁 static/             # Archivos CSS, JavaScript, imágenes
├── 📁 media/              # Imágenes subidas por usuarios
├── manage.py              # Comando principal de Django
├── requirements.txt       # Dependencias del proyecto
└── db.sqlite3            # Base de datos (se crea automáticamente)
```

---

## 🛠️ **Comandos Útiles**

```bash
# Activar entorno virtual (antes de cualquier comando)
# Windows:
env\Scripts\Activate.ps1
# Mac/Linux:
source env/bin/activate

# Iniciar servidor de desarrollo
python manage.py runserver

# Crear migraciones después de cambios en models.py
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Abrir shell interactivo de Django
python manage.py shell

# Recolectar archivos estáticos (para producción)
python manage.py collectstatic
```

---

## 🏆 **Características Técnicas**

- **Framework:** Django 5.2.6
- **Base de Datos:** SQLite 
- **Pagos:** MercadoPago SDK
- **PDFs:** ReportLab
- **Estilos:** CSS personalizado con animaciones

**¡Gracias por usar nuestro e-commerce! 🎉**
- Si agregas nuevas dependencias, instálalas con `pip install <paquete>` y considera usar un `requirements.txt`.
- Para dudas, revisa la documentación oficial de Django: https://docs.djangoproject.com/