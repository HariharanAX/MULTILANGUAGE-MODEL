document.addEventListener('DOMContentLoaded', function() {
    // Function to handle form submission
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Get form data
        const formData = new FormData(event.target);
        const textToTranslate = formData.get('text_to_translate');
        const sourceLanguage = formData.get('source_language');
        const targetLanguage = formData.get('target_language');

        // Send form data to server using fetch API
        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                text_to_translate: textToTranslate,
                source_language: sourceLanguage,
                target_language: targetLanguage,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            // Update the translation result on the page
            document.querySelector('.translation-result').innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error scenario here (e.g., display an error message)
        });
    });
});
