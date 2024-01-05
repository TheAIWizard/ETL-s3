SOURCE_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/"
DESTINATION_PATH="s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/Archive annotations/"

mc ls "$SOURCE_PATH" | grep -E '\.csv$|\.parquet$' | awk '{print $6}' | while read -r filename; do
    echo "Moving file: $filename"
    # Uncomment the following line when you're ready to perform the actual move
    mc mv "$SOURCE_PATH$filename" "$DESTINATION_PATH"
done

# Move the other way
# mc ls "$DESTINATION_PATH" | grep -E '\.csv$|\.parquet$' | awk '{print $6}' | while read -r filename; do
#     echo "Moving file: $filename"
#     # Uncomment the following line when you're ready to perform the actual move
#     mc mv "$DESTINATION_PATH$filename" "$SOURCE_PATH"
# done