#!/bin/bash
#set -x

SOURCE_PATH="s3/$S3_BUCKET/$S3_BUCKET_PREFIX_DEPOT_MANUEL"
ARCHIVE_PATH="s3/$S3_BUCKET/$S3_BUCKET_PREFIX_ARCHIVE_DEPOT_MANUEL"


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

                # Get export folder name for annotated data before creation
                NUMERO_LOT=$(python display_last_target_folder_id.py)
                # Copy in an other folder, tasks done in the current batch before creation of new LS project (avoid sync problem)
                mc cp --recursive "s3/$S3_BUCKET$S3_BUCKET_PREFIX_ANNOTATION_TARGET/in-progress/batch-$NUMERO_LOT/" "s3/$S3_BUCKET$S3_BUCKET_PREFIX_ANNOTATION_TARGET/completed/batch-$NUMERO_LOT"
                
                # Create or update/create label studio project
                python update_create_project.py

                # Get current export folder name for annotated data after creation
                NUMERO_LOT=$(python display_current_target_folder_id.py)
                echo "Folder to sync: batch-$NUMERO_LOT"

                # Get current project id 
                LABEL_STUDIO_PROJECT_ID=$(python display_last_pk.py)
                # Export as env variable
                export LABEL_STUDIO_PROJECT_ID=$LABEL_STUDIO_PROJECT_ID
                # Check current project id (according to label studio)
                echo CURRENT LABEL STUDIO ID PROJET: $LABEL_STUDIO_PROJECT_ID

                # Transform and save batch data to annotate
                python transform_to_json.py "$filename"

                # Give right path for export storage
                TARGET_PATH="$S3_BUCKET_PREFIX_ANNOTATION_TARGET/in-progress/batch-$NUMERO_LOT"
                echo "TARGET_PATH is set to: $TARGET_PATH"

                # Create target S3 
                python s3_create_target.py "$TARGET_PATH"
                # Export target path
                export TARGET_PATH=$TARGET_PATH

                # Sync export storage with s3
                python s3_sync_target.py $ID_S3_TARGET "$TARGET_PATH"

                # Move the treated batch data to the archive
                mc mv "$SOURCE_PATH$filename" "$ARCHIVE_PATH"
                
                ;;
            *)
                echo "$filename is not a file to annotate"
                ;;
        esac
    done
else
    echo "No files found for annotation"
fi

# Get current project id 
LABEL_STUDIO_PROJECT_ID=$(python display_last_pk.py)
# Export as env variable
export LABEL_STUDIO_PROJECT_ID=$LABEL_STUDIO_PROJECT_ID
# Check current project id (according to label studio)
echo CURRENT LABEL STUDIO ID PROJET: $LABEL_STUDIO_PROJECT_ID
# Get export folder name for path syncing to S3
NUMERO_LOT=$(python display_last_target_folder_id.py)
echo mc ls s3/$S3_BUCKET$S3_BUCKET_PREFIX_ANNOTATION_TARGET/in-progress
# Export folder path
TARGET_PATH="$S3_BUCKET_PREFIX_ANNOTATION_TARGET/completed/batch-$NUMERO_LOT"
# Check if previous batch is full and assign next target storage
if mc ls "s3/$S3_BUCKET$TARGET_PATH" | grep STANDARD; then
    echo "batch-$NUMERO_LOT est terminé --> Archivage du lot précédent --> Passage au lot suivant pour annotation"
    NUMERO_LOT=$(python display_current_target_folder_id.py)
else
    echo "batch-$NUMERO_LOT toujours en cours d'annotation"
    NUMERO_LOT=$(python display_last_target_folder_id.py)
fi
echo "Folder to sync: batch-$NUMERO_LOT"
# Give right path for export storage
TARGET_PATH="$S3_BUCKET_PREFIX_ANNOTATION_TARGET/in-progress/batch-$NUMERO_LOT"
# sync export storage with s3
python s3_sync_target.py $ID_S3_TARGET "$TARGET_PATH"

