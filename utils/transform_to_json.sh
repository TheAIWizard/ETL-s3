#!/bin/bash
set -x

SOURCE_PATH="s3/$S3_BUCKET/$S3_BUCKET_PREFIX_DEPOT_MANUEL"
ARCHIVE_PATH="s3/$S3_BUCKET/$S3_BUCKET_PREFIX_ARCHIVE_DEPOT_MANUEL"
TARGET_PATH="$S3_BUCKET_PREFIX_ANNOTATION_TARGET"

# Retrieve activity description to annotate and archive them
# 2>/dev/null suppress any error messages like syntax that may occur
files=$(mc ls "$SOURCE_PATH" 2>/dev/null | grep -E '\.csv$|\.parquet$' | awk '{print $6}')
if [ -n "$files" ]; then
    echo "Files found. Starting processing..."
    echo "$files" | while read -r filename; do
        case "$filename" in
            *.csv|*.parquet)
                echo "Moving file: $filename"
                
                # Retrieve activity description from s3
                mc cp --recursive "$SOURCE_PATH$filename" ./
                
                # Transform and save batch data to annotate
                python transform_to_json.py "$filename"

                # Create target S3 
                ID_S3_TARGET_VALUE=$(python s3_create_target.py "$TARGET_PATH")

                # Create or update the ConfigMap
                kubectl create configmap etl-label-studio-config --from-literal=ID_S3_TARGET=$ID_S3_TARGET_VALUE --dry-run=client -o yaml | kubectl apply -f -
                
                # Move the treated batch data to the archive
                mc mv "$SOURCE_PATH$filename" "$ARCHIVE_PATH"
                ;;
            *)
                echo "$filename is not a file to annotate"
                ;;
        esac
    done
else
    echo "No files found for processing."
fi


echo $ID_S3_TARGET_VALUE
echo $ID_S3_TARGET 
python s3_sync_target.py $ID_S3_TARGET "$TARGET_PATH"