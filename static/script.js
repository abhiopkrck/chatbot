async function send() {
    const prompt = document.getElementById("prompt").value;

    let res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    });

    let data = await res.json();
    document.getElementById("output").innerText = data.reply;
}
function img() {
    window.location.href = "https://ai-image-generator-6mq5.onrender.com/";
}
function generateImage(){
    const prompt = document.getElementById("prompt").value.trim();
    const result = document.getElementById("result");
    result.innerHTML = "Generating image...";

    fetch("/generate_image", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({prompt})
    }).then(res=>res.json())
    .then(data=>{
        if(data.success){
            const e = data.entry;
            result.innerHTML = `
                <h3>Generated Image:</h3>
                <img src="${e.image_url}" style="width:100%;margin:10px 0;">
                <p><b>Prompt:</b> ${e.prompt}</p>
                <p><b>Time:</b> ${e.created_at}</p>
            `;
            loadHistory();
        } else {
            result.innerHTML = "<p>Error generating image.</p>";
        }
    });
}
const chatDisplay = document.getElementById("chat-display");
const inputEntry = document.getElementById("input-entry");

document.getElementById("settings-btn").onclick = () => {
    document.getElementById("settings-panel").style.display = "flex";
};
function closeSettings(){
    document.getElementById("settings-panel").style.display = "none";
}

function appendMessage(sender, text){
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-msg" : "jarvis-msg";
    msg.innerText = `${sender}: ${text}`;
    chatDisplay.appendChild(msg);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

function sendPrompt(){
    const prompt = inputEntry.value.trim();
    if(!prompt) return;
    appendMessage("user", prompt);
    inputEntry.value = "";

    fetch("/send_prompt", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({prompt})
    }).then(res=>res.json())
    .then(data=>{
        appendMessage("Jarvis", data.response);
    });
}

// Add web
function addWeb(){
    const name = document.getElementById("web-name").value.trim();
    const url = document.getElementById("web-url").value.trim();
    if(!name||!url) return alert("Fill both fields");
    fetch("/add_web", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({name,url})})
    .then(()=>alert("Website added!"));
}

// Add app
function addApp(){
    const name = document.getElementById("app-name").value.trim();
    const path = document.getElementById("app-path").value.trim();
    if(!name||!path) return alert("Fill both fields");
    fetch("/add_app", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({name,path})})
    .then(()=>alert("App added!"));
}

// Simple voice recognition
function voiceMode(){
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();
    recognition.onresult = (event)=>{
        const speech = event.results[0][0].transcript;
        inputEntry.value = speech;
        sendPrompt();
    };
    recognition.onerror = (e)=>{
        alert("Voice recognition error");
    };
}
