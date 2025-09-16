# System Design Diagram Generator

System Design Diagram Generator is a Python-based CLI tool for generating architecture diagrams from PlantUML files (.puml), Python diagram files (.py using diagrams library), and Mermaid files (.mmd). It can be run directly as a Python module or deployed as a Docker container.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Development Environment Setup
- Install Python 3.9+: `python3 --version` (should be >= 3.9)
- Install Hatch package manager: `pip install hatch`
- Install system dependencies for diagram generation:
  - PlantUML: `sudo apt-get install -y plantuml`
  - Graphviz: `sudo apt-get install -y graphviz`
  - For Mermaid (optional): Install Node.js and `npm install -g @mermaid-js/mermaid-cli`

### Quick Development Setup (Manual)
When network/PyPI issues prevent Hatch environment creation:
- Install dependencies manually: `pip install click loguru diagrams pytest coverage pytest-cov pytest-mock pytest-asyncio pytest-xdist ruff mypy`
- Set PYTHONPATH: `export PYTHONPATH="${PYTHONPATH}:/path/to/repo/src"`
- Create version file: `echo 'version = "0.1.0-dev"' > src/sys_design_diagram/_version.py`

### Build and Test Process
- **NEVER CANCEL**: Test suite takes 8-10 seconds. Set timeout to 30+ minutes for safety.
- Run tests: `export PYTHONPATH="${PYTHONPATH}:/path/to/repo/src" && pytest -n auto`
- Expected: 74 tests pass, 100% coverage achieved in ~9 seconds
- If PlantUML/Graphviz missing, tests will fail with specific error messages

### Run the Application
- CLI Help: `python -m sys_design_diagram.cli --help`
- Version: `python -m sys_design_diagram.cli --version`
- Process all diagram types: `python -m sys_design_diagram.cli process-all -d input_dir -o output_dir`
- Process specific types:
  - PlantUML only: `python -m sys_design_diagram.cli plantuml -d input_dir -o output_dir`
  - Python diagrams only: `python -m sys_design_diagram.cli diagrams -d input_dir -o output_dir`
  - Mermaid only: `python -m sys_design_diagram.cli mermaid -d input_dir -o output_dir`

### Validation Process
- **ALWAYS run tests before and after changes**: `pytest -n auto`
- **ALWAYS test CLI functionality**: `python -m sys_design_diagram.cli process-all -d ./tests-data -o /tmp/test-output`
- Verify outputs: Check that PNG files are generated in output directory structure
- Test formatting: `ruff check --fix src/ tests/ && ruff format src/ tests/` (takes <1 second)
- Type checking: `mypy src/` (takes 2-3 seconds, may show loguru type warnings - these are expected)

### Pre-commit Hooks and CI
- Pre-commit configuration: `.githooks.d/.pre-commit-config.yaml`
- Environment setup: `.githooks.d/pre-commit_environment.yml`
- CI uses micromamba environment with pre-commit hooks
- **NEVER CANCEL**: CI build takes 2-5 minutes including Docker builds

## Docker Usage

### Docker Build (Local Development)
- **NEVER CANCEL**: Docker builds take 20-45 minutes. Set timeout to 60+ minutes.
- Local build: `docker build -f Dockerfile_local -t sys-design-diagram-local:latest .`
- Production build: `docker build -f Dockerfile -t sys-design-diagram:latest .`
- Note: Production build expects package to be published to PyPI

### Docker Compose
- Run all diagram types: `docker-compose up --build sdd-process-all`
- Run specific services: `sdd-plantuml`, `sdd-diagrams`, `sdd-build-locally`
- Output saved to `./sdd-outputs/` directories

### Test Docker Image
- Basic functionality: `docker run --rm image:latest --version`
- Help: `docker run --rm image:latest --help`
- Process sample data: `docker run --rm -v ./tests-data:/input -v ./output:/output image:latest process-all -d /input -o /output`

## Validation Scenarios

### End-to-End Testing
After making changes, ALWAYS run these validation steps:

1. **Unit Tests**: `pytest -n auto` (expect 74 tests, 100% coverage, ~9 seconds)

2. **CLI Functionality**: 
   ```bash
   mkdir -p /tmp/validation-output
   python -m sys_design_diagram.cli process-all -d ./tests-data -o /tmp/validation-output
   ```
   - Should complete in 1-2 seconds
   - Should generate PNG files in `/tmp/validation-output/design1/` and `/tmp/validation-output/design2/`
   - May show Mermaid CLI warnings (expected if mermaid-cli not installed)

3. **Code Quality**:
   - `ruff check --fix src/ tests/` (should pass, <1 second)
   - `ruff format src/ tests/` (should format files, <1 second)

## Common Issues and Solutions

### Build Issues
- **Network timeouts**: Common in CI environments. Use manual dependency installation method.
- **Missing system dependencies**: Install plantuml and graphviz via package manager
- **Hatch environment creation fails**: Fall back to manual pip installation with PYTHONPATH

### Test Failures
- **Missing PlantUML**: Tests fail with "plantuml command not found" - install plantuml package
- **Missing Graphviz**: Tests fail with "failed to execute PosixPath('dot')" - install graphviz package
- **Import errors**: Check PYTHONPATH is set correctly and includes src directory

### Runtime Issues
- **Mermaid warnings**: Expected if @mermaid-js/mermaid-cli not installed - creates placeholder files
- **Permission errors**: Ensure output directory is writable
- **Module not found**: Verify PYTHONPATH includes project src directory

## Repository Structure

### Key Directories
- `src/sys_design_diagram/`: Main source code
  - `cli.py`: Command-line interface
  - `plantuml.py`: PlantUML processing
  - `diagrams.py`: Python diagrams processing  
  - `mermaid.py`: Mermaid processing
  - `process_diagrams.py`: Main processing logic
- `tests/`: Comprehensive test suite (74 tests)
- `tests-data/`: Sample diagram files for testing
  - `design1/`: Contains .puml, .py, .mmd files
  - `design2/`: Additional test diagrams
- `.github/workflows/`: CI/CD pipeline definitions
- `.githooks.d/`: Pre-commit hook configurations

### Important Files
- `pyproject.toml`: Project configuration and dependencies
- `requirements.txt`: Minimal dependencies (just "hatch")
- `Dockerfile`: Production Docker image
- `Dockerfile_local`: Local development Docker image
- `compose.yaml`: Docker Compose services

### Build Artifacts (Auto-generated)
- `src/sys_design_diagram/_version.py`: Version file (created by hatch or manually)
- `tmp-output/`: Test coverage and reports
- `dist/`: Built packages (wheel files)

Always verify changes work with the sample data in `tests-data/` before committing.