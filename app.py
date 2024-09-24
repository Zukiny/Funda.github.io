from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            absences = int(request.form['absences'])
            prelim_exam_grade = float(request.form['prelim_exam_grade'])
            quizzes_grade = float(request.form['quizzes_grade'])
            requirements_grade = float(request.form['requirements_grade'])
            recitation_grade = float(request.form['recitation_grade'])
            
            result = calculate_grades(absences, prelim_exam_grade, quizzes_grade, requirements_grade, recitation_grade)

            if isinstance(result, str):
                return render_template('index.html', result=result)
            else:
                return render_template('index.html', 
                                       prelim_grade=result['prelim_grade'],
                                       pass_midterm=result['pass_midterm'],
                                       pass_final=result['pass_final'],
                                       deans_midterm=result['deans_midterm'],
                                       deans_final=result['deans_final'])
        except ValueError:
            return render_template('index.html', result="Invalid input. Please enter valid values.")

    return render_template('index.html')

def calculate_grades(absences, prelim_exam_grade, quizzes_grade, requirements_grade, recitation_grade):
    attendance_grade = 100 - (10 * absences)
    if absences >= 4:
        return "FAILED due to excessive absences."
    
    class_standing = (0.4 * quizzes_grade) + (0.3 * requirements_grade) + (0.3 * recitation_grade)
    
    prelim_grade = (0.6 * prelim_exam_grade) + (0.1 * attendance_grade) + (0.3 * class_standing)

    overall_target_pass = 75
    overall_target_deans = 90

    def required_grades(overall_target):
        for midterm in range(101):
            final = (overall_target - (0.2 * prelim_grade + 0.3 * midterm)) / 0.5
            if 0 <= final <= 100:
                return midterm, final
        return "Not possible", "Not possible"

    pass_midterm, pass_final = required_grades(overall_target_pass)
    deans_midterm, deans_final = required_grades(overall_target_deans)

    return {
        "prelim_grade": prelim_grade,
        "pass_midterm": pass_midterm,
        "pass_final": pass_final,
        "deans_midterm": deans_midterm,
        "deans_final": deans_final,
    }

if __name__ == '__main__':
    app.run(debug=True)
