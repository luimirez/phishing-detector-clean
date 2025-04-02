document.addEventListener("DOMContentLoaded", function () {
    const scanBtn = document.getElementById("scanBtn");
    scanBtn.addEventListener("click", checkPhishing);
});

async function checkPhishing() {
    const emailText = document.getElementById("emailText").value;
    const resultElem = document.getElementById("result");

    resultElem.className = "loading";
    resultElem.textContent = "Scanning"

    const payload = {
        subject: "",
        body: emailText
    };

    try {
        
        const response = await fetch("https://phishing-detector-pnli.onrender.com/scan", {
            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            resultElem.textContent = "Error: " + response.statusText;
            return;
        }

        const result = await response.json();
        
        if (result.phishing) {
            resultElem.textContent = `${result.message}`;
            resultElem.className = "phishing";
        } else {
            resultElem.textContent = `${result.message}`;
            resultElem.className = "safe"
        }

    } catch (error) {
        resultElem.textContent = "Could not connect to API";
        resultElem.className = "phishing";
        console.error(error);
    }
}