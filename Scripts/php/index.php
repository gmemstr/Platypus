<?php

$fh = fopen('/proc/meminfo', 'r');
  $mem = 0;
  while ($line = fgets($fh)) {
    $pieces = array();
    if (preg_match('/^MemTotal:\s+(\d+)\skB$/', $line, $pieces)) {
      $memtotal = $pieces[1];
    }
    if (preg_match('/^MemFree:\s+(\d+)\skB$/', $line, $pieces)) {
      $memfree = $pieces[1];
    }
    if (preg_match('/^Cached:\s+(\d+)\skB$/', $line, $pieces)) {
      $memcache = $pieces[1];
      break;
    }
  }
fclose($fh);

$stat1 = file('/proc/stat');
sleep(1);
$stat2 = file('/proc/stat');
$info1 = explode(" ", preg_replace("!cpu +!", "", $stat1[0]));
$info2 = explode(" ", preg_replace("!cpu +!", "", $stat2[0]));
$dif = array();
$dif['user'] = $info2[0] - $info1[0];
$dif['nice'] = $info2[1] - $info1[1];
$dif['sys'] = $info2[2] - $info1[2];
$dif['idle'] = $info2[3] - $info1[3];
$total = array_sum($dif);
$cpu = array();
foreach($dif as $x=>$y) $cpu[$x] = round($y / $total * 100, 1);
$array['cpu'] = round($cpu['user']);

$memmath = $memcache + $memfree;
$memmath2 = $memmath / $memtotal * 100;
$memory = round($memmath2);

$array['memory'] = $memory;

$hddtotal = disk_total_space("/");
$hddfree = disk_free_space("/");
$hddmath = $hddfree / $hddtotal * 100;
$hdd = round(100 - $hddmath);

$array['hdd'] = $hdd;

// RETURNS
// USED CPU
// USED MEMORY
// USED HDD
// IN PERCENTAGES
// YA NUMPTY

echo json_encode($array);
?>