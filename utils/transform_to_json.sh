SOURCE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/"
ARCHIVE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/Archive annotations/"

# Connect to MinIO bucket
export MC_HOST_s3=https://$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY@$AWS_S3_ENDPOINT


# Retrieve activity description to annotate and archive them
mc ls "$SOURCE_PATH" | grep -E '\.csv$|\.parquet$' | awk '{print $6}' | while read -r filename; do
    echo "Moving file: $filename"
    # Retrieves fiactivity description from s3
    mc cp --recursive "$SOURCE_PATH$filename" ./
    # Transform and save batch data to annotate
    python transform_to_json.py $filename
    # Move the treated batch data to archive
    mc mv "$SOURCE_PATH$filename" "$ARCHIVE_PATH"
done

