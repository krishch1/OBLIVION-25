#!/bin/bash

# Define constants
FILE_NAME="oblivion_disk.img"
FILE_SIZE_MB=20
FILE_SIZE_BYTES=$((FILE_SIZE_MB * 1024 * 1024))
DUMMY_DATA="This is some dummy data to write to the disk image."
TIMESTAMP_FORMAT="%Y-%m-%dT%H:%M:%S%z"

# Capture start time in ISO 8601 format
START_TIME=$(date -u +"$TIMESTAMP_FORMAT")

# Create a 20MB file
dd if=/dev/zero of="$FILE_NAME" bs=1 count=0 seek="$FILE_SIZE_BYTES" 2>/dev/null

# Write some dummy data into it
echo "$DUMMY_DATA" >> "$FILE_NAME"

# Calculate the SHA256 hash of the file (pre-wipe)
PRE_WIPE_HASH=$(sha256sum "$FILE_NAME" | awk '{print $1}')

# Use the shred command to wipe the file.
# The -v flag is for verbose output (not required, but good for debugging)
# The -z flag adds a final overwrite with zeros to obscure shredding.
# The -n 3 flag is the number of times to overwrite.
shred -n 3 -z "$FILE_NAME" 2>/dev/null

# Calculate the SHA256 hash of the file again (post-wipe)
POST_WIPE_HASH=$(sha256sum "$FILE_NAME" | awk '{print $1}')

# Capture end time in ISO 8601 format
END_TIME=$(date -u +"$TIMESTAMP_FORMAT")

# Output a single, clean JSON object
cat <<EOF
{
  "targetDevice": "$FILE_NAME",
  "wipeMethod": "shred",
  "startTime": "$START_TIME",
  "endTime": "$END_TIME",
  "preWipeHash_sha256": "$PRE_WIPE_HASH",
  "postWipeHash_sha256": "$POST_WIPE_HASH"
}
EOF
