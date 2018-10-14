<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 11.02.2015
 *
 * The footer imports all Javascript stuff and provides the common footer part.
 */

?>
    <!-- Begin footer content -->
    <div class="footer">
      <div class="container">
        <p class="text-muted">&copy;<?php echo $translation["copyright"].' '.$translation["copyrightdate"]; ?> </p>
      </div>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>
    
    <!-- Custom JavaScript
    ================================================== -->
    <!-- Include Map JS -->
    <script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
    <!-- Custom JS Settings for Map -->
    <script src="js/custom-map.js"></script>
    <!-- Helper JS Functions -->
    <script src="js/helper.js"></script>
    
  </body>
</html>
