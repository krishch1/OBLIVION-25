# Oblivion Demo Flow: Secure Data Destruction & Verification

## Purpose

This document details the step-by-step process for the Oblivion project demo. It serves as a script for the Day 11 recording and provides the technical blueprint for the `wipe_script.sh` to be implemented by Isaac. The goal is to demonstrably prove that sensitive data has been securely and unrecoverably wiped.

## 1. Demo Scenario

The user has a sensitive file, for example, a `private_tax_records.pdf`, that needs to be permanently deleted from a system. Simply using `rm` is insufficient as the data can be recovered with forensic tools. The user wants to prove that the data is gone forever and receive a verifiable certificate of destruction.

## 2. Pre-Wipe State

- **User Action:** The user will navigate to a terminal and show the existence of a file, such as `sensitive_data.txt`.
    
- **Narration:** "Before we use Oblivion, let's look at a sensitive file. We'll create a simple file, and then we'll get a unique fingerprint of its data using SHA256. This is our baseline, the 'before' state."
    
- **Technical Steps (to be included in the script):**
    
    - Create a dummy file and write some identifiable text to it.
        
    - Calculate and display the pre-wipe SHA256 hash.
        

```
# Create a dummy file with sensitive information
echo "This is highly confidential information that must be permanently destroyed. This is a secret: 5f98a2c3-d7e1-4b10-9f0a-1a0e1b2f3c4d" > sensitive_data.txt

# Calculate the initial SHA256 hash
sha256sum sensitive_data.txt
```

## 3. The Oblivion Wipe Process

- **User Action:** The user will execute the `wipe_script.sh` and pass the sensitive file as an argument.
    
- **Narration:** "Now we'll use the Oblivion wipe script. This isn't a simple `rm` command. It will overwrite the file's data multiple times, making it unrecoverable."
    
- **Technical Steps (to be implemented by Isaac in `wipe_script.sh`):**
    
    - The script will use `dd` to create a loopback file, format it, and mount it.
        
    - The script will then call the core data-wiping utility, `shred`.
        
    - The `shred` command will overwrite the file's contents with random data. The `-u` flag will ensure the file is deallocated after overwriting. The `-v` flag can be used for a verbose output to show the process.
        

```
# Example command within the script
# This will be encapsulated in projects/oblivion/scripts/wipe_script.sh
FILE_TO_WIPE="sensitive_data.txt"

echo "Wiping data with Oblivion..."
shred -f -u -z -v "${FILE_TO_WIPE}"

echo "Wipe complete."
```

## 4. Post-Wipe State & Verification

- **User Action:** The user will show that the file no longer exists and attempt to calculate its hash.
    
- **Narration:** "The file has been removed. You can see it's no longer in our directory. We can't even calculate its hash because the file is gone. But is the data truly gone?"
    
- **Technical Steps:**
    
    - The script or a manual command will attempt `ls` and `sha256sum`, which will fail, proving the file is deleted.
        

```
ls sensitive_data.txt
# Expected output: No such file or directory

sha256sum sensitive_data.txt
# Expected output: sha256sum: sensitive_data.txt: No such file or directory
```

## 5. Forensic Recovery Attempt (Proof of Destruction)

- **User Action:** The user will run a simulated forensic recovery tool (or show a pre-recorded log/screenshot of the result).
    
- **Narration:** "To prove our method is effective, we'll try to recover the data using a forensic tool like `photorec` or `grep` on the disk block. As you can see, the original 'secret' text is no longer present, demonstrating a successful and secure wipe."
    
- **Technical Steps (for Isaac's `forensic_report.md`):**
    
    - The `wipe_script.sh` will calculate the post-wipe SHA256 of the _entire disk block_ to show that the file data is now just random bits.
        
    - This step directly ties into Isaac's task of capturing forensic evidence.
        

## 6. The Oblivion Certificate

- **User Action:** The script will output a JSON object to the terminal representing the Certificate of Destruction.
    
- **Narration:** "After a successful wipe, Oblivion issues a verifiable, signed certificate. This certificate includes the pre-wipe hash and a digital signature, providing irrefutable proof of destruction for auditing or compliance."
    
- **Technical Steps (for future implementation by Krish and Apurv):**
    
    - The `wipe_script.sh` will call a backend API endpoint (`/oblivion/issue`).
        
    - This endpoint receives the log data (hashes, timestamp, filename).
        
    - It signs this data using a private key and returns the signed certificate JSON.
        

```
{
  "wipe_id": "8c45d2e7-f1c5-4a2b-9e0c-8d1f2e3g4h5i",
  "filename": "sensitive_data.txt",
  "timestamp": "2025-09-10T12:00:00Z",
  "pre_wipe_sha256": "5f98a2c3-d7e1-4b10-9f0a-1a0e1b2f3c4d...",
  "post_wipe_sha256": "9b1e7c5d-3a2f-1e7d-9a8c-1e2f3a4b5d6e...",
  "signed_certificate": "..."
}
```

## Expected Outcome

The demo will successfully prove that Oblivion provides a comprehensive solution for secure data destruction, going beyond simple deletion to offer unrecoverable data erasure and a cryptographically verifiable certificate.