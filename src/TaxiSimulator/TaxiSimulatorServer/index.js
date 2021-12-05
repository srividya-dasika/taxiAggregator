
function initMap() {
   const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: { lat: 17.480660, lng: 78.493740 },
    mapTypeId: "terrain",
  });
  const rectangle = new google.maps.Rectangle({
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#FF0000",
    fillOpacity: 0.35,
    map,
    bounds: {
      north: 17.4977725,
      south: 17.4777725,
      east: 78.503740,
      west: 78.483740 ,
    },
  });

  // use a Material Icon as font
  new google.maps.Marker({
    position: { lat: 17.49778334, lng: 78.483940 },
    map,
    label: {
      text: "\ue530",
      fontFamily: "Material Icons",
      color: "#ffffff",
      fontSize: "18px",
    },
    title: "Material Icon Font Marker",
  });
  new google.maps.Marker({
    position: { lat: 17.48778334, lng: 78.493940 },
    map,
    label: {
      text: "\ue530",
      fontFamily: "Material Icons",
      color: "#ffffff",
      fontSize: "18px",
    },
    title: "Material Icon Font Marker",
  });
  new google.maps.Marker({
    position: { lat: 17.48798334, lng: 78.493040 },
    map,
    label: {
      text: "\ue530",
      fontFamily: "Material Icons",
      color: "#ffffff",
      fontSize: "18px",
    },
    title: "Material Icon Font Marker",
  });
  plotTaxi(map,17.48909989,78.503040, 17.5091000,78.523040,"#0000ff");
  plotTaxi(map,17.47909989,78.473040, 17.4991000,78.523040,"#00ff00");

}

async function plotTaxi(map,startLat,startLang,endLat,endLang,colorCode){
for (let i = startLat ,j=startLang; i < endLat& j<endLang ; i=i+0.0001,j=j+0.0001){
const taxiCoordinates = [
    { lat: i, lng: j },
    { lat: i+0.0001, lng: j+0.0001 },
   // { lat: -18.142, lng: 178.431 },
 //   { lat: -27.467, lng: 153.027 },
  ];
  const taxiPath = new google.maps.Polyline({
    path: taxiCoordinates,
    geodesic: true,
    strokeColor: colorCode,
    strokeOpacity: 1.0,
    strokeWeight: 2,
  });

    taxiPath.setMap(map)
    await sleep(1000);
 }}
 function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}