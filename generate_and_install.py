import os
import ast
import subprocess
import pkg_resources

project_path = r"C:\Users\CarlosPepinPeralta\OneDrive - EvoPoint Solutions\Escritorio\Generative AI POC\ProjectAI"
ignore_dirs = ['project-ai-venv', '__pycache__']
imports = set()

# Recorrer archivos .py del proyecto
for dirpath, dirnames, filenames in os.walk(project_path):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
    for filename in filenames:
        if filename.endswith(".py"):
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, encoding="latin-1") as f:
                        content = f.read()
                except Exception as e:
                    print(f"No se pudo leer {file_path}: {e}")
                    continue

            try:
                node = ast.parse(content, filename=filename)
                for n in ast.walk(node):
                    if isinstance(n, ast.Import):
                        for alias in n.names:
                            imports.add(alias.name.split('.')[0])
                    elif isinstance(n, ast.ImportFrom):
                        if n.module:
                            imports.add(n.module.split('.')[0])
            except Exception as e:
                print(f"Error de sintaxis en {file_path}: {e}")

# Mostrar las librerías detectadas
print("\n📦 Librerías detectadas:")
for i in sorted(imports):
    print(f"- {i}")

# Guardar en requirements-autogen.txt
req_file = os.path.join(project_path, "requirements-autogen.txt")
with open(req_file, "w", encoding="utf-8") as f:
    for lib in sorted(imports):
        f.write(f"{lib}\n")

print(f"\n✅ Archivo generado: {req_file}")

# Verificar e instalar solo si no está ya instalada
print("\n🚀 Instalando librerías faltantes...")
installed_packages = {pkg.key for pkg in pkg_resources.working_set}

for lib in sorted(imports):
    if lib.lower() not in installed_packages:
        print(f"🔧 Instalando {lib}...")
        try:
            subprocess.check_call(["pip", "install", lib])
        except subprocess.CalledProcessError:
            print(f"❌ No se pudo instalar: {lib}")
    else:
        print(f"✅ {lib} ya está instalado.")

print("\n🎉 Proceso completado.")
