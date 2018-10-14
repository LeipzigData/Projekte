<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 2015-02-18
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

$language = getLanguage();
// check ini file for translated verbs
$translation = getTranslation($language);
// start building website
echo pageHeader($translation["tabTitle"],$language);
echo pageNavigation($translation["label"], $translation["map"], 
		    $translation["aboutUs"], $translation["languageButton"], $language);
echo '<div class="container">'; 
echo pageTitle($translation["pageTitle"]);
($language == "en" ? include("about_en.html") : include("about_de.html"));
echo '</div>';
echo  pageFooter($translation["copyright"], $translation["copyrightdate"]);

?>