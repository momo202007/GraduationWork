import boto3
translate = boto3.client('translate')
text = '昨日のご飯は美味しかった。'

#翻訳
result = translate.translate_text(
    Text=text, SourceLanguageCode='ja', TargetLanguageCode='en')
print(result['TranslatedText'])