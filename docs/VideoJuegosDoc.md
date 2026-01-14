# Videojuegos Management System

This repository contains an application to manage a collection of video games. It uses **ZODB** for persistence and **BTrees** for in-memory data structures.

## High‑level architecture
- **Videojuego** – Persistent entity representing a video game.
- **SistemaVideojuegos** – Core system providing CRUD operations and search.
- **Main CLI** – Interactive menu that drives user actions.

## Core classes
### `Videojuego`
- Stores basic attributes: `nombre`, `edad`, `dificultad`, `horas_aprox`, `plataforma`, `precio`.
- Implements `__str__` for a human‑readable representation.
- `contiene_texto(texto)` – Helper to perform a case‑insensitive search across all fields.

### `SistemaVideojuegos`
- Handles database initialization, opening, and transaction management.
- Methods
  - `agregar_videojuego()` – Prompt user, create `Videojuego` instance, persist.
  - `editar_videojuego()` – Update existing record.
  - `eliminar_videojuego()` – Delete record after confirmation.
  - `buscar_videojuegos()` – Text‑based search across all fields.
  - `mostrar_todos()` – List all records.
  - `menu_principal()` – Main menu loop.
- Graceful shutdown via `cerrar()`.

## Usage
```bash
$ python Videojuegos.py
```
Follow the textual menu. The database is stored as `videojuegos.db` in the current directory.

## Dependencies
- `ZODB` – Object database.
- `BTrees` – Persistent B‑tree containers.
- `transaction` – Transaction manager for committing changes.

## Diagram
![System Flowchart](generated_docs/diagrams/system_flowchart.png)

*(The diagram is generated using Mermaid – see the `create_mermaid_diagram` tool.)*
