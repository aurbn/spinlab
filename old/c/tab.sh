for file in "$@"
do
     awk '{print $6,"\t",$4}' file > file.t1
done

for file in "$@"
do
    join 
