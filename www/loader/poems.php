<?php
set_time_limit(100);
// Create connection
$conn = new mysqli('localhost', 'root', '', 'bar_poem3');

#$dir = 'C:\tmp\chm_test\2\3\texts\push17\vol01';
#$dir = 'C:\tmp\chm_test\2\3\texts\push17\vol02';
#$dir = 'C:\tmp\chm_test\2\3\texts\push17\vol03';
$dir = 'C:\tmp\chm_test\poems_extracted';

$files = scandir($dir);

$num_found = 0;
foreach ($files as $k=>$file_name){
    #for test
//    if ('y21-247-tt.htm' != $file_name){
//        continue;
//    }

//    if ( in_array($file_name, array('y03-005-tt.htm', 'y21-005-tt.htm'))){
//        continue;
//    }
//    #do not include fairy-tails
//    if ($file_name == 'y03-497-tt.htm' || $file_html == 'y21-487-tt.htm'){
//        exit;
//    }
    if ( strpos($file_name, '-tt') > 0 ){
//        echo $file_name."\n";
//        echo "<br />";

        $file_html = file_get_contents($dir.DIRECTORY_SEPARATOR.$file_name);
        $file_html = iconv("cp1251", "utf-8", $file_html);
        if (strpos($file_html, "name=author content='Пушкин А. С.'")){
            //try get titles
            preg_match_all("#<meta name=title content=\'([^\']+)\'>#i", $file_html, $matches);
            $titles = $matches[1];
            if ( count($titles) < 2 ){
                //check for having ...
                if (strpos($titles[0], '..') !== false){
                    $titles[1] = $titles[0];
                }else{
                    continue;
                }
//                continue;
//                var_dump($titles);
            }
            #var_dump($matches);die;

            $body_start = strpos($file_html, '<BODY');
            $poem_html = substr($file_html, $body_start);
            #$poem_html = iconv("cp1251", "utf-8", $poem_html);

            $poem_html = str_replace('&lt;', '', $poem_html);
            $poem_html = str_replace('&gt;', '', $poem_html);

            #deleting line numbers
            $poem_html = preg_replace("#<span class=verseno(.*?)</span>#is", "", $poem_html);
            $poem_html = preg_replace("#<span class=page(.*?)</span>#is", "", $poem_html);

            $poem_html = strip_tags($poem_html, '<a>');


            #getting names and year
            $pattern_name = "/<a [^>]*>(.*?)<\/a>/";
            preg_match($pattern_name, $poem_html, $matches);
//            print_r($matches);
            $name_extracted = $matches[1];
            $name_extracted = str_replace(
                array("&bdquo;", "&ldquo;", "&#x300;"),
                array('`', '`', ''), $name_extracted
            );

            $pattern_year = "/#(\d{4})\./";
            preg_match($pattern_year, $poem_html, $matches);
//            print_r($matches);
            $year_extracted = $matches[1];

            #delete title
            #print $poem_html;
            $poem_html_test = preg_replace("#<a href(.*?)</a>([^\n]*?)[\n][\n][\n]#is", "", $poem_html);
            if (strlen($poem_html_test) < 20){
                $poem_html = preg_replace('#<a(.*?)>(.*?)</a>#is', "", $poem_html);
            }else{
                $poem_html = $poem_html_test;
            }


            $poem_extracted = strip_tags($poem_html);
            $poem_extracted = str_replace("\n\n", "\n", $poem_extracted);
            $poem_extracted = str_replace("\n\n", "\n", $poem_extracted);
            $poem_extracted = str_replace("\n\n", "\n", $poem_extracted);
            #i do not know why, but next line does not work at all :(
            #$poem_extracted = htmlspecialchars_decode($poem_extracted);
            $poem_extracted = str_replace("&nbsp;", " ", $poem_extracted);
            $poem_extracted = str_replace(
                array("&bdquo;", "&ldquo;", "&#x300;"),
                array('`', '`', ''), $poem_extracted
            );
            $poem_extracted = trim($poem_extracted);
            $poem_extracted = addslashes($poem_extracted);

            #$first_line = get_first_line($poem_extracted);
            $first_line = $titles[1];
            $name_extracted = $titles[0];

//            if (mb_strlen( trim($poem_extracted)) < 20){
//                echo 'AAAAAA';
//            }
            print $file_name . " -- file_name\n\n\n";
            print $year_extracted." -- year \n\n\n";
            print $name_extracted." -- name \n\n\n";
            print $titles[0]." -- title \n\n\n";
            print $titles[1]." -- first line \n\n\n";
            print $poem_extracted."\n";
//            print $poem_html;
            print "================================\n";

            $num_found++;

            //DB
            $sql = "INSERT INTO academ16 (year, `name`, first_line, `body`)
                  VALUES ('{$year_extracted}', '{$name_extracted}', '{$first_line}', '{$poem_extracted}')";
            $conn->query($sql);
        }
    }
//    if ($num_found > 15){
//        exit;
//    }
}

echo '>>>>'.$num_found;

function get_first_line($tt){
    $lines = explode("\n", $tt);
    foreach ($lines as $line) {
        if (strlen($line)>4){
            return $line;
        }
    }
    return '';
}