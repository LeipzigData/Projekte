<?php
/**
 * User: Immanuel Plath
 * Date: 05.12.14
 */

// load app settings
//=========================
include_once "../config/config.php";

// debug settings
//=========================
if ($settings["debug"] == "1") {
    error_reporting(E_ALL);
} else {
    error_reporting(0);
}

// include section
//=========================
include_once "../module/searching.php";

// ouput settings
//=========================
ini_set('default_charset', 'utf-8');

// Local Function: Return json encoded result of searchByUri 
// param: search string
// return: JSON object
//=========================
function response($searchKey)
{
    // Change Content Header
    header('Content-Type: application/json;charset=utf-8');
    return json_encode(searchByUri($searchKey));
}

// print search result as JSON object to the user
if (!empty($_GET["search"])) { echo response($_GET["search"]); }

// echo response("nextbike"); // to test it

?>



