//import { faCar } from "@fontawesome/free-solid-svg-icons";
let taxiMarkers = {};
let IP = "localhost";
let PORT = "1112";
function initMap(areadata) {
   console.log(areadata);
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
  setUsersOnMap(map);
 // var taxis;
  taxis = setTaxisOnMap(map);
  console.log(taxis);
  for(let t=0;t<taxis.length;t++){
    console.log("Plotting for "+taxis[t]['reg_no'])
    plotTaxi(map,taxis[t]['reg_no'],taxis[t]['latitude'],taxis[t]['longitude'],"#000000");
  }
}

function setUsersOnMap(map){
var myurl = "http://"+IP+":"+PORT+"/userInitialLocations";
 $.ajax({
        type: "POST",
        url: myurl,
        contentType: 'application/json',
        data: JSON.stringify({
               "location":"Hyderabad",
               "currentLat":17.3850,
               "currentLong":78.4867
              }),
         dataType: 'json',
        success: function(userdata) {
                             // use a Material Icon as font
                             console.log(userdata);
                            for (let i=0; i<userdata.length; i++){
                            console.log("users lat longs - "+userdata[i][`latitude`]+userdata[i][`longitude`]);
                           // const image ="https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";;
                           const iconBase ="https://developers.google.com/maps/documentation/javascript/examples/full/images/";
                        new google.maps.Marker({
                                /* position: { lat: 17.4909, lng: 78.4990 },*/
                                    position: {lat:userdata[i][`longitude`], lng:userdata[i][`latitude`]},
                                      map,
                                      /*label: {
                                                 text: "\ue530",
                                                 fontFamily: "Material Icons",
                                                 color: "#ffffff",
                                                 fontSize: "18px",
                                               },*/
                                       icon: iconBase + "parking_lot_maps.png",
                                       title: "Material Icon Font Marker",
                                });
                              }
                             }
        })

}

function setTaxisOnMap(map){
var result=""
var myurl  = "http://"+IP+":"+PORT+"/taxiInitiallocations";
$.ajax({
        async: false,
        type: "POST",
        url: myurl,
        contentType: 'application/json',
        data: JSON.stringify({
               "location":"Hyderabad",
               "currentLat":17.3850,
               "currentLong":78.4867
              }),
         dataType: 'json',
         success: function(taxidata) {
                            result=taxidata;
                            var regNo = ''
                            console.log("got "+taxidata.length+" taxis");
                            for (let i=0; i<taxidata.length; i++){
                            regNo = taxidata[i][`reg_no`]
                            console.log("taxi lat longs - "+taxidata[i][`latitude`]+taxidata[i][`longitude`]);
                            const image ="user.svg";
                            const iconBase ="https://developers.google.com/maps/documentation/javascript/examples/full/images/";
                             const marker = new google.maps.Marker({
                                position: { lat: taxidata[i][`longitude`], lng: taxidata[i][`latitude`] },
                                map,
                                icon: iconBase + "library_maps.png",
                                title: "Taxis in the taxiApp",
                              });
                              taxiMarkers[regNo]= marker;
                              console.log("regNo="+regNo+"taxiMarker="+taxiMarkers[regNo])
                              marker.setMap(map);
                              }
                            }
        })
        console.log("taxiMarkers = "+taxiMarkers)
        return result;
}

async function plotTaxi(map,regNo,startLat,startLang,colorCode){
  //var i=0;
  //while (i<60) {
    var newLat=startLat;
    var newLong=startLang;
   // getTaxiCoords(taxiName)
   var myurl = "http://"+IP+":"+PORT+"/taxiCurrentLocations/";
   console.log("beforestringify"+regNo)
   console.log("stringifieddata- "+JSON.stringify({"reg_no":regNo}))
    $.ajax({
        type: "POST",
        url: myurl,
        contentType: 'application/json',
         data: JSON.stringify({
               "location":"Hyderabad",
               "reg_no":regNo
              }),
         dataType: 'json',
        success: function(newCoords) {
                            console.log("reg No = "+regNo)
                            taxiMarkers[regNo].setMap(null)
                            console.log("getting taxi locations for - "+regNo);
                             newLat=newCoords[0]['latitude'];
                             newLong = newCoords[0]['longitude'];
                             console.log("got new coordinates as -"+newLat+" & "+newLong)
                             const taxiCoordinates = [
                                    { lat: startLang, lng: startLat },
                                    { lat: newLong, lng: newLat },
                                ];
                            const taxiPath = new google.maps.Polyline({
                             path: taxiCoordinates,
                             geodesic: true,
                              strokeColor: colorCode,
                                strokeOpacity: 1.0,
                             strokeWeight: 2,
                            });
                             taxiPath.setMap(map);
                             const iconBase ="https://developers.google.com/maps/documentation/javascript/examples/full/images/";
                             const marker = new google.maps.Marker({
                                position: { lat: newLong, lng: newLat },
                                map,
                                icon: iconBase + "library_maps.png",
                                title: "Taxis in the taxiApp",
                              });
                              taxiMarkers[regNo]=marker;
                              marker.setMap(map);
                             }
    })
     await sleep(5000);
     plotTaxi(map,regNo,newLat,newLong,colorCode);
    //i++;

 }
 function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getTaxiCoords(regNo){
var  myurl = "http://"+IP+":"+PORT+"/taxiCurrentLocations/";
console.log("stringifieddata- "+JSON.stringify({"location":"Hyderabad","reg_no":regNo}))
 $.ajax({
        type: "POST",
        url: myurl,
        contentType: 'application/json',
        data: JSON.stringify({"location":"Hyderabad","reg_no":regNo}),
         dataType: 'json',
        success: function(newCoords) {
                            console.log("getting taxi locations for - "+regNo);

                             newLat=newCoords['latitude'];
                             newLong = newCoords['longitude'];
                             getTaxiCoords(regNo);
                             }
    })
 }