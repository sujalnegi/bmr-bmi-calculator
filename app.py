from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# --- Utility Functions for Conversions ---

def convert_lbs_to_kg(weight_lbs):
    # Only important comments
    return weight_lbs * 0.453592

def convert_ft_in_to_cm(feet, inches):
    # Only important comments
    total_inches = (feet * 12) + inches
    return total_inches * 2.54

# --- TDEE Calculation Core Function ---

def calculate_tdee(weight_kg, height_cm, age_years, gender, activity_factor):
    """Calculates TDEE using the Mifflin-St Jeor Equation."""
    BMR = 0
    
    # Calculate BMR based on gender
    if gender == 'male':
        BMR = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + 5
    elif gender == 'female':
        BMR = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) - 161
    else:
        # Fallback or error handling for unspecified
        return None 

    # Calculate TDEE
    TDEE = BMR * activity_factor
    return round(TDEE)

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize tdee_result to None; it will hold the calculation result
    tdee_result = None

    if request.method == 'POST':
        # 1. Get Form Data and Handle Errors
        try:
            # Personal Info (fetched from the form)
            age = int(request.form['age'])
            gender = request.form['gender']
            # Activity factor is sent as the option value (e.g., '1.55')
            activity_factor = float(request.form['activity'])

            # Weight Handling
            weight_input = float(request.form['weight'])
            weight_unit = request.form['weight-unit']
            
            # Height Handling
            height_unit = request.form['height-unit']

            # 2. Convert Weight to KG
            if weight_unit == 'lbs':
                final_weight_kg = convert_lbs_to_kg(weight_input)
            else:
                final_weight_kg = weight_input
            
            # 3. Convert Height to CM
            if height_unit == 'ftin':
                # Fetch feet and inches inputs (required attributes are set by JS)
                # Ensure a default of 0 if input is missing/empty, though 'required' should prevent this
                height_ft = float(request.form.get('height-ft') or 0)
                height_in = float(request.form.get('height-in') or 0)
                final_height_cm = convert_ft_in_to_cm(height_ft, height_in)
            else:
                # Fetch CM input
                final_height_cm = float(request.form['height-cm'])

            # 4. Calculate TDEE
            tdee_result = calculate_tdee(
                final_weight_kg, 
                final_height_cm, 
                age, 
                gender, 
                activity_factor
            )

        except Exception as e:
            # Catch exceptions like ValueError if input fields were left empty or invalid
            tdee_result = "Error: Please check your input values and ensure all required fields are filled correctly."
            print(f"Calculation Error: {e}")
    
    # Render the index.html template and pass the calculation result
    return render_template('index.html', tdee_result=tdee_result)

if __name__ == '__main__':
    # Runs the application on a local server
    app.run(debug=True)