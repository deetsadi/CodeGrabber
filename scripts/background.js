let id = 100;
var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.4.1.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);

chrome.browserAction.onClicked.addListener(() => {

  chrome.tabs.captureVisibleTab((screenshotUrl) => {
    decoded = getText(screenshotUrl)
    alert("Code copied to clipboard! Just use Ctrl+V to paste.")
  });
});

async function Request(url = '', data = {}, method = 'POST') {
    // Default options are marked with *
    const response = await fetch(url, {
      method: method, // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        // 'Content-Type': "application/json;charset=utf-8",
        'Content-Type':'application/json',
        'Accept':'application/json'
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function getText(input){
    console.log("in getText")
    var out = ""

    h = Request(url="http://127.0.0.1:5000/getText", data={"data":input})
    var out = ""
    h.then(function(result){
        console.log(result.result)
        document.addEventListener('copy', function(e) {
            var textToPutOnClipboard = result.result;
            e.clipboardData.setData('text/plain', textToPutOnClipboard);
            e.preventDefault();
          });
        document.execCommand('copy')
        out =result.result
    })

    return out;
}