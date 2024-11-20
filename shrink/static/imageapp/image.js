var msgLine = document.getElementById("message");
const compressBtn = document.getElementById("compress-btn");
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.addEventListener("DOMContentLoaded", function () {
    form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const csrftoken = getCookie("csrftoken");
        const imageFile = document.getElementById("image").files[0];
        const compression_percentage =
            document.getElementById("compression-range").value;
        const formData = new FormData();
        const downloadBtn = document.getElementById("download-btn");
        formData.append("image", imageFile);
        formData.append("compression_percentage", compression_percentage);

        fetch("", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("DATA IS : ", data),
                    msgLine.style.visibility = "hidden",
                    (downloadBtn.style.visibility = "visible"),
                    (document.getElementById("response").textContent =
                        "New file size = " + data.filesize + "KB"),
                    (downloadBtn.href = `download_compressed_image?filename=${encodeURIComponent(
                        data.filename
                    )}`);
            })
            .catch((error) => console.error("Error:", error));
    });
});

document
    .getElementById("compression-range")
    .addEventListener("input", function () {
        document.getElementById("range-value").textContent = this.value + "%";
    });

document.getElementById("image").addEventListener("change", function () {
    var fileName = this.value.split("\\").pop();
    var reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById("preview-image").src = e.target.result;

        document.getElementById("range-container").style.visibility = "visible";
        compressBtn.style.visibility = "visible";
    };
    reader.readAsDataURL(this.files[0]);
});

compressBtn.addEventListener("click", function(){
    msgLine.style.visibility = "visible";
})

