<?php

# check if data valid
if (!isset($_REQUEST['poem_body'])){
    exit( '{error:1}' );
}
error_reporting(E_ALL);
ini_set('display_errors', 1);
$poem_body = $_REQUEST['poem_body'];

//insert into database
$link = mysqli_connect("localhost", "bar_poem3", "ACLQ7E7JcAwE9K3e", "bar_poem3") or die("Error " . mysqli_error($link));
mysqli_set_charset($link, "utf8");
mysqli_query($link, "INSERT INTO poems (poem_body) VALUES ('{$poem_body}')");
$last_id = mysqli_insert_id($link);


//call python
$python_script = dirname(__FILE__).'/../www.py '.$last_id;
shell_exec('python '.$python_script);

//read results
$result = mysqli_query($link, "SELECT * FROM poems_result WHERE poem_id=".$last_id);
while($r = mysqli_fetch_array( $result )) {
    $res_json = json_encode($r);
}

//send results
//echo "oki_".$last_id;
echo $res_json;