function updateInfo() {
    fetch('/info')
        .then(response => response.json())
        .then(data => {
            let container = document.getElementById("info-container");
            container.innerHTML = ""; // Clear old content

            Object.entries(data).forEach(([key, value]) => {
                container.innerHTML += `
                    <div class="info-card">
                        <h5>${key}</h5>
                        <p>${value}</p>
                    </div>
                `;
            });
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Auto-refresh every 5 seconds
setInterval(updateInfo, 5000);

// Load data on page load
window.onload = updateInfo;

