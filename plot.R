require(plyr)
exps = read.table("./data.txt", sep=',', header=T, stringsAsFactors=F)
data = by(exps, 1:nrow(exps), 
   function(row)
   {
     t = read.table(row$datafile, sep='\t', header=F, stringsAsFactors=F, fill=T)
     t = t[,c("V6", "V5")]
     colnames(t) <- c("atom", "value")
     t$value = abs(t$value)*2^(-row$NCproc)
     t$medium = row$medium
     t$resudue = sub("\\S+\\s(\\S+)", "\\1", t$atom)
     t$nucleus = sub("(\\S+)/\\S+\\s.+", "\\1", t$atom)
     return(t)     
   }
)
data=rbind.fill(data)


db = data.frame(atom=character(0))
for ( i in c("c_0", "c_1", "n_0", "n_1"))
{
  x = strsplit(i, "_")[[1]]
  t = read.table(paste0("./db",x[1],"/", x[2], ".txt"),
                 sep='\t', header=F, stringsAsFactors=F, fill=T)
  t = t[,c("V6", "V5")]
  colnames(t) <- c("atom", i)
  db = merge(x=db, by.x = "atom", y = t, by.y="atom", all=T)
}

m = data.frame(atom=character(0))
for ( i in c("c_0", "c_1", "n_0", "n_1"))
{
  x = strsplit(i, "_")[[1]]
  t = read.table(paste0("./m",x[1],"/", x[2], ".txt"),
                 sep='\t', header=F, stringsAsFactors=F, fill=T)
  t = t[,c("V6", "V5")]
  colnames(t) <- c("atom", i)
  m = merge(x=m, by.x = "atom", y = t, by.y="atom", all=T)
}
