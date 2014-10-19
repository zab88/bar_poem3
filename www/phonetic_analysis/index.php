<!DOCTYPE html>
<html>
<head>
    <title>Фонетический разбор онлайн</title>
    <meta charset="UTF-8">
</head>
<body>
<h1>Фонетический разбор слова</h1>
<form action="" method="POST">
    <input type="text" name="word" placeholder="введите слово для разбора" style="width: 250px;" />
</form>
<?php

if (isset($_POST['word'])){
    include_once('classes/Sound.php');
    include_once('classes/SingleLetter.php');
    include_once('classes/SingleSound.php');

    $sound = new Sound();
    $sound->setWord($_POST['word']);
    $sound->makePhoneticAnalysis();

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
    }
}
?>
</body>
</html>