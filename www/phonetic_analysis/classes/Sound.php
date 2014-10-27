<?php
//http://school-assistant.ru/?predmet=russian&theme=glasnie_i_soglasnie
//http://www.licey.net/russian/phonetics/1_5
class Sound {
    //VOWELS
    public static $vowels_sound = array('и', 'ы', 'у', 'э', 'о', 'а');
    public static $vowels_special = array("я", "е", "ё", "ю");
    public static $consonants_sound = array('б', 'в', 'г', 'д', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ж', 'ш', 'ц', 'ч', 'й');
    #public static $consonants_paired = array('и', 'ы', 'у', 'э', 'о', 'а');
    #public static $consonants__not_paired = array('и', 'ы', 'у', 'э', 'о', 'а');
    public static $sonorous = array('р', 'л', 'м', 'н', 'й');
    //features:
    //согласный, гласный
    //твердый, мягкий
    //звонкий, глухой
    //парный, непарный
    //сонорный, сонорные это вроде (Р, Р’, Л, Л’, Н, Н’, М, М’, Й)
    public $transcription = '';
    public $letters = array();

    public function setWord($word){
        $word = mb_strtolower($word, 'utf-8');
        $word_length = mb_strlen($word, 'utf-8');
        for ($i=0;$i<$word_length;$i++){
            $letter = mb_substr($word, $i, 1, 'utf-8');

//            $i > 0 ? $prevLetter = mb_substr($word, $i-1, 1, 'utf-8') : $prevLetter = null;
//            $word_length-1 > $i ? $nextLetter = mb_substr($word, $i+1, 1, 'utf-8') : $nextLetter = null;

            $this->letters[] = new SingleLetter($letter);

        }

        foreach ($this->letters as $k=>$letter) {
            if ($k>0){
                $letter->setPrevLetter( $this->letters[$k-1] );
            }
            if ($word_length-1 > $k){
                $letter->setNextLetter( $this->letters[$k+1] );
            }
        }

    }

    public function set_accent($accent){

    }

    public function makePhoneticAnalysis(){
        foreach ($this->letters as $letter) {
            $letter->setDefaultSounds();
        }
    }

    public function getTranscription(){
        foreach ($this->letters as $letter) {
            foreach($letter->sounds as $singleSound){
                $this->transcription .= $singleSound->getSpell();
            }
        }
        return $this->transcription;
    }

    public function countSoundFeatures(){
        $TOTAL_SOUNDS = 0;
        $vowels = 0;
        $consonants = 0;
        $soft = 0;
        $hard = 0;
        $clunk = 0;
        $voiced = 0;
        $paired = 0;
        $non_paired = 0;
        $sonorous = 0;
        foreach ($this->letters as $letter) {
            foreach ($letter->sounds as $sound) {
                $info = $sound->getVerboseInfo();
                foreach($info as $el){
                    switch ($el){
                        case 'гласный': $vowels++;break;
                        case 'согласный': $consonants++;break;
                        case 'твердый': $hard++;break;
                        case 'мягкий': $soft++;break;
                        case 'глухой': $clunk++;break;
                        case 'звонкий': $voiced++;break;
                        case 'парный': $paired++;break;
                        case 'сонорный': $sonorous++;break;
                        case 'звука нет' : $TOTAL_SOUNDS--; break;
                        default : echo 'Err'.$el;
                    }
                }
                $TOTAL_SOUNDS++;
            }
        }
        return array(
            'vowels' => $vowels,
            'consonants' => $consonants,
            'soft' => $soft,
            'hard' => $hard,
            'clunk' => $clunk,
            'voiced' => $voiced,
            'paired' => $paired,
            'sonorous' => $sonorous,
            'total_sounds' => $TOTAL_SOUNDS
        );
    }

    /*
    public function generateTranscription($word){
        $word = strtolower($word);
        //every letter in word has some information

        for ($i=0;$i<strlen($word);$i++){
            $letter = substr($word, $i, 1);
            //some letters can create two sounds
            if ( ! in_array($letter, self::$vowels_special) ){
                $this->transcription[ ] = new SingleSound( $letter, $i );
            }else{
                ($i>0) ? $letter_before = substr($word, ($i-1), 1) : $letter_before = '';
                //two letters
                if ($i > 0 && !in_array($letter_before, self::$consonants_sound) ){
                    $this->transcription[ ] = new SingleSound( 'й', $i );
                    switch($letter){
                        case "я": $this->transcription[] = new SingleSound("а", $i); break;
                        case "е": $this->transcription[] = new SingleSound("э", $i); break;
                        case "ё": $this->transcription[] = new SingleSound("о", $i); break;
                        case "ю": $this->transcription[] = new SingleSound("у", $i); break;
                    }
                }
            }
        }

        //я, е, ё, ю add softness if previous letter is consonant
        foreach ($this->transcription as $k=>$sound) {
            $next_sound = self::getNextSound($k);
//            if (!$sound->is_vowel && $next_sound->){
//
//            }
        }

        //ь, ъ - mean no sound
        foreach ($this->transcription as $k=>$sound) {
        }

    }

    public static function getNextSound($k){
        if ( count(self::$transcription) >= $k )
        return self::$transcription[$k+1];
    }

    public static function getPrevSound($k){
        if ($k === 0) return null;
        return self::$transcription[$k-1];
    }
    */
}