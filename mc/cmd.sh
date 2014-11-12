for i in $@ 
do 
    cat $i | awk '{if(NF==7){printf("%s-%s\t%i\n", $7, $6, $5<0 ? -1*$5:$5)};}' > $i.1 
done
join 0.txt.1 1.txt.1 > join.txt
grep -f list.txt > table.txt
rm *.1
