
function scanDuplicates() {
    const folderPath = document.getElementById('folder-path').value;
    if (!folderPath) {
        alert("Please enter a folder path");
        return;
    }

    window.pywebview.api.find_duplicates(folderPath).then((groups) => {
        const resultsDiv = document.getElementById('results');
        if (groups.length === 0) {
            resultsDiv.innerText = "No duplicates found.";
        } else {
            let resultText = "";
            groups.forEach((group, idx) => {
                resultText += `🔁 Group ${idx + 1}\n`;
                group.forEach((file) => {
                    resultText += `  ${file}\n`;
                });
                resultText += `\n`;
            });
            resultsDiv.innerText = resultText;
        }
    });
}
