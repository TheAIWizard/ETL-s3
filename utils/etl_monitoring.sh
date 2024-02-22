#Set env variables
export DATA_FILE_PATH_LOCAL=data

# Retrieve recursively all annotation data "locally"
# mc cp --recursive --flatten s3/$S3_BUCKET/$PATH_ANNOTATION_RESULTS data
mc ls s3/$S3_BUCKET/$PATH_ANNOTATION_RESULTS | awk '{print "s3/'$S3_BUCKET'/'$PATH_ANNOTATION_RESULTS'/" $5}' | xargs -I {} mc cp --recursive {} ./$DATA_FILE_PATH_LOCAL


# Transform and save annotation data
python extract_test_data_monitoring.py $DATA_FILE_PATH_LOCAL $PATH_ANNOTATION_PREPROCESSED