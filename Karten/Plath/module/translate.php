<?php
/**
 * User: Immanuel Plath
 * Date: 05.12.14
 */

// output settings
//=========================
ini_set('default_charset', 'utf-8');

// base settings
//=========================

// Function: Get language from GET parameter
// param: none
// return: a valid existing language
// Add new languages here! 
//=========================
function getLanguage()
{
    $lang="de";
    $language = (empty($_GET["lang"]) ? "de" : $_GET["lang"]);
    switch ($language) {
        case "de": $lang = "de";  break;
        case "en": $lang = "en";  break;
        default: $lang = "de";
    }
    return $lang;
}

// Function: Get language from GET parameter
// param: none
// return: a valid existing language
// Add new languages here! 
//=========================
function addLanguageTag($link)
{
    $language=getLanguage();
    return "\"$link?lang=$language\"";
}

// Function
// function read .ini file with translate text for website
// param: wished language example "de" or "en" ...
// return: a array is returned which contain all data
//=========================
function getTranslation($language)
{
    $pathToTranslateDir = "../data/translation/";
    $fullpath           = $pathToTranslateDir . $language . ".ini";
    $translation        = parse_ini_file($fullpath);
    return $translation;
}

// echo getLanguage(); // for test

?>