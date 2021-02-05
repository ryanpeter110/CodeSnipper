document.getElementById("snipText").addEventListener('click',function(){
    console.log("POPUP button clicked");
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs) {
        
        chrome.tabs.captureVisibleTab(null, {
            "format": "png"
        }, function (dataURI) {
            
            chrome.tabs.sendMessage(tabs[0].id, dataURI);
    
        });
      
    });
});
