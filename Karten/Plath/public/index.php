<?php
/**
 * User: Immanuel Plath
 * Date: 05.12.14
 */

// include section
//=========================
include_once "../config/config.php";
include_once "../module/translate.php";
include_once "../module/html.php";
include_once "../module/getCategories.php";

// ouput settings
//=========================
ini_set('default_charset', 'utf-8');

// base settings
//=========================

// Function
// function return a full website contains map
// param: wished language example "de" or "en" ...
// return: a array is returned which contain all data
//=========================
function buildWebpage()
{
    $language = getLanguage();
    $translation = getTranslation($language);
    // start building website
    $webpage = "";
    $webpage = pageHeader($translation["tabTitle"],$language);
    $webpage.= pageNavigation($translation["label"], $translation["map"], 
	       $translation["aboutUs"], $translation["languageButton"], $language);
    $webpage.='<div class="container">'; 
    $webpage.= pageTitle($translation["pageTitle"]);
    $webpage.= pageMap($translation["placeDescription"], $translation["opening"], 
               $translation["contact"], $translation["properties"], $translation["chooseEntry"], $language);
    $webpage.= getCategories($language, $translation["allCategories"], $translation["noCategorie"]);
    $webpage.= displaySearchResponse();
    $webpage.='</div>';
    $webpage.= pageFooter($translation["copyright"], $translation["copyrightdate"]);
    return $webpage;
}

echo buildWebpage();

?>