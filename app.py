from flask import Flask, render_template, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

app = Flask(__name__)

# Initialize the model and tokenizer
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")

# Language code to language name mapping
language_mapping = {
    "ar_AR": "Arabic",
    "cs_CZ": "Czech",
    "de_DE": "German",
    "en_XX": "English",
    "es_XX": "Spanish",
    "et_EE": "Estonian",
    "fi_FI": "Finnish",
    "fr_XX": "French",
    "gu_IN": "Gujarati",
    "hi_IN": "Hindi",
    "it_IT": "Italian",
    "ja_XX": "Japanese",
    "kk_KZ": "Kazakh",
    "ko_KR": "Korean",
    "lt_LT": "Lithuanian",
    "lv_LV": "Latvian",
    "my_MM": "Burmese",
    "ne_NP": "Nepali",
    "nl_XX": "Dutch",
    "ro_RO": "Romanian",
    "ru_RU": "Russian",
    "si_LK": "Sinhala",
    "tr_TR": "Turkish",
    "vi_VN": "Vietnamese",
    "zh_CN": "Chinese",
    "af_ZA": "Afrikaans",
    "az_AZ": "Azerbaijani",
    "bn_IN": "Bengali",
    "fa_IR": "Persian",
    "he_IL": "Hebrew",
    "hr_HR": "Croatian",
    "id_ID": "Indonesian",
    "ka_GE": "Georgian",
    "km_KH": "Khmer",
    "mk_MK": "Macedonian",
    "ml_IN": "Malayalam",
    "mn_MN": "Mongolian",
    "mr_IN": "Marathi",
    "pl_PL": "Polish",
    "ps_AF": "Pashto",
    "pt_XX": "Portuguese",
    "sv_SE": "Swedish",
    "sw_KE": "Swahili",
    "ta_IN": "Tamil",
    "te_IN": "Telugu",
    "th_TH": "Thai",
    "tl_XX": "Tagalog",
    "uk_UA": "Ukrainian",
    "ur_PK": "Urdu",
    "xh_ZA": "Xhosa",
    "gl_ES": "Galician",
    "sl_SI": "Slovene"
}


def translate_text(article_text, target_lang):
    # Tokenize the input text
    model_inputs = tokenizer(article_text, return_tensors="pt")

    # Generate the translation
    generated_tokens = model.generate(
        **model_inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang]
    )

    # Decode the generated tokens
    translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return translation[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        article_text = request.form['article_text']
        target_lang = request.form['target_lang']
        translated_text = translate_text(article_text, target_lang)
        return render_template('index.html', article_text=article_text, target_lang=target_lang, translated_text=translated_text, language_mapping=language_mapping)
    return render_template('index.html', language_mapping=language_mapping)

# Endpoint for AJAX translation requests
@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    article_text = data['article_text']
    target_lang = data['target_lang']
    translated_text = translate_text(article_text, target_lang)
    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
