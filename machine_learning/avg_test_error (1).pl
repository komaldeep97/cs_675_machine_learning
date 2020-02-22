#!/usr/bin/perl

$mean = 0;
$data = shift;
#$dir=$data;
$dir="ionosphere/$data";

$mean = 0;
for(my $i=0; $i<10; $i++){
  system("python3 assignment_9_randomprojections.py $dir/$data.data $dir/$data.trainlabels.$i > nm_out.$data");
  $err[$i] = `perl error.pl $dir/$data.labels nm_out.$data`;
  chomp $err[$i];
  print "$err[$i]\n";
  $mean += $err[$i];
  #print "$mean\n";
}
$mean /= 10;
$sd = 0;
for(my $i=0; $i<1; $i++){
  $sd += ($err[$i]-$mean)**2;
}
$sd /= 10;
$sd = sqrt($sd);
print "Least Squares adaptive eta error = $mean% ($sd)\n";

