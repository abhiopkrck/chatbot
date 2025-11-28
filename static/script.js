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
