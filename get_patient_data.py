# Define the normal ranges for lab values based on gender and age
def get_normal_ranges(gender, age):
    normal_ranges = {
        'CBC_RED_BLOOD_CELL_COUNT': (4.1, 5.5, 'm/cumm'),
        'CBC_WHITE_BLOOD_CELL_COUNT': (4.5, 10.5, 'k/cumm'),
        'CBC_Hemoglobin': (13.0, 18.0, 'gm/dL'),
        'CBC_PLATELET_COUNT': (100, 450, 'k/cumm'),
        'METABOLIC_ALT_SGPT': (10, 40, 'U/L'),
        'METABOLIC_GLUCOSE': (70, 100, 'mg/dL'),
        'METABOLIC_CREATININE': (0.5, 1.0, 'mg/dL'),
        'METABOLIC_BUN': (7, 20, 'mg/dL'),
        'METABOLIC_BILI_TOTAL': (0.1, 1.2, 'mg/dL'),
        'METABOLIC_ALBUMIN': (3.5, 5.0, 'gm/dL'),
        'METABOLIC_SODIUM': (135, 145, 'mmol/L'),
        'METABOLIC_POTASSIUM': (3.5, 5.1, 'mmol/L'),
        'URINALYSIS_RED_BLOOD_CELLS': (0, 2, 'rbc/hpf'),
        'URINALYSIS_WHITE_BLOOD_CELLS': (0, 5, 'wbc/hpf'),
        'URINALYSIS_PH': (5, 7, ''),
        'CBC_Lymphocytes': (20, 40, '%'),
        'CBC_Neutrophils': (40, 80, '%'),
        'CBC_Basophils': (0, 1, '%'),
        'CBC_Eosinophils': (0.1, 0.6, '%'),
        'CBC_Hematocrit': (42, 52, '%'),
        'CBC_MCH': (27, 31, 'pg'),
        'CBC_MCHC': (80, 100, 'g/L'),
        'CBC_Monocytes': (0.2, 1.0, '%'),
        'CBC_RDW': (11.5, 14, '%'),
        'METABOLIC_CARBON_DIOXIDE': (22, 29, 'mmol/L'),
        'METABOLIC_CHLORIDE': (96, 106, 'mmol/L'),
        'METABOLIC_TOTAL_PROTEIN': (6, 8, 'g/dL'),
        'METABOLIC_CALCIUM': (8.4, 10, 'mg/dL')
    }
    return normal_ranges

# Define normal BMI ranges based on gender and age
def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 24.9:
        return 'Normal weight'
    elif 25.0 <= bmi < 29.9:
        return 'Overweight'
    else:
        return 'Obese'

# Function to categorize lab test values
def categorize_value(value, low, high):
    if value < low:
        return 'Low'
    elif value > high:
        return 'High'
    else:
        return 'Normal'

# Function to provide preventive measures
def get_preventive_measures(row, gender, age, bmi, smoke, alcohol, exercise):
    measures = []

    normal_ranges = get_normal_ranges(gender, age)

    # Analyze each relevant column and provide advice
    for column, (low, high, _) in normal_ranges.items():
        if column in row:
            category = categorize_value(row[column], low, high)
            if category == 'Low':
                measures.append(f"{column} is low. Increase it by eating more nutrients, and consider increasing your intake of vegetables and fruits.")
            elif category == 'High':
                measures.append(f"{column} is high. Decrease it by reducing intake of specific foods, and consider eating more vegetables and fruits.")

    # BMI Analysis
    if gender == 'Male':
        if age >= 2 and age <= 5:
            if bmi < 14.1:
                measures.append("BMI is Underweight. Increase weight by eating healthy food.")
            elif 18.6 <= bmi <= 21.6:
                measures.append("BMI is Overweight. Reduce weight and maintain a proper diet.")
            elif bmi > 21.6:
                measures.append("BMI is Obese. Reduce weight and maintain a proper diet.")
        elif age >= 6 and age <= 11:
            if bmi < 15.3:
                measures.append("BMI is Underweight. Increase weight by eating healthy food.")
            elif 21.3 <= bmi <= 24.6:
                measures.append("BMI is Overweight. Reduce weight and maintain a proper diet.")
            elif bmi > 24.6:
                measures.append("BMI is Obese. Reduce weight and maintain a proper diet.")
        elif age >= 12 and age <= 19:
            if bmi < 16.1:
                measures.append("BMI is Underweight. Increase weight by eating healthy food.")
            elif 23.3 <= bmi <= 27.2:
                measures.append("BMI is Overweight. Reduce weight and maintain a proper diet.")
            elif bmi > 27.2:
                measures.append("BMI is Obese. Reduce weight and maintain a proper diet.")
        else:  # Adults
            if bmi < 18.5:
                measures.append("BMI is Underweight. Increase weight by eating healthy food.")
            elif 25.0 <= bmi <= 29.9:
                measures.append("BMI is Overweight. Reduce weight and maintain a proper diet.")
            elif bmi > 29.9:
                measures.append("BMI is Obese. Reduce weight and maintain a proper diet.")
    elif gender == 'Female':
        if age >= 2 and age <= 5:
            if bmi < 13.8:
                measures.append("BMI is Underweight. Increase weight by eating healthy food.")
            elif 18.2 <= bmi <= 21.2:
                measures.append("BMI is Overweight. Reduce weight and maintain a proper diet.")
            elif bmi > 21.2:
                measures.append("BMI is Obese. Reduce weight and maintain a proper diet.")
        elif age >= 6 and age <= 11:
            if bmi < 15.0:
                measures.append("BMI is Underweight. Increase weight by eating healthy food.")
            elif 21.1 <= bmi <= 24.1:
                measures.append("BMI is Overweight. Reduce weight and maintain a proper diet.")
            elif bmi > 24.1:
                measures.append("BMI is Obese. Reduce weight and maintain a proper diet.")
        elif age >= 12 and age <= 19:
            if bmi < 15.8:
                measures.append("BMI is Underweight. Increase weight by eating healthy food.")
            elif 22.7 <= bmi <= 26.1:
                measures.append("BMI is Overweight. Reduce weight and maintain a proper diet.")
            elif bmi > 26.1:
                measures.append("BMI is Obese. Reduce weight and maintain a proper diet.")
        else:  # Adults
            if bmi < 18.5:
                measures.append("BMI is Underweight. Increase weight by eating healthy food.")
            elif 25.0 <= bmi <= 29.9:
                measures.append("BMI is Overweight. Reduce weight and maintain a proper diet.")
            elif bmi > 29.9:
                measures.append("BMI is Obese. Reduce weight and maintain a proper diet.")

    # Lifestyle advice
    if smoke == 1:
        measures.append("Quit smoking.")
    if alcohol == 1:
        measures.append("Quit drinking alcohol.")
    if exercise == 0:
        measures.append("Start exercising regularly.")

    return measures