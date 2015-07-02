/**
 * google map widget used in admin
 */
(function (gmap, d$, undefined) {

    gmap.has = function (id) {
        return id && d$('#' + id).length;
    };

    gmap.updateMapZoom = function (map, zoom_id) {
        if (!d$('#' + zoom_id).val())
            return;
        map.setZoom(parseInt(d$('#' + zoom_id).val()));
    };

    gmap.updatePanoPOV = function (pano, source_heading_id, source_pitch_id) {

        var heading = 0;
        var pitch = 0;

        if (d$('#' + source_heading_id).val())
            heading = d$('#' + source_heading_id).val();

        if (d$('#' + source_pitch_id).val())
            pitch = d$('#' + source_pitch_id).val();

        pano.setPov({
            heading: parseFloat(heading),
            pitch: parseFloat(pitch)
        });
    };

    gmap.updateMapPosition = function (map, pano, source_id, lat_id, lng_id) {

        if (!d$('#' + source_id).val())
            return;

        var geocoder = new google.maps.Geocoder();
        var position = geocoder.geocode(
            {'address': d$('#' + source_id).val()},
            function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {

                    if (status != google.maps.GeocoderStatus.ZERO_RESULTS) {

                        var position = results[0].geometry.location;

                        map.setCenter(position);
                        var marker = new google.maps.Marker({map: map, position: position});

                        if (pano)
                            pano.setPosition(position);

                        if (gmap.has(lat_id)) {
                            d$('#' + lat_id).val(position.k);
                        }

                        if (gmap.has(lng_id)) {
                            d$('#' + lng_id).val(position.A);
                        }
                    }
                }
                else {
                    alert("Adresse Not Found;");
                }
            });
    };

    gmap.bindMapZoomListener = function (map, zoom_id) {
        google.maps.event.addListener(map, 'zoom_changed', function() {
            if (has(zoom_id))
                d$('#' + zoom_id).val(map.getZoom());
        });
    };

    gmap.bindPanoPOVListener = function (pano, heading_id, pitch_id) {

        google.maps.event.addListener(pano, 'pov_changed', function(){

            if (gmap.has(heading_id))
                d$('#' + heading_id).val(pano.getPov().heading);

            if (gmap.has(pitch_id))
                d$('#' + pitch_id).val(pano.getPov().pitch);
        });

    };

})(window.gmap = window.gmap || {}, django.jQuery);
