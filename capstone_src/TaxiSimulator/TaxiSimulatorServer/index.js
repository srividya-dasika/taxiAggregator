
function initMap(areadata,userdata,taxidata) {
   console.log(userdata);
   console.log(areadata);
   console.log(taxidata);
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
      north: areadata[0]['southLat'],
      south: areadata[0]['northLat'],
      east: areadata[0]['eastLong'],
      west: areadata[0]['westLong'] ,
    },
  });

  // use a Material Icon as font
  for (let i=0; i<userdata.length; i++){
  new google.maps.Marker({
    position: { lat: userdata[i][`latitude`], lng: userdata[i][`longitude`] },
    map,
    label: {
      text: "\ue530",
      fontFamily: "Material Icons",
      color: "#ffffff",
      fontSize: "18px",
    },
    title: "Material Icon Font Marker",
  });
  }
  for(let t=0;t<taxidata.length;t++){
    console.log("Plotting for "+taxidata[t][`taxiName`])
    plotTaxi(map,taxidata[t][`taxiName`],taxidata[t][`startLat`],taxidata[t][`startLong`],taxidata[t][`endLat`],taxidata[t][`endLong`],"#000000");
  }
}

async function plotTaxi(map,taxiName,startLat,startLang,endLat,endLang,colorCode){
for (let i = startLat ,j=startLang; i < endLat& j<endLang ; i=i+0.0001,j=j+0.0001){
const taxiCoordinates = [
    { lat: i, lng: j },
    { lat: i+0.0001, lng: j+0.0001 },
  ];
    $.ajax({
        type: "POST",
        url: "http://localhost:1112/settaxicoords/"+taxiName+"&"+i+"&"+j,
    })
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