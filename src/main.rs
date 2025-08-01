// Clap provides a declarative macro-based CLI parser. This allows us to
// easily extend runtime parameters without hand-rolling argument logic.
use clap::Parser;
use nesshash_core::{
    BreathSignature,
    ClimateProfile,
    Config,
    NessHashCore,
};

/// Command line options for configuring the engine at startup.
#[derive(Parser, Debug)]
#[command(author, version, about)]
struct Args {
    /// Frequency in Hz used for the initial breath signature
    #[arg(long, default_value_t = 528.0)]
    signature_frequency: f32,

    /// Desired average temperature in Celsius
    #[arg(long, default_value_t = 20.0)]
    temperature: f32,
}

/// Entry point for the NessHash binary. Initializes configuration and boots
/// the core engine. Additional CLI options will be added in future iterations
/// to configure runtime behavior.
fn main() {
    // Parse CLI parameters. In a production setting error handling would
    // include user-friendly messages and logging.
    let args = Args::parse();

    // Build configuration from CLI values so the core can boot with
    // custom parameters.
    let config = Config {
        initial_signature: Some(BreathSignature {
            frequency: args.signature_frequency,
        }),
        initial_climate: Some(ClimateProfile {
            temperature: args.temperature,
        }),
    };

    let engine = NessHashCore::new(config);
    engine.boot();
}
