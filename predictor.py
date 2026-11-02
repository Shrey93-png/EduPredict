
def validate_inputs(name, attendance, assignment, internal, study_hours):
    errors = []

    if not str(name).strip():
        errors.append("Student name cannot be empty.")

    if not 0 <= attendance <= 100:
        errors.append("Attendance must be between 0 and 100.")

    if not 0 <= assignment <= 100:
        errors.append("Assignment marks must be between 0 and 100.")

    if not 0 <= internal <= 100:
        errors.append("Internal marks must be between 0 and 100.")

    if not 0 <= study_hours <= 24:
        errors.append("Study hours must be between 0 and 24.")

    return errors


def predict_performance(attendance, assignment, internal, study_hours):

    if (attendance >= 90 and assignment >= 85
            and internal >= 85 and study_hours >= 3):
        return "Excellent"

    elif (attendance >= 80 and assignment >= 70
          and internal >= 70 and study_hours >= 2):
        return "Good"

    elif (attendance >= 65 and assignment >= 50
          and internal >= 50 and study_hours >= 1):
        return "Average"

    else:
        return "Poor"


def generate_suggestions(attendance, assignment, internal, study_hours):

    suggestions = []

    if attendance < 75:
        suggestions.append("Improve class attendance.")

    if assignment < 60:
        suggestions.append("Practise more and submit assignments on time.")

    if internal < 60:
        suggestions.append("Revise topics and take practice tests.")

    if study_hours < 2:
        suggestions.append("Follow a regular study timetable.")

    if not suggestions:
        suggestions.append("Excellent work! Maintain your performance.")

    return " ".join(suggestions)
