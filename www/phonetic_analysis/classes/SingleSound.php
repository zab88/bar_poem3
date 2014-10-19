<?php

class SingleSound {
    //согласный, гласный
    //твердый, мягкий
    //звонкий, глухой
    //парный, непарный
    //сонорный,

    public $letter;
    public $spell = '';
    public $is_vowel = null;
    public $is_soft = null;
    public $is_paired = null;
    public $is_clunk = null;
    public $is_sonorous = null;
    public $letter_num = null; //only if created from letters

    function __construct($letter, $letter_num=0){
        $this->letter = $letter;
        $this->letter_num = $letter_num;
        if (in_array($letter, Sound::$vowels_sound)){
            $this->is_vowel = true;
        }else{
            $this->is_vowel = false;
        }

        if ($letter != 'ь' && $letter != 'ъ'){
            $this->spell = $letter;
        }
    }

    function setSoftness(){
        $this->is_soft = true;
//        if ( mb_strpos($this->spell, "'", 0, 'utf-8') === false){
//            $this->spell .= "'";
//        }
    }

    function setClunkPaired($spell_letter){
        $this->is_clunk = true;
        $this->spell = $spell_letter;
    }

    function setVoicedPaired($spell_letter){
        $this->is_clunk = false;
        $this->spell = $spell_letter;
    }

    //draw ' if soft
    public function getSpell(){
        return ($this->is_soft) ? $this->spell."'" : $this->spell;
    }

    public function setSpell($newSpell){
        $this->spell = $newSpell;
    }

    public function getVerboseInfo($inline = false){
        $info = array();
        if (!$this->spell){
            $info = array('звука нет');
            return ($inline) ? implode(", ", $info) : $info;
        }

        //consonant vs verbose
        if (in_array($this->spell, Sound::$consonants_sound)){
            $info[] = 'согласный';
        }else if (in_array($this->spell, Sound::$vowels_sound)){
            $info[] = 'гласный';
        }

        //softness
        if (in_array($this->spell, Sound::$consonants_sound) && $this->is_soft){
            $info[] = 'мягкий';
        }elseif(in_array($this->spell, Sound::$consonants_sound)){
            $info[] = 'твердый';
        }

        //paired
        if (in_array($this->letter, SingleLetter::$voiced_paired) || in_array($this->letter, SingleLetter::$clunk_paired)){
            $info[] = 'парный';
        }

        //clunk
        if (in_array($this->letter, SingleLetter::$voiced_paired)){
            $info[] = 'звонкий';
        }elseif(in_array($this->letter, SingleLetter::$clunk_paired)){
            $info[] = 'глухой';
        }

        //sonorous
        if (in_array($this->letter, Sound::$sonorous)){
            $info[] = 'сонорный';
        }

        return ($inline) ? implode(", ", $info) : $info;
    }
}