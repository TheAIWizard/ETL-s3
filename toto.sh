for file in $(mc ls "s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/" | awk '{print $5}')
do
    mc mv "s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/$file" "s3/nrandriamanana/Label Studio/Annotation APE 2024/Extract manuelle/Archive annotations/"
done
