$(document).ready(function() {
    // Intercept the form submission with AJAX
    $("#translationForm").submit(function(event) {
        event.preventDefault();
        translateText();
    });

    // Function to handle translation with AJAX
    function translateText() {
        var article_text = $("#article_text").val();
        var target_lang = $("#target_lang").val();

        $.ajax({
            type: "POST",
            url: "/translate",
            contentType: "application/json",
            data: JSON.stringify({
                article_text: article_text,
                target_lang: target_lang
            }),
            success: function(data) {
                $("#translated_text").text(data.translated_text);
            },
            error: function(error) {
                console.error("Translation error:", error);
            }
        });
    }
});
