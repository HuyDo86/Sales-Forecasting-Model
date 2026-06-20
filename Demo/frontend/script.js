async function uploadFile() {
    const file = document.getElementById("fileInput").files[0];
    const periods = document.getElementById("periods").value;

    if (!file) {
        alert("Vui lòng chọn file CSV");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
        `http://127.0.0.1:8000/predict?periods=${periods}`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();
    console.log("BACKEND DATA:", data);

    const table = document.getElementById("forecastTable");
    table.innerHTML = "";

    data.forecast.forEach((value, index) => {
        table.innerHTML += `
            <tr>
                <td>${index + 1}</td>
                <td>${Number(value).toFixed(2)}</td>
            </tr>
        `;
    });

    document.getElementById("chart").src =
        "data:image/png;base64," + data.image;
}
