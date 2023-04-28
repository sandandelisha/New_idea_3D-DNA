#!/usr/bin/perl
my $agp=shift;
open IN,$agp or die $!;
#Superscaffold_1	1	1219797	1	W	ctg053805_np5512	1004735	2224531	-
#Superscaffold_1	1219798	1220297	2	N	hic_gap	1	500	+
#Superscaffold_1	1220298	1339497	3	W	ctg082802_np5512	1	119200	+
#Superscaffold_1	1339498	1339997	4	N	hic_gap	1	500	+
#Superscaffold_1	1339998	1566670	5	W	ctg018104_np5512	1	226673	-
my $n=0;
while(<IN>){
	chomp;
	my @f=split;
	if($f[4] =~/W/){
		my $line=join("\t",@f),"\n";
		$f[0]=~s/Scaffold_//;
		my $end=$f[7]-$f[6]+1;
		print "new_ctg.$f[0].$n\t1\t$end\t1\tW\t$f[5]\t$f[6]\t$f[7]\t$f[8]\n";
		print STDERR "new.contig.$f[0].$n\t$line\n";
		$n++;
	}
}
