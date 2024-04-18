def calculate_quiz_score(answers):
    # Define the correct answers
    correct_answers = ['A', 'A', 'B', 'B', 'D', 'B', 'D', 'C', 'C', 'D']

    # Initialize score
    score = 0

    # Iterate through each question and check if the answer is correct
    for i in range(1, 11):
        # Construct the key for the current question in the answers dictionary
        answer_key = 'q' + str(i)
        
        # Check if the answer exists and if it matches the correct answer
        if answer_key in answers and answers[answer_key] == correct_answers[i - 1]:
            score += 1

    return score
