/// Basic climate parameters for the target environment.
#[derive(Clone, Debug)]
pub struct ClimateProfile {
    /// Desired average surface temperature in Celsius.
    pub temperature: f32,
}
