// filepath: c:\Users\nikao\Desktop\TJ\TJ_Project\frontend\renderer.js
document.getElementById('generate').addEventListener('click', function() {
    const classe = document.getElementById('classe').value;
    const dataInicio = document.getElementById('dataInicio').value;
    const dataFinal = document.getElementById('dataFinal').value;

    // Validate input
    if (!classe || !dataInicio || !dataFinal) {
        document.getElementById('output').innerText = 'Please fill in all fields.';
        return;
    }

    // Send data to the backend (this is a placeholder for actual backend communication)
    console.log(`Generating PDF for Classe: ${classe}, Data Início: ${dataInicio}, Data Final: ${dataFinal}`);

    // Here you would typically make an API call to the backend to generate the PDF
    // For example, using fetch or XMLHttpRequest
    // fetch('/generate-pdf', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({ classe, dataInicio, dataFinal })
    // })
    // .then(response => response.json())
    // .then(data => {
    //     document.getElementById('output').innerText = 'PDF generated successfully!';
    // })
    // .catch(error => {
    //     document.getElementById('output').innerText = 'Error generating PDF.';
    //     console.error('Error:', error);
    // });
});