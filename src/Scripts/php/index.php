<?php
// PHP index file for Platypus-compatibility.
// This script is for Linux only, rename index.php.windows
// to index.php for the Windows script
// Credit for script: https://stackoverflow.com/questions/22949295/how-do-you-get-server-cpu-usage-and-ram-usage-with-php

function get_server_memory_usage(){

    $free = shell_exec('free');
    $free = (string)trim($free);
    $free_arr = explode("\n", $free);
    $mem = explode(" ", $free_arr[1]);
    $mem = array_filter($mem);
    $mem = array_merge($mem);
    $memory_usage = $mem[2]/$mem[1]*100;

    return $memory_usage;
}

function get_server_cpu_usage(){

    $load = sys_getloadavg();
    return $load[0];

}

function stats(){
    $s = new stdClass();
    // $s->cpu = get_server_cpu_usage();
    $s->memory = get_server_memory_usage();
    $s->disk = disk_free_space('/') / disk_total_space('/');

    return $s;
}

echo json_encode(stats());

?>