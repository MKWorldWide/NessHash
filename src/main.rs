use clap::{Parser, Subcommand};

mod controller;

/// Command-line interface definition using Clap.
#[derive(Parser)]
#[command(name = "NessHash", version = "0.1.0", author = "NessHash Team")]
struct Cli {
    /// Optional subcommand to run a specific controller
    #[command(subcommand)]
    command: Option<Commands>,
}

/// Available subcommands for granular control over the system.
#[derive(Subcommand)]
enum Commands {
    /// Boot the entire terraforming flow
    Boot,
    /// Trigger the atmospheric regulation cycle only
    Regulate,
    /// Route resonance waves without starting other systems
    Route,
}

fn main() {
    let cli = Cli::parse();
    match cli.command.unwrap_or(Commands::Boot) {
        Commands::Boot => {
            println!("NessHash core booting...");
            controller::terraforming_engine::initiate();
            controller::atmospheric_control::regulate();
            controller::resonance_router::route();
        }
        Commands::Regulate => controller::atmospheric_control::regulate(),
        Commands::Route => controller::resonance_router::route(),
    }
}
