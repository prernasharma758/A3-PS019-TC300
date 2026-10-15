const fileInput = document.getElementById('fileInput');
const auditedCount = document.getElementById('auditedCount');
const piiCount = document.getElementById('piiCount');

fileInput.addEventListener('change', function(event) {
    if (event.target.files.length > 0) {
        auditedCount.innerText = "01";
        piiCount.innerText = "03";
        alert("File successfully uploaded and audit started!");
    }
});