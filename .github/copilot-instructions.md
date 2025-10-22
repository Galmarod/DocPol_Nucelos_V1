# DocPol AI Coding Agent Instructions

## Project Overview
DocPol is a Python-based document processing system that handles SVG template modifications and PDF generation. The project uses FastAPI for its API server and integrates with Streamlit for UI components.

## Architecture

### Core Components
- `api/api_server.py`: FastAPI server handling file uploads and document processing
- `controller/`: SVG manipulation logic (`modifySvg.py`, `svg_edits.py`)
- `model/`: Data processing modules (`tspan_replacer.py`)
- `view/main_window.py`: GUI implementation
- `worker/processor.py`: Background processing tasks

### Key Workflows
1. Document Processing:
   - SVG files are uploaded via API (`/docpolSaveFiles` endpoint)
   - Templates are processed through `controller/svg_edits.py`
   - Results are saved to `temp/` directory

## Development Patterns

### File Organization
- All temporary files go in `temp/`
- Templates are stored in `templates/{PDF,svgFiles,texts}`
- Each major component (api, controller, model, view) has its own package

### API Conventions
- File upload endpoints accept multipart/form-data
- Async operations use `asyncio.to_thread` for CPU-bound tasks
- Response files are zipped before sending

### Dependencies
Key external dependencies:
- FastAPI + uvicorn for API server
- PySide6 for GUI components
- Streamlit for web interface
- lxml for SVG processing

## Testing
- Test files are in `test/` directory
- Use `test_path.py` as reference for path handling tests

## Getting Started Guide

### Step 1: Install Required Software
1. Download and install Python 3.9.6 or later:
   - Go to https://www.python.org/downloads/
   - Click "Download Python 3.9.6"
   - Run the installer
   - **Important**: Check "Add Python to PATH" during installation

2. Install Inkscape:
   - Go to https://inkscape.org/release
   - Download and install the version for your operating system

### Step 2: Setup the Project
1. Open PowerShell or Command Prompt:
   - Press Windows + X
   - Click "Windows PowerShell" or "Command Prompt"

2. Install Python dependencies:
   ```
   cd path/to/DocPol_Nucelos_V1
   pip install -r requirements.txt
   ```
   - Wait for all packages to install (this may take a few minutes)

### Step 3: Running the Program
The program has two modes: API Server mode and GUI mode.

#### API Server Mode (Current)
1. Start the API server:
   ```
   python main.py
   ```
   This will:
   - Start the API server on `http://localhost:8000`
   - Allow file uploads through the `/docpolSaveFiles` endpoint
   - Process files in the background

#### GUI Mode
1. To use the graphic interface instead:
   - Open `main.py` in a text editor
   - Find this line: `proyecto.apitest()`
   - Change it to: `proyecto.remplace()`
   - Save the file

2. Then run:
   ```
   python main.py
   ```
   This will:
   - Open the PySide6-based graphic interface
   - Show the SVG template viewer
   - Allow interactive document processing

3. Choose Your Mode:
   - Use API mode for automated/programmatic processing
   - Use GUI mode for interactive visual editing

### Step 4: Viewing Results
- Check the `temp/` folder for processed files
- Log information is written to `bitacora.log`

### Common Issues and Solutions
1. If Python is not found:
   - Reinstall Python and make sure to check "Add Python to PATH"
   - Restart your computer

2. If packages fail to install:
   - Try running: `pip install --upgrade pip`
   - Then retry: `pip install -r requirements.txt`

3. If Inkscape is not found:
   - Make sure Inkscape is installed
   - Add Inkscape to your system PATH

## Common Operations
1. Running the API server:
   ```python
   # Initialize through main.py
   proyecto = Docpol()
   proyecto.apitest()  # Starts API server
   ```

2. SVG Processing:
   - SVG edits are defined in `edits/ediciones_utf8.json`
   - Use `controller.svg_edits.apply_svg_edits()` for modifications
   - Always backup SVGs before editing

## Environment Setup

### Local Development
1. Python Environment:
   - Python 3.9.6+ required
   - Install dependencies: `pip install -r requirements.txt`
   - Ensure system has Inkscape installed for SVG processing

### Docker Deployment
1. Build the Container:
   ```bash
   docker build -t mi-worker .
   ```

2. Run the Container:
   - Standard run: `docker run -p 8000:8000 -v $(pwd)/test_data:/data mi-worker`
   - Interactive shell: `docker run -it --entrypoint /bin/bash mi-worker`

3. Environment Variables:
   - `QT_QPA_PLATFORM=offscreen`: Required for headless Qt operation
   - `QTWEBENGINE_DISABLE_GPU=1`: Disables GPU acceleration
   - `QT_OPENGL=software`: Forces software OpenGL rendering
   - `QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"`: Required for containerized environment

### System Dependencies
Key system packages required (installed automatically in Docker):
- Inkscape for SVG processing
- Qt dependencies (libegl1, libgl1, etc.)
- Font and image processing libraries
- X11 dependencies for GUI components

## Logging
- Use `common/logs.py` for consistent logging
- Log files are written to `bitacora.log`

