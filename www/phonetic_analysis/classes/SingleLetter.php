<?php

class SingleLetter {
    public $letter = '';
    public $prevLetter = null;
    public $nextLetter = null;
    public $sounds = array();

    public static $vowels_sound = array('и', 'ы', 'у', 'э', 'о', 'а');
    public static $vowels_special = array("я", "е", "ё", "ю");
    public static $consonants_sound = array('б', 'в', 'г', 'д', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ж', 'ш', 'ц', 'ч', 'й');

    public static $voiced_paired = array('б', 'в', 'г', 'д', 'ж', 'з');
    public static $clunk_paired =  array('п', 'ф', 'к', 'т', 'ш', 'с');

    public function __construct($letter){
        $this->letter = $letter;
    }

    public function setPrevLetter(&$prevLetter){
        $this->prevLetter = $prevLetter;
    }

    public function setNextLetter(&$nextLetter){
        $this->nextLetter = $nextLetter;
    }

    public function setDefaultSounds(){
        //1: let's manage letters, that can produce double sounds
        if ( ! in_array($this->letter, self::$vowels_special) ){
            $this->sounds[] = new SingleSound( $this->letter );
        }else{
            //if previous letter not consonant
            if ($this->prevLetter && !in_array($this->prevLetter->letter, self::$consonants_sound) ){
                $this->sounds[] = new SingleSound( 'й');
                switch($this->letter){
                    case "я": $this->sounds[] = new SingleSound("а"); break;
                    case "е": $this->sounds[] = new SingleSound("э"); break;
                    case "ё": $this->sounds[] = new SingleSound("о"); break;
                    case "ю": $this->sounds[] = new SingleSound("у"); break;
                }
            }else{
                switch($this->letter){
                    case "я": $this->sounds[] = new SingleSound("а"); break;
                    case "е": $this->sounds[] = new SingleSound("э"); break;
                    case "ё": $this->sounds[] = new SingleSound("о"); break;
                    case "ю": $this->sounds[] = new SingleSound("у"); break;
                }
                //and prev consonant now soft
                if (count($this->prevLetter->sounds) > 0){
                    $this->prevLetter->sounds[0]->setSoftness();
                }
            }
        }

        //2: soft sign after consonant make consonant soft
        if ( $this->nextLetter && $this->nextLetter->letter === 'ь' && in_array($this->letter, self::$consonants_sound) ){
            $this->sounds[0]->setSoftness();
        }

        //3: voiced in the end of word or before clunk consonant becomes clunk
        if ( in_array($this->letter, self::$voiced_paired) ){
            if ( is_null($this->nextLetter) || ($this->nextLetter && in_array($this->nextLetter->letter, self::$clunk_paired)) ){
                $key = array_search($this->letter, self::$voiced_paired);
                $this->sounds[0]->setClunkPaired( self::$clunk_paired[$key] );
            }
        }

        //4:жи ши ци
        if ( $this->letter == 'и' && in_array($this->prevLetter->letter, array('ж', 'ш', 'ц')) ){
            $this->sounds[0]->setSpell('ы');
        }

        //5: non pronounce consonants //http://orthographia.ru/orfografia.php?sid=45
        if ($this->prevLetter && $this->nextLetter){
            $non_pc = array('стн', 'стл', 'здн', 'рдц', 'рдч', 'стц', 'здц', 'ндц');
            foreach ($non_pc as $non_p) {
                $combo = $this->prevLetter->letter.$this->letter.$this->nextLetter->letter;
                #$non_letter = mb_substr($non_p, 1, 1, 'utf-8');
                if ($combo == $non_p){
                    $this->sounds[0]->setSpell('');
                }
            }
            $non_pc_2 = array('нтск', 'ндск', 'нтств', 'стск');
        }

        //6: озвончение, косьба [з], молотьба [д] Глухой согласный перед звонким согласным ( кроме л, м, н, р, в, й ) заменяется парным ему звонким
        // http://bugaga.net.ru/ege/rus/theory/?n=1
        if ($this->nextLetter && in_array($this->letter, array('п', 'к', 'т', 'ш', 'с'))) {
            $nextLetter = $this->nextLetter->letter;
            if ($nextLetter == 'ь' && $this->nextLetter->nextLetter){
                $nextLetter = $this->nextLetter->nextLetter->letter;
            }
            if ( in_array($nextLetter, array('б', 'г', 'д', 'ж', 'з'))){
                $key = array_search($this->letter, self::$clunk_paired);
                $this->sounds[0]->setVoicedPaired( self::$voiced_paired[$key] );
            }
        }


    }

    public function getSound(){

    }

}