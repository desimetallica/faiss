var videoListGlobal;
var queryResponse;

Dropzone.options.searchDropzone= {
	    paramName: "file", // The name that will be used to transfer the fil
	    maxFilesize: 10000, // MB
	    addRemoveLinks: true,
	    autoProcessQueue: true,
	    init: function() {
		console.log("init");
		this.on("addedfile", function(file) {   
			console.log("ciao");
			document.getElementById("results").innerHTML = "";
			resDiv = document.getElementById("results");        	
			img = document.createElement("img");
			//img.src = "img/gears.svg";
			//resDiv.appendChild(img);
		});
		
		this.on("success", function(file, response) {
			console.log("response OK 200");
			//console.log(response);
			//file.previewTemplate.appendChild(response);
			//var args = Array.prototype.slice.call(arguments);
			queryResponse = response;
			console.log(queryResponse);
			//loadVideoJS(file.name);
			//resDiv = document.getElementById("results").innerHTML = "";
			//loadImages(response);		        	
			loadResponse(response);
		});
	    }
	};

function initSearchDropzone(){
	console.log("preinit");
	var entireURL = location.href;
	var countPartURL=entireURL.split("/").length;
	var lastPartURL=entireURL.split("/")[countPartURL-1];
	var baseServerURL = entireURL.replace(lastPartURL,"");
	var basePathServerURL="";
	var checkBasePathServerURL=entireURL.split("/")[3];
	if(countPartURL>4)
	{
		basePathServerURL="/"+entireURL.split("/")[3];
	}			
	$("[data-toggle='tooltip']").tooltip();
}

function initPlayers(){
	player = videojs("videoQuery", {
        controls: true,        
    });
	     
	playerResult = videojs("playerResult", {
        controls: true,        
    });
}

function loadVideoJS(video)
{	
	console.log("video name is: "+video);
	var entireURL = location.href;
	var countPartURL=entireURL.split("/").length;
	var lastPartURL=entireURL.split("/")[countPartURL-1];
	var baseServerURL = entireURL.replace(lastPartURL,"");
	
	var baseServerStorageHTTP = location.protocol + "//" + location.hostname + ":8000";		
	
	var tmpFolder = "/tmp/IACABSearchControllerTmp/";
		
	source = baseServerStorageHTTP + tmpFolder + video;
	
	var sources = [{"type": "video/mp4", "src": source}];
    player.pause();
    player.src(sources);
    player.load();
    player.play();		
	//document.getElementById("videoQuery").setAttribute("src",baseServerStorageHTTP + tmpFolder + video);
}

function loadResponse(response){
	
	const respLength = response.length;
	var entireURL = location.href;
	var baseHost = entireURL.split(":")[1];
	//var baseServerURL = entireURL.replace(lastPartURL,"");

	console.log(baseHost);

		
	resDiv = document.getElementById("results").innerHTML = "";
	
	if(response.length != 0) {
		for(r = 0; r < response.length; r++) {
			if(response[r].path) {
				var imgResp = document.createElement("img");
				imgResp.id = "response-" + r;
				imgResp.className = "respImg"
				//http://localhost/home/teche/131254834/20170418131254834002.jpg
				imgResp.src = "http:" + baseHost + response[r].path;
				document.getElementById("results").appendChild(imgResp);
			}		
		}
	}
}

function loadImages(response){
	//var docs = response.docs;
	const respLength = response.length;
	var entireURL = location.href;
	var countPartURL=entireURL.split("/").length;
	var lastPartURL=entireURL.split("/")[countPartURL-1];
	var baseServerURL = entireURL.replace(lastPartURL,"");

	
	if(response.length==0) {
		console.log("A problem has occurred with server");
	} else {
		
		document.getElementById("querySlideshow").innerHTML = "";
		document.getElementById("resultSlideshow").innerHTML = "";
		
		for (r = 0; r < respLength; r++) {			
			if (response[r].docs[0].title) {
				$.ajax({
					type : "POST",
					//url : "http://localhost:8080/IACAB/lireSolrDemo/image",
					url:baseServerURL+"IACAB/lireSolrDemo/image",
					contentType: "text/plain; charset=UTF-8",
					//data: docs[idx].id,
					data:response[r].docs[0].title,
					async: false,
					success: function(data){
																		
						var imgResponse = document.createElement("img");
						var imgQuery = document.createElement("img");
						var imagePath=response[r].docs[0].title;
						//da notare che nella funzione noi diamo una stringa, facendo l'escape con il carattere '\'
						if( response[r].docs[0].d < 4.0 ){	
							imgResponse.id = "response-" + r;
							imgResponse.src = "data:image/jpg;base64," + data;
							imgResponse.className = "img-thumbnail-without-background-color selected_image";
							//img = "<img id='" +response[r].docs[0].d+ "' src='data:image/jpg;base64," + data + "' class='img-thumbnail-without-background-color selected_image' onclick=getVideoURLFromImagePath(\""+imagePath+"\")>";
						}
						else {
							imgResponse.id = "response-" + r;
							imgResponse.src = "data:image/jpg;base64," + data;
							imgResponse.className = "img-thumbnail-without-background-color";
							//img = "<img id='" +response[r].docs[0].d+ "' src='data:image/jpg;base64," + data + "' class='img-thumbnail-without-background-color' onclick=getVideoURLFromImagePath(\""+imagePath+"\")>";
						}
						document.getElementById("resultSlideshow").appendChild(imgResponse);
						document.getElementById("response-" + r).onclick = function(){
							console.log("onclick image path: " + imagePath);
							getVideoURLFromImagePath(imagePath);
						};
						
						imgQuery.id = "query-" + r;
						imgQuery.src = response[r].filePath;
						imgQuery.className = "img-thumbnail-without-background-color";
						
						var ptsTime = response[r].ptsTime;
						
						document.getElementById("querySlideshow").appendChild(imgQuery);
						imgQuery.onclick = function(){
							player.pause();
							player.currentTime(parseInt(ptsTime));
						};
							
					}
				});		
				
			}
		}
	}
}

function setQueryVideoTime(ptsTime){
	console.log("set query video time:" + ptsTime);

}

function videoShowResults(response) {
	
	//var docs = response.docs;
	const TABLE_COLUMNS = 4;
	const TABLE_ROWS = Math.ceil(response.length / TABLE_COLUMNS);
	var entireURL = location.href;
	var countPartURL=entireURL.split("/").length;
	var lastPartURL=entireURL.split("/")[countPartURL-1];
	var baseServerURL = entireURL.replace(lastPartURL,"");
	
	if(response.length==0)
	{
		bootbox.alert("Problem with images Solr core, no images found");
	}
	
	var table = "<table><tbody>";
	for (r = 0; r < TABLE_ROWS; r++) {
		var tr = "<tr>";
		for (c = 0; c < TABLE_COLUMNS; c++) {
			var idx = r * TABLE_COLUMNS + c;
			
			if (idx == response.length) break;
			if (response[idx].docs[0].title) {
				tr += "<td>";
				$.ajax({
					type : "POST",
					//url : "http://localhost:8080/IACAB/lireSolrDemo/image",
					url:baseServerURL+"IACAB/lireSolrDemo/image",
					contentType: "text/plain; charset=UTF-8",
					//data: docs[idx].id,
					data:response[idx].docs[0].title,
					async: false,
					success: function(data){
						imagePath=response[idx].docs[0].title;
						//da notare che nella funzione noi diamo una stringa, facendo l'escape con il carattere '\'
						if( response[idx].docs[0].d < 4.0 ){
							tr += "<img id='" +response[idx].docs[0].d+ "' src='data:image/jpg;base64," + data + "' class='img-thumbnail-without-background-color selected_image' onclick=getVideoURLFromImagePath(\""+imagePath+"\")>";
						}
						else {
							tr += "<img id='" +response[idx].docs[0].d+ "' src='data:image/jpg;base64," + data + "' class='img-thumbnail-without-background-color' onclick=getVideoURLFromImagePath(\""+imagePath+"\")>";
						}
					}
				});
				tr += "</td>";
			}									
		}
		tr += "</tr>";
		table += tr;
	}
	table += "</tbody></table>"
	
	$("#results").empty();
	$(table).appendTo($("#results"));	
	
}

function onFocusURLOut() {
    var url = $("#url").val();
    if (url) {
        $("#urlImage").attr("src", url);
        if ($( document ).width() <= 728) {
            $("#urlImage").css("width", "100%");
        } else {
            $("#urlImage").css("width", "100%");
        }
        $("#urlImage").css("margin-top", "15px");
        
    }
    
}

function onClickEnter(event)
{
	var keyCode =event.keyCode;
	
	if(keyCode==13)
	{
		onFocusURLOut();
	}
}

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#urlImage')
        .attr('src', e.target.result)
        .width(150)
        .height(200);
    };
    reader.readAsDataURL(input.files[0]);
  }
}



function search(nameKey, myArray){
    for (var i=0; i < myArray.length; i++) {
        if (myArray[i].docs[0].title === nameKey) {
            return myArray[i];
        }
    }
}
