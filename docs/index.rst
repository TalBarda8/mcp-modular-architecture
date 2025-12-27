.. MCP Modular Architecture documentation master file

MCP Modular Architecture - API Documentation
=============================================

Welcome to the MCP Modular Architecture API documentation. This documentation is
automatically generated from docstrings using Sphinx autodoc.

**Project Overview:**

The MCP Modular Architecture is an academic reference implementation demonstrating
professional software architecture principles through a layered, modular design.
The project implements a Model Context Protocol (MCP) server with tools, resources,
and prompts, showcasing clean architecture patterns and best practices.

**Key Features:**

* 5-layer modular architecture (Core → MCP → Transport → SDK → UI)
* Comprehensive test coverage (95.12%, 228 tests)
* Extensible design with registry pattern
* Transport abstraction (STDIO, HTTP-ready)
* Parallel processing support (multiprocessing + multithreading)

**Architecture Layers:**

1. **Core Infrastructure**: Configuration, logging, error handling
2. **MCP Layer**: Business logic for tools, resources, prompts
3. **Transport Layer**: Communication abstraction
4. **SDK Layer**: Client API wrapper
5. **UI Layer**: User-facing interfaces (CLI)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
