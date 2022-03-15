source_text=$1
dict=tools/dict
font=$2
background_path=$3
output_dir=`date +%s`

num=1000000

invalid_chars=$(python tools/font_check.py -d $dict -f $font)

shuf $source_text | head -n $num | python tools/replace_by_dict.py tools/replace | egrep -v $invalid_chars | python tools/limit_length.py > tmp_text.txt
c=`cat tmp_text.txt | wc -l`

trdg -id $background_path \
    -ft $font \
    -fi \
    -na 2 \
    -b 3 \
    -t 12 \
    --input_file ./tmp_text.txt \
    --output_dir out/$output_dir \
    -tc '#000000,#FFFFFF' \
    -c $c \
    -bl 0 \
    -w 25
mv out/$output_dir/labels.txt out/$output_dir.txt
sed -i -r 's#jpg #jpg\t#g' out/$output_dir.txt
sed -i -r 's#^#'`pwd`'/out/'$output_dir'/#g' out/$output_dir.txt
