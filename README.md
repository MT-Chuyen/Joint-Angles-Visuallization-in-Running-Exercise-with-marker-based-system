# Joint-Angles-Visuallization-in-Running-Exercise-with-marker-based-system

# Angle Measurement for Running Exercise Analysis

[![Example Angle Plot](link_to_example_plot_image.png)](link_to_github_repository)

This project automates the analysis of running biomechanics by measuring joint angles (knee, pelvis, hip, ankle) during a running cycle. It synchronizes data from the MR3 plantar pressure system and the Nexus motion capture system to provide insights into running performance and potential injury risks. The code processes plantar pressure data to define running cycles and then maps angle data from motion capture to those cycles, handling variability in cycle length and segmented input files.

## Key Features

*   **Data Synchronization:** Integrates data from MR3 and Nexus systems based on timestamps.
*   **Cycle Identification:** Automatically identifies start and end frames for each running cycle from plantar pressure data.
*   **Angle Extraction:** Extracts and processes joint angle data for each identified running cycle.
*   **Cycle Normalization:** Scales each cycle to a uniform length for comparative analysis.
*   **Statistical Analysis:** Calculates average angle trajectories and standard deviations.
*   **Data Visualization:** Generates plots of joint angles over the running cycle.

