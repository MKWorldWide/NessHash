# Architecture Overview

NessHash is composed of modular layers written primarily in Rust and Python. The
core engine exposes a library (`nesshash_core`) that orchestrates controllers
responsible for atmospheric regulation and resonance routing. AI components are
implemented in Python for rapid iteration and leverage Rust bindings where
performance is critical.

```
+------------------+
|    CLI / API     |
+---------+--------+
          |
          v
+---------+--------+
|  nesshash_core   |  <-- Rust library (controllers & models)
+---------+--------+
          |
          v
+---------+--------+
|   Python AI      |  <-- ML modules for emotion and warmth processing
+------------------+
```

Future expansions will integrate distributed ledgers for audit trails and
Terraform scripts to simulate planetary resources.
