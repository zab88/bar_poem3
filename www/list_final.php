<?php
header('Content-Type: text/html; charset=utf-8');
//insert into database
$link = mysqli_connect("localhost", "bar_poem3", "ACLQ7E7JcAwE9K3e", "bar_poem3") or die("Error " . mysqli_error($link));
mysqli_set_charset($link, "utf8");


//read results
$poems = array();
if (isset($_GET['year'])){
    $where = 'WHERE year='.intval($_GET['year']);
}else{
    $where = '';
}
$result = mysqli_query($link, "SELECT * FROM final_02 $where ORDER BY id");

echo "<table border='2'>";
echo '<tr>
    <td>tid</td>
    <td>id</td>
    <td>title</td>
    <td>year</td>
    <td>~lines</td>
    <td>lines num</td>
    <td>metric</td>
    <td>strofika</td>
    <td>outer id</td>
</tr>';
while($r = mysqli_fetch_array( $result )) {
    $poems[] = json_encode($r);
    echo "<tr>";
    $lines_diff = abs($r['lines_num'] - substr_count($r['poem_body'], "\n") );
    echo "<td valign='top'>".$r['tid']."</td>";
    echo "<td valign='top'>".$r['id']."</td>";
    echo "<td valign='top'>".$r['title']."</td>";
    echo "<td valign='top'>".$r['year']."</td>";
    echo "<td valign='top' ".($lines_diff>3?'style="color:red"':'').">" . substr_count($r['poem_body'], "\n") . "</td>";
    echo "<td valign='top'>".$r['lines_num']."</td>";
    echo "<td valign='top'>".$r['metric']."</td>";
    echo "<td valign='top'>".$r['strofika']."</td>";
    echo "<td valign='top'><a target='_blank' href='list_detail.php?outer_id=".$r['outer_id']."'>".$r['outer_id']."</td>";


    echo "</tr>";
}
echo "</table>";

//send results
//echo "oki_".$last_id;
//echo $res_json;