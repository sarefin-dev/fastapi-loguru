**Commands so far**
py -m pip install --upgrade pip
pip install -r .\requirements.txt

**Sequence Diagram**
(Special thanks to coderabbitai)
```mermaid
sequenceDiagram
    participant FastAPI App
    participant Lifespan Manager
    participant Settings (Config)
    participant Logging Setup
    participant Loguru
    participant Stdlib Logging
    
    FastAPI App->>Lifespan Manager: startup (FastAPI lifespan)
    Lifespan Manager->>Settings (Config): get_settings()
    Settings (Config)-->>Lifespan Manager: AppSettings from .env
    Lifespan Manager->>Logging Setup: setup_logging()
    Logging Setup->>Loguru: remove handlers, configure console sink
    Logging Setup->>Loguru: add JSON file sink (production)
    Logging Setup->>Stdlib Logging: intercept_all_loggers()
    Stdlib Logging->>Loguru: route via InterceptHandler
    Loguru-->>Logging Setup: initialized
    Logging Setup-->>Lifespan Manager: complete
    Lifespan Manager->>Loguru: log startup message
    Loguru-->>FastAPI App: logging ready
    Note over FastAPI App: App running with integrated logging