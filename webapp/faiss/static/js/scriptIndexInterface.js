function getVideoURLFromImagePath(imagePath)
{	
	var entireURL = location.href;
	var countPartURL=entireURL.split("/").length;
	var lastPartURL=entireURL.split("/")[countPartURL-1];
	var baseServerURL = entireURL.replace(lastPartURL,"");
	var baseServerHTTP="http://localhost:80";
	alert("imagepath vale: "+imagePath);
	$.ajax({
		type : "GET",
		//url : "http://localhost:8080/IACAB/getVideoFromImagePath?imagePath="+imagePath,
		url: baseServerURL+"IACAB/getVideoFromImagePath?imagePath="+imagePath,
		contentType: "text/plain; charset=UTF-8",
	
		success: function(data){
			
			//bootbox.dialog({ message: '<div class="text-center">pippo</div>' });
			alert("il video legato all'immagine "+imagePath+"si trova qui : "+data);
			$("#videoContainer").empty();
			$('<video id="videoTag" width="320" height="240" controls>'+
											'<source id="videoSourceURL" src="" type="video/mp4">'+
										'</video>').appendTo('#videoContainer');
			document.getElementById("videoSourceURL").setAttribute("src",baseServerHTTP+data);
			var videoTag=document.getElementById("videoTag");
			videoTag.playbackRate=0.5;
			videoTag.load();
			
			}
	});
}

function getPlaySpeed() { 
	var vid=document.getElementById("videoTag");
	//vid.playbackRate=0.5;
    alert(vid.playbackRate);
} 