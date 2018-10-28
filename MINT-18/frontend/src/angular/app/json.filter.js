angular
    .module("app.services")
    .filter("jsonFilter", function() {
        return function(input, filterObject) {
            if (input == undefined) {
                return [];
            }

            // Search Strings
            const searchString = function(entry) {
                let searchString = filterObject.searchString;
                // No String given
                if (searchString === "") {
                    return true;
                }
                // String in label?
                if (entry.name &&
                    entry.name.toLowerCase().indexOf(searchString.toLowerCase()) >= 0) {
                    return true;
                }
                return false;
            };

            // Search applied tags
            const searchTags = function(element) {
                if (filterObject.tags.length === 0) {
                    return true;
                }
                if (! element.tags) {
                    return false;
                }
                for (tagName of filterObject.tags) {
                    if (! element.tags.includes(tagName)) {
                        return false;
                    }
                }
                return true;
            };

            const searchHandicappedSuited = function(element) {
                if (element.accessibility == null) {
                    element.accessibility = 0;
                }
                return filterObject.accessibility <= element.accessibility;
            };

            return input.filter(searchString)
                .filter(searchTags)
                .filter(searchHandicappedSuited);
        };
    });
