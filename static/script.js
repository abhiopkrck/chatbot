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
