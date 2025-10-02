import google.generativeai as genai
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("🤖 Available Gemini Models:")
print("=" * 50)

try:
    # List all available models
    models = genai.list_models()
    
    gemini_models = []
    for model in models:
        if 'gemini' in model.name.lower():
            model_name = model.name.replace('models/', '')
            gemini_models.append(model_name)
            
            print(f"📋 Model: {model_name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print(f"   Supported Methods: {', '.join(model.supported_generation_methods)}")
            print("-" * 40)
    
    print(f"\n✅ Total Gemini Models Found: {len(gemini_models)}")
    print("\n📝 Model Names for LangChain:")
    for model in gemini_models:
        print(f"   - {model}")
        
except Exception as e:
    print(f"❌ Error fetching models: {e}")
    print("\n🔧 Common model names to try:")
    print("   - gemini-1.5-pro")
    print("   - gemini-1.5-flash") 
    print("   - gemini-1.0-pro")
    print("   - gemini-2.0-flash-exp")