//! Core library for the NessHash terraform engine.
//!
//! This module exposes high-level abstractions and initialization logic
//! for managing the controller and model layers. The intent is to allow
//! binaries and integrations to initialize the engine in a consistent
//! and maintainable manner.

pub mod controller {
    pub mod atmospheric_control;
    pub mod resonance_router;
    pub mod terraforming_engine;
}

pub mod models {
    pub mod breath_signature;
    pub mod climate_profile;
}

use models::{breath_signature::BreathSignature, climate_profile::ClimateProfile};

/// Configuration parameters for initializing the NessHash core.
#[derive(Default)]
pub struct Config {
    pub initial_signature: Option<BreathSignature>,
    pub initial_climate: Option<ClimateProfile>,
}

/// Central struct representing the running NessHash engine.
pub struct NessHashCore {
    config: Config,
}

impl NessHashCore {
    /// Instantiate a new engine with the provided configuration.
    pub fn new(config: Config) -> Self {
        Self { config }
    }

    /// Boot the core, preparing controllers and logging status.
    pub fn boot(&self) {
        println!("NessHash core booting...");
        if let Some(sig) = &self.config.initial_signature {
            println!("Loaded breath signature: {} Hz", sig.frequency);
        }
        if let Some(profile) = &self.config.initial_climate {
            println!("Target temperature: {}°C", profile.temperature);
        }
    }
}
