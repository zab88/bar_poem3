<?php

# check if data valid
if (!isset($_REQUEST['poem_body'])){
    exit( '{error:1}' );
}
$poem_body = $_REQUEST['poem_body'];

//insert into database
$link = mysqli_connect("localhost", "root", "", "bar_poem3") or die("Error " . mysqli_error($link));
mysqli_query($link, "INSERT INTO poems (poem_body) VALUES ('{$poem_body}')");
$last_id = mysqli_insert_id($link);


//call python


//read results


//send results
echo "oki_".$last_id;