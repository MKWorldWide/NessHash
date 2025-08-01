use nesshash_core::{Config, NessHashCore};

/// Entry point for the NessHash binary. Initializes configuration and boots
/// the core engine. Additional CLI options will be added in future iterations
/// to configure runtime behavior.
fn main() {
    // Basic configuration loaded with default values.
    let config = Config::default();

    let engine = NessHashCore::new(config);
    engine.boot();
}
