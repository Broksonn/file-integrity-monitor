# 🛡️ File Integrity Monitor

A lightweight Python security tool that monitors a designated directory for file changes in real-time. It calculates cryptographic hashes to detect unauthorized modifications, providing a basic foundation for file system auditing.

## 📌 Features
* **Real-time Monitoring:** Utilizes the `watchdog` library to instantly detect file system events.
* **Cryptographic Hashing:** Computes **SHA-256** checksums (`hashlib`) to verify data integrity and detect content tampering.
* **Event Detection:** Accurately logs file creations, modifications, and deletions.
* **Memory Efficient:** Reads files in chunks to safely process large files without exhausting RAM.

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/Broksonn/file-integrity-monitor.git
   cd file-integrity-monitor
   ```

2. Create and activate a virtual environment:
   **Windows:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
   **Linux / macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
   ```bash
   python integrity_monitor.py
   ```

*Note: Drop any files into the `monitored_folder` directory to see the real-time event logging in the console.*