# 🔄 Guía Rápida de Git/GitHub

## ¿Los cambios en VS Code se reflejan en GitHub automáticamente?

**NO** ❌ - Debes subirlos manualmente con estos 3 pasos:

## 📝 Flujo Básico de Trabajo

### 1️⃣ Ver qué cambió

```bash
git status
```

Muestra archivos modificados, nuevos, o eliminados.

### 2️⃣ Agregar cambios al "staging"

```bash
# Agregar UN archivo específico
git add nombre-archivo.py

# Agregar VARIOS archivos
git add archivo1.md archivo2.html

# Agregar TODOS los cambios
git add .
```

### 3️⃣ Guardar cambios con commit

```bash
git commit -m "descripción clara del cambio"
```

**Ejemplos de mensajes**:

- `"docs: Actualizar README con nuevas instrucciones"`
- `"feat: Agregar nueva función de agregación"`
- `"fix: Corregir error en schema de BigQuery"`
- `"refactor: Mejorar estructura del código"`

### 4️⃣ Subir a GitHub

```bash
git push origin main
```

## 🚀 Comandos Completos (Copiar y Pegar)

### Caso 1: Modificaste 1 archivo

```bash
git add nombre-archivo.md
git commit -m "docs: Actualizar documentación"
git push origin main
```

### Caso 2: Modificaste varios archivos

```bash
git add .
git commit -m "refactor: Mejoras generales en el proyecto"
git push origin main
```

### Caso 3: Solo quieres subir ciertos archivos

```bash
git add archivo1.py archivo2.md archivo3.html
git commit -m "feat: Implementar nuevas funcionalidades"
git push origin main
```

## 🔍 Comandos Útiles de Verificación

### Ver cambios realizados (antes de commit)

```bash
git diff
```

### Ver historial de commits

```bash
git log --oneline -10
```

Muestra últimos 10 commits.

### Ver archivos en staging

```bash
git diff --staged
```

### Deshacer cambios (antes de commit)

```bash
# Descartar cambios en UN archivo
git restore nombre-archivo.py

# Descartar TODOS los cambios no guardados
git restore .
```

### Quitar archivo del staging (pero mantener cambios)

```bash
git restore --staged nombre-archivo.py
```

## 📊 Ver Estado Actual

```bash
# Estado completo
git status

# Estado resumido
git status -s
```

**Símbolos**:

- `M` = Modificado
- `A` = Agregado (nuevo)
- `D` = Eliminado
- `??` = No versionado

## 🔄 Sincronizar con GitHub

### Traer últimos cambios del repositorio

```bash
git pull origin main
```

**Importante**: Hazlo ANTES de empezar a trabajar si colaboras con otros.

### Ver repositorio remoto

```bash
git remote -v
```

## ⚠️ Errores Comunes

### Error: "Updates were rejected"

**Causa**: Hay cambios en GitHub que no tienes localmente.

**Solución**:

```bash
git pull origin main --rebase
git push origin main
```

### Error: "Nothing to commit"

**Causa**: No hay cambios sin guardar.

**Verificar**: `git status`

### Error: "Please tell me who you are"

**Solución** (solo primera vez):

```bash
git config --global user.email "tu@email.com"
git config --global user.name "Tu Nombre"
```

## 🎯 Workflow Recomendado

### Cada vez que trabajes

1. **Antes de empezar**:

   ```bash
   git pull origin main
   ```

2. **Durante el trabajo**:
   - Edita archivos en VS Code
   - Guarda con Cmd+S (pero NO sube a GitHub)

3. **Después de terminar**:

   ```bash
   git status              # Ver qué cambió
   git add .               # Agregar todos los cambios
   git commit -m "mensaje" # Guardar con descripción
   git push origin main    # Subir a GitHub
   ```

## 📱 Ver Cambios en GitHub

Después de `git push`, ve a:

**<https://github.com/Edushuaia/streaming-serverless-pipeline>**

Los cambios aparecen inmediatamente en:

- Pestaña "Code" (archivos actualizados)
- Pestaña "Commits" (historial)

## 💡 Tips Profesionales

1. **Commits frecuentes**: No esperes a terminar todo. Haz commits pequeños y específicos.

2. **Mensajes descriptivos**:
   - ✅ `"fix: Corregir schema BigQuery INT64 en lugar de INTEGER"`
   - ❌ `"cambios"`

3. **Revisar antes de commit**:

   ```bash
   git status
   git diff
   ```

4. **Backup automático**: Al hacer `git push`, tu código está respaldado en GitHub.

## 🔗 Recursos Adicionales

- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Docs](https://docs.github.com/en)
- [Pro Git Book](https://git-scm.com/book/es/v2)

---

## 🎓 Ejemplo Práctico Completo

```bash
# 1. Ver estado actual
git status

# 2. Modificaste README.md y agregaste nuevo-archivo.py
# VS Code muestra "M" y "U" pero NO están en GitHub aún

# 3. Agregar cambios
git add README.md nuevo-archivo.py

# 4. Commit
git commit -m "docs: Actualizar README y agregar nueva función"

# 5. Subir a GitHub
git push origin main

# 6. Verificar en GitHub: https://github.com/Edushuaia/streaming-serverless-pipeline
```

---

**Recuerda**: `git push` es OBLIGATORIO para que tus cambios aparezcan en GitHub. VS Code solo guarda localmente.
