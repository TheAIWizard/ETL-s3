#!/bin/bash

SOURCE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/"
ARCHIVE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/Archive annotations/"

# Retrieve activity description to annotate and archive them
mc ls "$SOURCE_PATH" | grep -E '\.csv$|\.parquet$' | awk '{print $6}' | while read -r filename; do
    export filename=$filename
    echo $filename
    [[ "$filename" == *.csv || "$filename" == *.parquet ]] && echo "Moving file: $filename" || echo "$filename is not a file to annotate"
    echo "$SOURCE_PATH$filename"
    # Retrieves activity description from s3
    [[ "$filename" == *.csv || "$filename" == *.parquet ]] && mc cp --recursive "$SOURCE_PATH$filename" ./
    # Transform and save batch data to annotate
    python transform_to_json.py $filename
    # Move the treated batch data to archive
    [[ "$filename" == *.csv || "$filename" == *.parquet ]] && mc mv "$SOURCE_PATH$filename" "$ARCHIVE_PATH"
done