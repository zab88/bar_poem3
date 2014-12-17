<?php
header('Content-Type: text/html; charset=utf-8');
//insert into database
$link = mysqli_connect("localhost", "bar_poem3", "ACLQ7E7JcAwE9K3e", "bar_poem3") or die("Error " . mysqli_error($link));
mysqli_set_charset($link, "utf8");


//read results
$poems = array();
$result = mysqli_query($link, "SELECT * FROM academ16 ");

echo "<table border='2'>";
echo '<tr>
    <td>id</td>
    <td>year</td>
    <td>title</td>
    <td>first line</td>
    <td>poem cut</td>
    <td>metr_id</td>
</tr>';
while($r = mysqli_fetch_array( $result )) {
    $poems[] = json_encode($r);
    echo "<tr>";

    echo "<td valign='top'>".$r['id']."</td>";
    echo "<td valign='top'>".$r['year']."</td>";
    echo "<td valign='top'><b>".$r['name']."</b></td>";
    echo "<td valign='top'>".$r['first_line']."</td>";
    echo "<td><pre>". mb_substr($r['body'], 0, 1500)."</pre></td>";
    echo "<td valign='top'>".$r['metr_id']."</td>";

    echo "</tr>";
}
echo "</table>";

//send results
//echo "oki_".$last_id;
//echo $res_json;