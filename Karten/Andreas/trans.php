<?php

/*

Script for reengineering the file jsp4.json into turtle format.  

To get this script running you have to link the easyrdf lib directory to this
directory. 

 */

require_once "lib/EasyRdf.php";

$graph = new EasyRdf_Graph('http://example.org/MeinGraph/');
$graph->parseFile('jsp4.json');
echo $graph->serialise('turtle');

?>