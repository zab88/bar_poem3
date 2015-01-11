<?php
header('Content-Type: text/html; charset=utf-8');
//insert into database
$link = mysqli_connect("localhost", "bar_poem3", "ACLQ7E7JcAwE9K3e", "bar_poem3") or die("Error " . mysqli_error($link));
mysqli_set_charset($link, "utf8");


//read results
$poems = array();
$result = mysqli_query($link, "SELECT * FROM academ16 WHERE id=".intval($_REQUEST['outer_id']));

while($r = mysqli_fetch_array( $result )) {
    echo "<h3>".$r['name']."</h3>";
    echo "<pre>".$r['body']."</pre>";
}