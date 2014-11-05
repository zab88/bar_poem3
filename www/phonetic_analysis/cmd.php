<?php
include_once('classes/Sound.php');
include_once('classes/SingleLetter.php');
include_once('classes/SingleSound.php');

$sound = new Sound();
$word = iconv("", "utf-8", $argv[1]);
$sound->setWord($argv[1]);
if (isset($argv[2])){
    $sound->set_accent($argv[2]);
}
$sound->makePhoneticAnalysis();

echo $sound->getTranscription();

if ($sound->letters){
    foreach ($sound->letters as $singleLetter) {
        echo '<p>';
        echo $singleLetter->letter;
        foreach($singleLetter->sounds as $singleSound){
            echo '[';
            echo $singleSound->getSpell() ;
            echo '] - ';
            echo $singleSound->getVerboseInfo(true);
            echo '</br>';
        }
        echo '</p>';
    }
}else{
    echo "AAAA";
}