<?php

$dir = 'C:\tmp\chm_test\2\3\texts\push17\vol03';

$files = scandir($dir);

$num_found = 0;
foreach ($files as $k=>$file_name){
    if ( in_array($file_name, array('y03-005-tt.htm'))){
        continue;
    }
    #do not include fairy-tails
    if ($file_name == 'y03-497-tt.htm'){
        exit;
    }
    if ( strpos($file_name, '-tt') > 0 ){
        echo $file_name."\n";
//        echo "<br />";

        $file_html = file_get_contents($dir.DIRECTORY_SEPARATOR.$file_name);
        if (strpos($file_html, 'name=author')){
            $body_start = strpos($file_html, '<BODY');
            $poem_html = substr($file_html, $body_start);
            $poem_html = iconv("cp1251", "utf-8", $poem_html);

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

            $pattern_year = "/#(\d{4})\./";
            preg_match($pattern_year, $poem_html, $matches);
//            print_r($matches);
            $year_extracted = $matches[1];

            #delete title
            $poem_html = preg_replace("#<a href(.*?)</a>([^\n]*?)[\n][\n][\n]#is", "", $poem_html);

            $poem_extracted = strip_tags($poem_html);
            $poem_extracted = str_replace("\n\n", "\n", $poem_extracted);
            $poem_extracted = str_replace("\n\n", "\n", $poem_extracted);
            $poem_extracted = str_replace("\n\n", "\n", $poem_extracted);

            print $year_extracted." -- year \n\n\n";
            print $name_extracted." -- name \n\n\n";
            print $poem_extracted."\n";
//            print $poem_html;
            print "================================\n";

            $num_found++;
        }
    }
//    if ($num_found > 15){
//        exit;
//    }
}