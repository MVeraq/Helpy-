# 📋 Cómo Actualizar las Categorías en Helpy

## Pasos para actualizar las categorías en la base de datos

### 1. Activar el entorno virtual (si es necesario)
```bash
# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 2. Navegar al directorio del proyecto
```bash
cd helpy
```

### 3. Ejecutar el comando de Django para crear/actualizar categorías
```bash
python manage.py crear_categorias
```

## ¿Qué hace este comando?

El comando `crear_categorias`:
- ✅ **Crea** las categorías que no existen en la base de datos
- ⚠️ **No modifica** las categorías que ya existen (para evitar sobrescribir datos)
- 📝 Muestra un mensaje para cada categoría indicando si fue creada o si ya existía

## Ejemplo de salida

```
✅ Creada: 🤝 Ayuda comunitaria
✅ Creada: 🍽️ Asistencia alimentaria
⚠️  Ya existe: ⛑️ Salud y bienestar
✅ Creada: 🚨 Emergencias y desastres
...
```

## Nota importante

Si necesitas **modificar** categorías existentes (cambiar nombre, descripción, color o icono), tienes dos opciones:

### Opción 1: Usar el panel de administración de Django
1. Accede a `/admin` en tu navegador
2. Ve a "Categorías"
3. Edita manualmente cada categoría

### Opción 2: Modificar el código y eliminar las categorías existentes
1. Elimina las categorías desde el admin o usando el shell de Django:
   ```bash
   python manage.py shell
   ```
   ```python
   from Humanet.models import Categoria
   Categoria.objects.all().delete()
   ```
2. Ejecuta nuevamente:
   ```bash
   python manage.py crear_categorias
   ```

## Categorías actuales

El sistema incluye las siguientes categorías:

1. 🤝 **Ayuda comunitaria**
2. 🍽️ **Asistencia alimentaria**
3. ⛑️ **Salud y bienestar**
4. 📚 **Educación y capacitación**
5. ❤️ **Donaciones y colectas**
6. 👵 **Ayuda a grupos vulnerables**
7. 🐶 **Protección animal**
8. 🌱 **Medio ambiente**
9. 🎨 **Actividades recreativas**
10. 🥾 **Trabajo en terreno**
11. 🚨 **Emergencias y desastres** (nueva)
12. 💻 **Tecnología e innovación social** (nueva)

