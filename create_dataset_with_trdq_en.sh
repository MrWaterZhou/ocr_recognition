dict=tools/dict
font=$1
background_path=$2
output_dir=`date +%s`

num=10000

trdg -id $background_path \
    -ft $font \
    -fi \
    -na 2 \
    -b 3 \
    -t 32 \
    -l en \
    --output_dir out/$output_dir \
    -tc '#000000,#FFFFFF' \
    -c $num \
    -bl 0 \
    -w 1
mv out/$output_dir/labels.txt out/$output_dir.txt
sed -i -r 's#jpg #jpg\t#g' out/$output_dir.txt
sed -i -r 's#^#'`pwd`'/out/'$output_dir'/#g' out/$output_dir.txt
