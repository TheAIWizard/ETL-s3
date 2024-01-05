SOURCE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/"
ARCHIVE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/Archive annotations/"

# Transform and save batch data to annotate
python transform_to_json.py $SOURCE_PATH

# Retrieve activity description to annotate and archive them
mc ls "$SOURCE_PATH" | grep -E '\.csv$|\.parquet$' | awk '{print $6}' | while read -r filename; do
    echo "Moving file: $filename"
    # Uncomment the following line when you're ready to perform the actual move
    mc mv "$SOURCE_PATH$filename" "$ARCHIVE_PATH"
done

