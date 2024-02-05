const textContainer = document.getElementById("text-container");
document.addEventListener("DOMContentLoaded", function () {
    const text = "This is not an example text. Welcome to Text Animation! \
    Lorem ipsum dolor sit amet consectetur adipisicing elit.Enim\
     architecto repudiandae repellat, ducimus eligenditationem sit!";
    let index = 0;

    function updateText() {
        if (index < text.length) {
            //             textContainer.removeChild(textContainer.children[1])
            const span = document.createElement("span");
            span.textContent = text[index];
            textContainer.appendChild(span);

            const cursor = document.createElement("div");
            cursor.classList.add("cursor");
            textContainer.appendChild(cursor);

            index++;
            // Remove the cursor after a short delay (adjust as needed)
            setTimeout(() => {
                textContainer.removeChild(cursor);
            }, 50);
            requestAnimationFrame(updateText);
        }
    }

    // updateText();
    // textContainer.innerHTML = text;
});
// const baseURL = "http://127.0.0.1:5000"
const baseURL = "https://summarizer-q2lh.onrender.com"
execute_gemini = (website) => {
    var url = baseURL + "/fetch_gemini"
    var formData = new FormData();
    formData.append('url', website);
    textContainer.innerHTML = "LOADING...";

    fetch(url, {
        method: 'POST',
        body: formData
    })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(function (data) {
            // console.log(data)
            textContainer.innerHTML = data.gemini_response;
        }).catch(function (error) {
            console.log('There was a problem with the fetch operation:', error);
        });

};
const refreshbutton = document.getElementById('refresh')
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var tab = tabs[0];
    var url = tab.url;
    const ele = document.getElementById('newid');
    // ele.innerHTML = url;

    execute_gemini(url)
    refreshbutton.addEventListener('click', function () {
        execute_gemini(url)
    });
});
