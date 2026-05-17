cat << 'EOF' > README.md
# Autonomous Decentralized UAV Swarm with Onboard Edge AI

### A Joint Venture Project by PIEAS & SAFSHIKAN

This repository contains the architecture, firmware configuration guidelines, and hardware overview for a budget-friendly, highly optimized micro-UAV swarm platform. Designed specifically as an experimental testbed, the platform runs decentralized peer-to-peer communication (ESP-NOW) and localized computer vision inference (Edge AI) without relying on centralized ground stations or internet connectivity.

## System Architecture

The platform decouples high-level machine learning and communication tasks from low-level flight control using a dedicated **Dual-MCU Architecture**. This guarantees deterministic flight stability while handling heavy parallel computing workloads.

```mermaid
graph TB
    subgraph DRONE_UNIT [DRONE UNIT]
        direction TB
        ESP32[ESP32-S3 AI Engine] <-->|MAVLink over UART| STM32[STM32F405 Flight Control]
        
        CAM[OV2640 / OV5640 Camera] --->|Parallel DVP| ESP32
        ESP32 --->|ESP-NOW Mesh RF 2.4GHz| SWARM[Swarm Network  Up to 20 Nodes]
        
        IMU[ICM-42688-P IMU] --->|SPI| STM32
        BARO[SPL06-001 Barometer] --->|SPI / I2C| STM32
        
        STM32 --->|Attitude Tracking| ATT[Attitude Estimation]
        STM32 --->|Altitude Tracking| ALT[Altitude Estimation]
    end

    style DRONE_UNIT fill:#f9f9f9,stroke:#333,stroke-width:2px;
    style ESP32 fill:#d4ebf2,stroke:#007799,stroke-width:1px;
    style STM32 fill:#ffe6cc,stroke:#d79b00,stroke-width:1px;

## Core Specifications

### 1. Dual-MCU Embedded Processing

* **Primary Flight Controller (STM32F405 ARM Cortex-M4):**
  * Handles real-time flight control loops, sensor fusion, and navigation.
  * Interfaced via high-speed SPI with the **ICM-42688-P** (6-axis IMU) and **SPL06-001** (barometer).
  * Runs a custom-compiled, lightweight build of **ArduPilot** autopilot.

* **AI Companion Computer & Comms Processor (ESP32-S3 Dual-Core Xtensa LX7):**
  * Handles image capture, neural network processing, and peer-to-peer radio transmission.
  * Direct parallel DVP interface with **OV2640 / OV5640** camera modules.

* **Inter-Processor Bridge:**
  * High-speed hardware UART serial connection.
  * Communication formalized using the industrial **MAVLink** protocol for robust packet parsing.

### 2. Hardware Design Evolution

The physical drone hardware was scaled through a strict prototyping workflow to achieve flight readiness:

* **Phase 1 (Breadboard):** Used for initial logic proofing, driver development, and validating MAVLink communication between microcontrollers.
* **Phase 2 (Veroboard):** Soldered circuitry created to eliminate loose jumper contacts, stabilize voltage rails, and enable bench testing under motor vibrations.
* **Phase 3 (Custom 4-Layer PCB):**
  * Designed a high-density, lightweight integrated flight controller.
  * Multi-layer stackup allocates internal solid ground (GND) and power planes to serve as a Faraday cage.
  * Shields sensitive analog sensors (IMU, Barometer) from high-frequency RF noise (ESP32-S3 2.4GHz) and high-current BLDC power surges.
  * Support integrated for both micro-coreless motors and standard brushless DC (BLDC) motors.
* **Phase 4 (CAD Airframe):** Custom-designed physical frames modeled in CAD software, balancing structural rigidity, center of gravity (CoG), and lightweight payload protection.

### 3. Decentralized Peer-to-Peer Mesh (ESP-NOW)

* **Protocol:** Operates on the 2.4GHz band using connectionless **ESP-NOW** packets to eliminate Wi-Fi handshake overhead.
* **Mesh Topology:** Dynamic, ad-hoc peer-to-peer networking where nodes continuously broadcast local telemetry and hazard data.
* **Range:** Up to 125 meters node-to-node line of sight.
* **Scalability:** Supports up to 20 active, collaborative nodes simultaneously.
* **Resilience:** Self-healing routing structure. If a single node goes offline, other nodes dynamically redirect traffic.

### 4. TinyML Edge AI Pipeline

* **Framework:** Models optimized, trained, and compiled using **Edge Impulse**.
* **Quantization:** Converted from FP32 to INT8 precision to comfortably fit within the hardware limits of the ESP32-S3.
* **Resolution:** 96 x 96 input size for optimal processing-to-accuracy balance.
* **Performance:**
  * **Human Detection (Survivor Search):** 95% accuracy with an onboard latency of **550 ms**.
  * **Hazard Detection (Fire & Smoke):** Onboard latency of **670 ms**.
  * **Streaming:** Parallel processing captures images at 320 x 240 and crops/downsamples on-the-fly to prevent memory overflows.

## Technical Competency Matrix

This project demonstrates several high-value, industrial-grade engineering competencies:

* **High-Speed hardware design:** 4-layer PCB design, EMI/EMC shielding, and differential signal routing.
* **Embedded firmware engineering:** Bare-metal C/C++ development, custom RTOS implementation, and custom Autopilot integration.
* **Edge computing & Machine Learning:** Model quantization, hardware-constrained optimization, and camera sensor interfacing.
* **Robotics networking:** Decentralized communication protocols, low-overhead RF transmission, and telemetry systems.
EOF
