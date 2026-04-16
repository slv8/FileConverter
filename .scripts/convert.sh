#!/bin/bash

INPUT="$1"
OUTPUT="$2"
FORMAT="$3"

echo "Starting conversion from $INPUT to $OUTPUT as $FORMAT"

cp "$INPUT" "$OUTPUT"
if [ $? -ne 0 ]; then
  echo "Error: Failed to copy $INPUT to $OUTPUT" >&2
  exit 1
fi

for i in {1..10}; do
  sleep 1
  echo "progress:$((i * 10))"
done

echo "Conversion complete."





