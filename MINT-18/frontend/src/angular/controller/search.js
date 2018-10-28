angular
    .module("app")
    .controller("SearchController",
        function($scope,
            $routeParams,
            JsonData,
            JsonConfig,
            $timeout,
            $templateRequest,
            $compile,
            $filter,
            localStorageService) {

            // Reset filter function
            $scope.resetFilter = () => $scope.option = {
                tags: [],
                searchString: "",
                accessibility: 0
            };

            $scope.toggleTag = (tag) => {
                let index = $scope.option.tags.findIndex(
                    el => el == tag.name);
                if (index >= 0) {
                    $scope.option.tags.splice(index, 1);
                } else {
                    $scope.option.tags.push(tag.name);
                }
            };

            $scope.loadMap = () => {
                if ($scope.map != null) {
                    return;
                }
                $scope.map = L.map('map-all').setView([51.505, -0.09], 13);
                // Setup map
                L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    maxZoom: 18,
                    id: 'mapbox.streets',
                    accessToken: 'pk.eyJ1IjoibWVnYW1hbm1hbHRlIiwiYSI6ImNqbDR5bG1rOTFpc2wzdnF5eTJ0dnhtemsifQ.RCMTLOjQri0YrwcqeDXqeA'
                }).addTo($scope.map);
                // Update all markers
                $scope.updateMarkers();
            };

            let updateTagCount = () => {
                $scope.tagCount = {};
                $scope.filteredData.forEach(entry => {
                    if (! entry.tags) {
                        return;
                    }
                    entry.tags.forEach(tag => {
                        if (!$scope.tagCount[tag]) {
                            $scope.tagCount[tag] = 1;
                        } else {
                            $scope.tagCount[tag] += 1;
                        }
                    });
                });
            };

            // Handle tab selection
            $scope.select = function(which) {
                // Prevent bad map loading
                if (which === 'map' && $scope.filteredData.length === 0) {
                    return;
                }
                $scope.selected = which;

                if (which === "map") {
                    $scope.loadMap();
                    // Timeout to fix false loading
                    // TODO: Improve
                    $timeout(() => {
                        if ($scope.markerGroup.getLayers().length != 0) {
                            $scope.map.invalidateSize();
                            $scope.map.fitBounds($scope.markerGroup.getBounds().pad(0.3));
                        }
                    }, 300);
                }
            };

            // Default is list view
            $scope.selected = 'list';

            // Update map markers
            $scope.updateMarkers = function() {
                $scope.markers = [];
                if ($scope.filteredData == null) {
                    return;
                }
                // Add all entries that have coordinates to the list of markers
                for (let entry of $scope.filteredData) {
                    let validLocation =
                        entry['gps'] != null &&
                        entry['gps']['lat'] != null &&
                        entry['gps']['long'] != null;
                    if (validLocation) {
                        $scope.markers.push(entry);
                    }
                }
                // Delete old markers
                if ($scope.markerGroup != null &&
                    $scope.map != null) {
                    $scope.map.removeLayer($scope.markerGroup);
                }
                // Create a layer group for all markers
                $scope.markerGroup = L.markerClusterGroup({
                    zoomToBoundsOnClick: false
                });
                // Actually create and add the markers to the markergroup
                for (let marker of $scope.markers) {
                    createMarker(marker).addTo($scope.markerGroup);
                }
                // Add event listener for clicks on clusters
                $scope.markerGroup.on('clusterclick', (a) => {
                    $scope.map.fitBounds(a.layer.getBounds().pad(0.1));
                });
                // Add the markergroup to the map
                if ($scope.map != null) {
                    $scope.markerGroup.addTo($scope.map);
                }
            };

            // Create a marker from the given entry
            let createMarker = entry => {
                let pos = [
                    entry.gps.lat,
                    entry.gps.long
                ];
                let m = L.marker(pos);
                let id = encodeURIComponent(entry.id);
                let img = "";
                if (entry.imgs && entry.imgs.length > 0) {
                    img = entry.imgs[0];
                }
                let template = `
<div class="card" style="width: 14rem;">
  <img class="card-img-top" src="${img}" alt="" onerror="brokenImage(this)">
  <div class="card-body">
    <h5 class="card-title">${entry.name}</h5>
  </div>
  <div class="card-footer">
    <a class="btn btn-block btn-primary btn-sm text-light" href="#!/e/${id}">Mehr Infos</a>
  </div>
</div>`;
                let popup = L.popup({
                        closeButton: false
                    })
                    .setContent(template);
                m.bindPopup(popup);
                m.update();
                return m;
            };

            $scope.updateFilter = function() {
                $scope.filteredData = $filter('jsonFilter')($scope.data, $scope.option);
                $scope.updateMarkers();
                updateTagCount();
            };

            JsonData.getData(function(data) {
                $scope.data = data;
                $scope.updateFilter();
            });

            JsonConfig.getConfig(function(config) {
                $scope.config = config;
            });

            $scope.$watchCollection("option.tags", function(newValue, oldValue) {
                $scope.updateFilter();
                localStorageService.set("optionSave", $scope.option);
            });
            $scope.$watchCollection("option", function(newValue, oldValue) {
                $scope.updateFilter();
                localStorageService.set("optionSave", $scope.option);
            });

            $scope.resetFilter();
            // Initialize search options
            $scope.option = localStorageService.get("optionSave");
            if (($scope.option == null)) {
                $scope.resetFilter();
            }
        });
