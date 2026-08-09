# Oblivion Forensic Analysis Report

## Objective
To verify the effectiveness of the `wipe_script.sh` data sanitization process by attempting file recovery using the `photorec` forensic tool.

## Procedure
1. An `oblivion_disk.img` file was generated using the `wipe_script.sh`. This script creates a disk image, writes data, and uses the `shred` utility for a 3-pass overwrite.
2. The `photorec_win.exe` tool was run against the shredded `oblivion_disk.img` file.
3. A full scan for recoverable files was performed.

## Results
The `photorec` scan completed and was able to successfully recover **2 files**. This indicates that some data remnants or file signatures remained on the disk image after the `shred` process.

## Evidence
The following screenshot shows the final result from the `photorec` scan, confirming that 2 files were saved.

![Photorec Scan Results](</demos/screenshots/oblivion_forensic_report.png>)

## Conclusion
The test confirms that while the `shred`-based wipe procedure significantly damages data, it is **not 100% effective** at preventing recovery by advanced forensic tools like `photorec`. This is a critical finding that will inform the future development of the Oblivion tool.