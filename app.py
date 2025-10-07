from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Flask ॲप सुरू करणे
app = Flask(__name__)

# सेव्ह केलेले मॉडेल आणि कॉलम्स लोड करणे
try:
    model = joblib.load('mushroom_model.joblib')
    model_columns = joblib.load('model_columns.joblib')
    print("Model and columns loaded successfully.")
except FileNotFoundError:
    print("Models and columns not found.plz check.")
    model = None
    model_columns = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    model_columns = None

@app.route('/predict', methods=['POST'])
def predict():
    # मॉडेल लोड झाले आहे की नाही हे तपासणे
    if model is None or model_columns is None:
        return jsonify({'error': 'model not loaded,please check server log.'}), 500

    # रिक्वेस्टमधून JSON डेटा मिळवणे
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Data not found in request (JSON format required).'}), 400

    try:
        # JSON डेटाला DataFrame मध्ये रूपांतरित करणे
        input_df = pd.DataFrame([json_data])

        # आलेल्या डेटाचे वन-हॉट एन्कोडिंग करणे
        input_encoded = pd.get_dummies(input_df)

        # मूळ मॉडेलनुसार कॉलम्स जुळवणे (Reindexing)
        # जे कॉलम्स इनपुटमध्ये नाहीत, ते 0 ने भरले जातील
        final_df = input_encoded.reindex(columns=model_columns, fill_value=0)

        # भविष्यवाणी करणे
        prediction = model.predict(final_df)
        probability = model.predict_proba(final_df)

        # भविष्यवाणीच्या आधारावर परिणाम देणे (0 = Edible, 1 = Poisonous)
        if prediction[0] == 1:
            result = 'Poisonous'
        else:
            result = 'Edible'

        # JSON प्रतिसाद तयार करणे
        response = {
            'prediction': result,
            'probability': {
                'edible': round(probability[0][0], 4),
                'poisonous': round(probability[0][1], 4)
            }
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'error found while predictions: {e}'}), 500

# हा भाग महत्त्वाचा आहे - यामुळे सर्वर फक्त एकदाच सुरू होतो
if __name__ == '__main__':
    app.run(debug=True, port=5000)