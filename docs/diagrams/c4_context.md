# C4 Context Diagram

## MCP Modular Architecture - System Context

This diagram shows the MCP Modular Architecture system in its environment, including external actors and their interactions with the system.

```mermaid
C4Context
    title System Context Diagram for MCP Modular Architecture

    Person(developer, "Software Developer", "Builds and tests MCP-based applications using the CLI or SDK")
    Person(ai_agent, "AI Agent", "Interacts with the MCP server to access tools, resources, and prompts")

    System(mcp_system, "MCP Modular Architecture", "A layered reference implementation of the Model Context Protocol providing Tools, Resources, and Prompts through a clean architectural design")

    System_Ext(external_data, "External Data Sources", "Configuration files, log files, and other data accessed by resources")

    Rel(developer, mcp_system, "Uses CLI/SDK to interact with server", "CLI commands, SDK API calls")
    Rel(ai_agent, mcp_system, "Sends MCP requests", "JSON-RPC over STDIO")
    Rel(mcp_system, ai_agent, "Returns results", "JSON-RPC responses")
    Rel(mcp_system, external_data, "Reads configuration and data", "File I/O")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

## Diagram Explanation

### Actors

**Software Developer**
- Primary user of the system
- Interacts via CLI for testing and demonstration
- Uses SDK to build MCP clients
- Purpose: Develop, test, and demonstrate MCP capabilities

**AI Agent**
- External AI system (e.g., Claude, GPT)
- Connects to MCP server via STDIO transport
- Sends JSON-RPC formatted requests
- Purpose: Access tools, read resources, and retrieve prompts

### System

**MCP Modular Architecture**
- Core system implementing Model Context Protocol
- Exposes three MCP primitives: Tools, Resources, Prompts
- Layered architecture with five distinct layers
- Provides both CLI and SDK interfaces for different use cases

### External Systems

**External Data Sources**
- Configuration files (YAML)
- Log files
- Resource data (config, status)
- Purpose: Provide configuration and data to the system

### Key Interactions

1. **Developer → System**: CLI commands or SDK API calls for testing and integration
2. **AI Agent → System**: JSON-RPC requests over STDIO transport
3. **System → AI Agent**: JSON-RPC responses with tool results, resource contents, or prompt messages
4. **System → External Data**: Read configuration files and resource data

### Scope and Boundaries

The MCP Modular Architecture system is a self-contained reference implementation with clear boundaries:
- **Inside scope**: MCP server, tools, resources, prompts, transport layer, SDK, CLI
- **Outside scope**: AI agents, external applications, configuration files

This context diagram establishes the system boundary and shows how external actors interact with the MCP Modular Architecture at the highest level of abstraction.
