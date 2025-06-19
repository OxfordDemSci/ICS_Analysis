import * as _utils from './utils.js?version=3'



export function updateUKregion_counts_map(_map, _layer, dataUK_counts) {

    var clustersIconUKinstitution = L.icon({
        iconUrl: "img/record-circle.svg",
        iconSize: [30, 30]
    });

    _map.setView([54.5, -3], 5);
    
    _layer.clearLayers();

    _map.removeLayer(_layer);

    var addresses = L.geoJson(dataUK_counts, {
        pointToLayer: function (feature, latlng) {
            var marker = L.marker(latlng, {icon: clustersIconUKinstitution});
            marker.bindPopup('<div><span><strong>' + feature.properties.name + '</strong></span><br/><span>Impact Case Studies: ' + feature.properties.count + '</span></div>');
            return marker;
        }
    });
    _layer.addLayer(addresses);
    _map.addLayer(_layer);

}


