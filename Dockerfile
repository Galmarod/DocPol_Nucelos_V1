FROM python:3.9.6-slim

# Evitar .pyc y forzar stdout inmediato
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema para PySide6/Qt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    inkscape \
    libegl1 \
    libgl1 \
    libxkbcommon0 \
    libfontconfig1 \
    libnss3 \
    libxcomposite1 \
    libxrandr2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-glib-1-2 \
    libxdamage1 \
    libgbm1 \
    libasound2 \
    libjpeg62-turbo \
    libpng16-16 \
    liblcms2-2 \
    libtiff5 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Variables de entorno para que QtWebEngine funcione en Docker
ENV QT_QPA_PLATFORM=offscreen
ENV QTWEBENGINE_DISABLE_GPU=1
ENV QT_OPENGL=software
ENV QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"
# Crear y usar directorio de trabajo
WORKDIR /app
# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del proyecto
COPY . /app/

# Puerto para FastAPI
EXPOSE 8080

# Comando para iniciar el worker
CMD ["python", "main.py"]
