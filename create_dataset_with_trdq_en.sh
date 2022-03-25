dict=tools/dict
font=$1
background_path=$2
output_dir=`date +%s`

num=20000

python TextRecognitionDataGenerator/trdg/run.py -id $background_path \
    -ft $font \
    -fi \
    -na 2 \
    -b 3 \
    -t 32 \
    -l en \
    --output_dir en_out/$output_dir \
    -tc '#000000,#FFFFFF' \
    -c $num \
    -bl 0 \
    -w 2
mv en_out/$output_dir/labels.txt en_out/$output_dir.txt
sed -i -r 's#jpg #jpg\t#g' en_out/$output_dir.txt
sed -i -r 's#^#'`pwd`'/en_out/'$output_dir'/#g' en_out/$output_dir.txt
