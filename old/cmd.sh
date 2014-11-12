for i in $@ 
do 
    cat $i | awk '{if(NF==6){printf("%s-%s\t%i\n", $6, $5, $4<0 ? -1*$4:$4)};}' > $i.1 
done
for i in 
do
    join 0.txt.1 1.txt.1 > join.txt
done
rm *.1
