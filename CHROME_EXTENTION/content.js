var X,Y,WIDTH,HEIGHT,BASE64_IMAGE;

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {

    BASE64_IMAGE = request;   

    var original_scroll_position = getCurrentScrollPosition();
    var image_object = addImageToBody(BASE64_IMAGE);
    setScrollPosition(0);
    lockScrolling();
   
    // configure + start cropper
    const cropper = new Cropper(image_object, {
        aspectRatio : NaN,
        zoomable : false,
        autoCrop: true,
        autoCropArea: 0.001,
        movable: false,
        rotatable: false,
        toggleDragModeOnDblclick: false,
        crop(event) {
            // console.log(event.detail.x);
            // console.log(event.detail.y);
            // console.log(event.detail.width);
            // console.log(event.detail.height);
            setValues(event.detail.x,event.detail.y,event.detail.width,event.detail.height);
        },
        cropend(event) {
            // crop image
            var croppedImage = cropImage(BASE64_IMAGE,X,Y,WIDTH,HEIGHT);

            sendPayloadToServer(croppedImage);


            alert('Text Coppied to your Clipbard :)');

            removeImageFromBody();
            enableScrolling();
            setScrollPosition(original_scroll_position);
        }

      });
    
});

function downloadImage(base64_image){
    var a = document.createElement("a"); 
    a.href = base64_image; 
    a.download = "snippyImage.png"; 
    a.click(); 
}

function cropImage(base64_image, x, y, width, height) {
    var canvas = document.createElement("canvas");
    var context = canvas.getContext('2d');
    var imageObj = new Image();
    imageObj.src = base64_image;

    canvas.width = width;
    canvas.height = height;

    context.drawImage(imageObj, x, y, width, height, 0, 0, width, height);

    return canvas.toDataURL();
  
}

function sendPayloadToServer(base64_image){
    var ocr_endpoint = "http://127.0.0.1:3000/codeSnipper/getText/";
   
    var xhr = new XMLHttpRequest();
    xhr.open("POST", ocr_endpoint, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function(){ 
      if(this.status.toString() == "200"){

        // Copy text to clipboard
        copyToClipboard(this.response);
        console.log("data sent");
      }else{
        console.log("Error sending data");
      }
    };

    xhr.send(JSON.stringify({
        "base64_image":base64_image
    }));
    return false;
}

function setValues(x,y,width,height){
    X=x;
    Y=y;
    WIDTH = width;
    HEIGHT=height;
}

function setScrollPosition(scroll_position){
    document.documentElement.scrollTop = scroll_position;
}

function getCurrentScrollPosition(){
    return document.documentElement.scrollTop;
}


function lockScrolling(){
    document.body.style.overflow = 'hidden';
}

function enableScrolling(){
    document.body.style.overflow = 'visible'
}

function addImageToBody(dataURI) {
    const div = document.createElement('div');
    div.id = "codeSnipperDiv";
    document.body.prepend(div);

    var img = document.createElement('img');
    img.src = dataURI;
    img.style.display= "block";
    img.style.maxWidth = "100%" ;
    document.getElementById(div.id).prepend(img)
    return img;

}

function removeImageFromBody(image_object){
    document.body.removeChild(document.getElementById('codeSnipperDiv'));
}

function copyToClipboard(text) {
    var input = document.createElement('textarea');
    input.innerHTML = text;
    document.body.appendChild(input);
    input.select();
    var result = document.execCommand('copy');
    document.body.removeChild(input);
    return result;
}