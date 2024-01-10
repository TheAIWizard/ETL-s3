#!/bin/sh

SOURCE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/"
ARCHIVE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/Archive annotations/"

# Retrieve activity description to annotate and archive them
file_list=$(mc ls "$SOURCE_PATH" | grep -E '\.csv$|\.parquet$' | awk '{print $6}')

if [ -z "$file_list" ]; then
    echo "No files to annotate"
else
    echo "Files to annotate: $file_list"

    # Iterate over each filename
    for filename in $file_list; do
        echo "Moving file: $filename"

        # Retrieves activity description from s3
        mc cp "$SOURCE_PATH$filename" ./

        # Transform and save batch data to annotate
        [ -n "$filename" ] && python transform_to_json.py "$filename"

        # Move the treated batch data to archive
        [ -n "$filename" ] && mc mv "$filename" "$ARCHIVE_PATH"
    done
fi
