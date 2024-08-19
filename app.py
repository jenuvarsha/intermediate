import streamlit as st
from get_patient_data import get_normal_ranges,get_bmi_category,categorize_value,get_preventive_measures
from generative_ai import chat_bot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dataset import df

# Calculate Age from AdmissionYear and BirthYear
df['AdmissionYear'] = pd.to_datetime(df['AdmissionStartDate']).dt.year
df['BirthYear'] = pd.to_datetime(df['PatientDateOfBirth']).dt.year
df['Age'] = df['AdmissionYear'] - df['BirthYear']

def chatbot_interface(df):
    st.title('Chatbot Interface')
    patient_id_input = st.text_input('Enter PatientID:', '')

    if patient_id_input:
        # Filter dataset by PatientID
        patient_data = df[df['PatientID'] == patient_id_input]
        
        if not patient_data.empty:
            # Get all claim IDs for the patient
            patient_claims = patient_data.sort_values(by='AdmissionStartDate')
            claim_id_list = patient_claims['ClaimID'].tolist()

            # Add a dropdown to select ClaimID
            selected_claim_id = st.selectbox('Select ClaimID:', claim_id_list)
            patient_claim = patient_claims[patient_claims['ClaimID'] == selected_claim_id]
            if not patient_claim.empty:
                st.success(f"Claim ID {selected_claim_id} verified.")
                user_input = st.text_input("How can I help you? (Type 'diet plan' or 'workout plan')")
                
                if user_input:
                    if 'diet' in user_input.lower():
                        glucose = patient_claim['METABOLIC_GLUCOSE'].values[0]
                        creatinine = patient_claim['METABOLIC_CREATININE'].values[0]
                        response_prompt = f"Give me a south indian food based diet plan based on METABOLIC_GLUCOSE {glucose} and METABOLIC_CREATININE {creatinine} values in just four points."
                        response = chat_bot(response_prompt)
                        st.write(response)
                        
                        if st.button('Get Detailed Plan'):
                            detailed_prompt = f"Give me a detailed diet plan based on METABOLIC_GLUCOSE {glucose} and METABOLIC_CREATININE {creatinine} values."
                            detailed_response = chat_bot(detailed_prompt)
                            st.write(detailed_response)
                    
                    elif 'workout' in user_input.lower():
                        bmi = patient_claim['BMI'].values[0]
                        response_prompt = f"Give me a very brief workout plan based on BMI {bmi} values in just four points."
                        response = chat_bot(response_prompt)
                        st.write(response)
                        if st.button('Get Detailed Plan'):
                            detailed_prompt = f"Give me a detailed workout plan based on BMI {bmi} values."
                            detailed_response = chat_bot(detailed_prompt)
                            st.write(detailed_response)
                    else:
                        st.warning("Please choose either 'diet plan' or 'workout plan'.")
            else:
                st.error("Claim ID not found. Please check the entered Claim ID.")

# Sidebar
st.sidebar.title('Menu')
menu_option = st.sidebar.radio('Select an option:', ['Dashboard', 'Preventive Measures','Chatbot'])

if menu_option == 'Dashboard':
    # User login
    st.title('Patient Lab Value and Lifestyle Analysis Dashboard')
    patient_id_input = st.text_input('Enter PatientID:', '')

    if patient_id_input:
        # Filter dataset by PatientID
        patient_data = df[df['PatientID'] == patient_id_input]
        
        if not patient_data.empty:
            # Get all claim IDs for the patient
            patient_claims = patient_data.sort_values(by='AdmissionStartDate')
            claim_id_list = ['ALL'] + patient_claims['ClaimID'].tolist()  # Add "ALL" option at the beginning

            # Add a dropdown to select ClaimID
            selected_claim_id = st.selectbox('Select ClaimID:', claim_id_list)

            if selected_claim_id == 'ALL':
                # Compare across all claims for this patient
                st.subheader('Comparison Across All Claim IDs')

                # Compare Lifestyle Factors
                st.subheader('Lifestyle Factors Comparison')
                lifestyle_data = patient_claims[['ClaimID', 'Smoke', 'Alcohol', 'Exercise']]
                fig_lifestyle = px.bar(lifestyle_data.melt(id_vars='ClaimID', var_name='Lifestyle Factor', value_name='Value'),
                                       x='ClaimID', y='Value', color='Lifestyle Factor',
                                       barmode='group', height=400)
                st.plotly_chart(fig_lifestyle)

                # Compare BMI across all claims
                st.subheader('BMI Comparison')
                fig_bmi = px.bar(patient_claims, x='ClaimID', y='BMI', color='BMI',
                                 color_continuous_scale='RdYlGn', height=400)
                st.plotly_chart(fig_bmi)

                # Compare Lab Values across all claims
                st.subheader('Lab Values Comparison')
                cols = st.columns(3)
                for i, (col, (_, _, unit)) in enumerate(get_normal_ranges('', 0).items()):
                    fig = px.bar(patient_claims, x='ClaimID', y=col,
                                 color_discrete_sequence=['#00CC96'],
                                 title=f'{col} ({unit})')
                    cols[i % 3].plotly_chart(fig)
            else:
                # Filter dataset by selected ClaimID
                selected_data = patient_claims[patient_claims['ClaimID'] == selected_claim_id]
                
                # Extract relevant data
                gender = selected_data['PatientGender'].values[0]
                age = selected_data['Age'].values[0]
                bmi = selected_data['BMI'].values[0]
                smoke = selected_data['Smoke'].values[0]
                alcohol = selected_data['Alcohol'].values[0]
                exercise = selected_data['Exercise'].values[0]
                normal_ranges = get_normal_ranges(gender, age)
                bmi_category = get_bmi_category(bmi)

                # Visualize Lifestyle Factors
                st.subheader('Lifestyle Factors')
                col1, col2, col3 = st.columns(3)

                col1.markdown(f'<div style="font-size:20px; text-align:center;">Smoke: {"Yes" if smoke else "No"}</div>', unsafe_allow_html=True)
                col2.markdown(f'<div style="font-size:20px; text-align:center;">Alcohol: {"Yes" if alcohol else "No"}</div>', unsafe_allow_html=True)
                col3.markdown(f'<div style="font-size:20px; text-align:center;">Exercise: {"Yes" if exercise else "No"}</div>', unsafe_allow_html=True)

                # Visualize BMI with normal range
                st.subheader('BMI Analysis')
                fig_bmi = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=bmi,
                    gauge={'axis': {'range': [10, 40]},
                           'steps': [
                               {'range': [10, 18.5], 'color': "lightblue"},
                               {'range': [18.5, 24.9], 'color': "lightgreen"},
                               {'range': [24.9, 29.9], 'color': "orange"},
                               {'range': [29.9, 40], 'color': "red"}],
                           'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': bmi}}))
                st.plotly_chart(fig_bmi)

                # Display BMI Category in a Card
                st.subheader('BMI Category')
                st.markdown(f'<div style="font-size:24px; color:#007bff; border-radius:10px; padding:10px; background-color:#e6f7ff; text-align:center;">{bmi_category}</div>', unsafe_allow_html=True)

                # Visualize Lab Values
                st.subheader('Lab Values')
                cols = st.columns(3)
                for i, (col, (lower, upper, unit)) in enumerate(normal_ranges.items()):
                    current_value = selected_data[col].values[0]
                    fig = px.bar(
                        x=[col],
                        y=[current_value],
                        color_discrete_sequence=['#00CC96' if lower <= current_value <= upper else '#FF4136']
                    )
                    fig.add_shape(
                        type='rect', x0=-0.4, x1=0.4, y0=lower, y1=upper,
                        line=dict(color='rgba(50, 171, 96, 0.6)', width=2)
                    )
                    fig.update_layout(
                        title_text=f'{col} ({unit})\n(Normal Range: {lower}-{upper})',
                        showlegend=False,
                        yaxis_range=[0, upper * 1.2]  # Adjust the y-axis for better visibility
                    )
                    cols[i % 3].plotly_chart(fig)

                st.write(f"### Showing data for ClaimID: {selected_claim_id}")

                # Display preventive measures
                st.subheader('Preventive Measures')
                measures = get_preventive_measures(selected_data.iloc[0], gender, age, bmi, smoke, alcohol, exercise)
                for measure in measures:
                    st.write(f"- {measure}")

        else:
            st.error("CPatientID not found. Please check the entered PatientID.")
elif menu_option == 'Preventive Measures':
    st.title('Preventive Measures')
    patient_id_input = st.text_input('Enter PatientID:', '')

    if patient_id_input:
        # Filter dataset by PatientID
        patient_data = df[df['PatientID'] == patient_id_input]
        
        if not patient_data.empty:
            # Get all claim IDs for the patient
            claim_id_list = patient_data['ClaimID'].tolist()
            
            # Add a dropdown to select ClaimID
            selected_claim_id = st.selectbox('Select ClaimID:', claim_id_list)

            # Filter data for the selected ClaimID
            selected_data = patient_data[patient_data['ClaimID'] == selected_claim_id]

            # Extract relevant data
            row = selected_data.iloc[0]
            gender = row['PatientGender']
            age = row['Age']
            bmi = row['BMI']
            smoke = row['Smoke']
            alcohol = row['Alcohol']
            exercise = row['Exercise']

            # Get preventive measures
            measures = get_preventive_measures(row, gender, age, bmi, smoke, alcohol, exercise)

            st.subheader(f"Preventive Measures")
            for measure in measures:
                st.write(f"- {measure}")

        else:
            st.error("PatientID not found. Please check the entered PatientID.")

elif menu_option == 'Chatbot':
    chatbot_interface(df)
