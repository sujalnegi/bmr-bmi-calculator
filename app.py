from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def convert_lbs_to_kg(weight_lbs):
    return weight_lbs * 0.453592

def convert_ft_in_to_cm(feet, inches):
    total_inches = (feet * 12) + inches
    return total_inches * 2.54

# tdee calculation function

def calculate_tdee(weight_kg, height_cm, age_years, gender, activity_factor):
    """Calculates tdee using the Mifflin-St Jeor Equation."""
    BMR = 0
    
    # Calculation of BMR based on gender
    if gender == 'male':
        BMR = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + 5
    elif gender == 'female':
        BMR = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) - 161
    else:
        return None 

    TDEE = BMR * activity_factor
    return round(TDEE)

# --- BMI Calculation---

def calculate_bmi_and_category(weight_kg, height_cm):
    """Calculates BMI (kg/m^2) and determines the health category."""
    # Convert height from cm to meters
    height_m = height_cm / 100
    
    if height_m == 0:
        return None, "Error: Height cannot be zero."

    BMI = weight_kg / (height_m ** 2)
    
    # Catrgory conditions
    if BMI < 18.0:
        category = "Underweight"
    elif 18.0 <= BMI < 25:
        category = "Normal (Healthy Weight)"
    elif 25 <= BMI < 30:
        category = "Overweight"
    else:
        category = "Obese"
        
    return round(BMI, 1), category

# Advice generation ---
def generate_advice(bmi_category):
    
    if "Normal" in bmi_category:
        return "You are a healthy Person! Stay fit. 👍"
    elif "Overweight" in bmi_category or "Obese" in bmi_category:
        return "Yout need to take dieting seriouslyy from now! 🥗🏃"
    elif "Underweight" in bmi_category:
        return "You should eat more foood! 🍎💪"
    else:
        return "Maintain healthy eating habits and regular physical activity."

# Flask Routes 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    # 1. Get Form Data and Handle Errors
    try:
        # Personal Information
        age = int(request.form['age'])
        gender = request.form['gender']
        activity_factor = float(request.form['activity'])

        # Weight 
        weight_input = float(request.form['weight'])
        weight_unit = request.form['weight-unit']
        
        # Height 
        height_unit = request.form['height-unit']

        # 2. Convert Weight to kg
        final_weight_kg = convert_lbs_to_kg(weight_input) if weight_unit == 'lbs' else weight_input
        
        # 3. Convert Height to cm
        if height_unit == 'ftin':
            height_ft = float(request.form.get('height-ft') or 0)
            height_in = float(request.form.get('height-in') or 0)
            final_height_cm = convert_ft_in_to_cm(height_ft, height_in)
        else:
            final_height_cm = float(request.form['height-cm'])

        # 4. actial Calculations
        tdee_result = calculate_tdee(
            final_weight_kg, final_height_cm, age, gender, activity_factor
        )
        bmi_value, bmi_category = calculate_bmi_and_category(
            final_weight_kg, final_height_cm
        )
        
        # 5. advice generation
        advice_message = generate_advice(bmi_category)
        
        # 6. Redirect to results page
        return render_template(
            'result.html', 
            tdee=tdee_result, 
            bmi=bmi_value, 
            category=bmi_category,
            advice=advice_message 
        )

    except Exception as e:
        print(f"Calculation Error: {e}")
        # missing field redirects to index.html
        return redirect(url_for('index', error=True))


if __name__ == '__main__':
    app.run(debug=True)
