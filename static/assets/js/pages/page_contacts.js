var ContactPage = function () {

    return {
        
        //Basic Map
        initMap: function() {
            var map;
            $(document).ready(function(){
              map = new GMaps({
                div: '#map',
                scrollwheel: true,
                lat: 59.858534,
                lng: 17.646085
              });
              
              var marker = map.addMarker({
                lat: 59.858534,
                lng: 17.646085,
               });
            });
        },

        init_map_loc: function(lat, lon) {
            var map;
            $(document).ready(function(){
              map = new GMaps({
                div: '#map',
                scrollwheel: true,
                lat: lat,
                lng: lon,
                zoom: 7
              });
              
              var marker = map.addMarker({
                lat: lat,
                lng: lon,
               });
            });
        },

        //Panorama Map
        initPanorama: function () {
            var panorama;
            $(document).ready(function(){
              panorama = GMaps.createPanorama({
                el: '#panorama',
                lat : 59.858534,
                lng : 17.646085
              });
            });
        }        

    };
}();