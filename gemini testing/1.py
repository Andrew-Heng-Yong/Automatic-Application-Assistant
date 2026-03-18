from google import genai

client = genai.Client(api_key="AIzaSyDMEmEulCuwZ07w1P7M-lky6-thSTYGzx8")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="what is the definition of a mechanism in mechanical engineering?"
)

print(response.text)