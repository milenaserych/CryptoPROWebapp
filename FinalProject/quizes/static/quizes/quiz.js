const url = window.location.href;
const quizBox = document.getElementById('quiz-box');
const scoreBox = document.getElementById('score-box');
const resultBox = document.getElementById('result-box');
const quizForm = document.getElementById('quiz-form');
const endBox = document.getElementById('end-box');
const csrf = document.getElementsByName('csrfmiddlewaretoken');
let currentQuestionIndex = 0;
let response;
let userAnswers = [];
let saveButton;
let nextButton;
let correctAnswer;
let noCorrectAnswers = 0;
let noQuestions = 0;
let isRevision = false
let requiredScore
let quizName

// Make an AJAX request to get quiz data when the page loads
$.ajax({
    type: 'GET',
    url: `${url}data/`,
    success: function (initialResponse) {
        // console.log("This is the initial response:", initialResponse);
        response = initialResponse; // Store the response globally
        let data = response.data;
        requiredScore = response.r_score;
        quizName = response.quiz_name;
        // Display the first question when data is retrieved
        displayQuestion(data, currentQuestionIndex);
    },
    error: function (error) {
        console.log(error);
    }
});

// Modify displayQuestion to handle undefined or non-array currentQuestion.answers
const displayQuestion = (data, index) => {
    quizBox.innerHTML = '';

    const currentQuestion = data[index];
    const questionText = Object.keys(currentQuestion)[0];
    const questionAnswers = currentQuestion[questionText];
    // console.log("Current question: ", questionText)
    // console.log("Answers: ", questionAnswers)
    noQuestions = data.length

    quizBox.innerHTML += `
        <div class="question-progress ml-3">
            Question ${index + 1} of ${data.length}
        </div>
        <hr>
        <div class="quiz-container">
            <div class="quiz-question">
                <b>${questionText}</b>
            </div>
            <div class="quiz-answers">
                ${generateAnswerButtons(questionAnswers)}
            </div>
        </div>
    `;

    createButtons(data)
};


// Modify createButtons to accept data as a parameter
const createButtons = (data) => {
    saveButton = document.createElement("button");
    saveButton.type = 'button';
    saveButton.className = 'btn btn-primary mt-3 ml-3';
    saveButton.textContent = 'Save';
    saveButton.disabled = true;

    // Add event listener to check if an answer is selected
    document.querySelectorAll('input[name="answer"]').forEach(input => {
        input.addEventListener('change', () => {
            saveButton.disabled = false; // Enable save button when an answer is selected
        });
    });

    saveButton.addEventListener('click', function saveOnce(event) {
         // Disable all answer radio buttons
         document.querySelectorAll('input[name="answer"]').forEach(input => {
            input.disabled = true;
        });

        // Execute saveUserAnswer function
        saveUserAnswer(data, currentQuestionIndex);
    
        // Disable saveButton and enable nextButton
        saveButton.disabled = true;
        nextButton.disabled = false;
    
        // Remove event listener after executing once
        saveButton.removeEventListener('click', saveOnce);
    });

    quizBox.appendChild(saveButton);

    nextButton = document.createElement("button");
    nextButton.type = 'button';
    nextButton.className = 'btn btn-primary mt-3 ml-3';
    nextButton.textContent = 'Next';
    nextButton.id = 'nextButton';
    nextButton.disabled = true;

    nextButton.addEventListener('click', () => {
        // Check if an answer is selected before moving to the next question
        if (!document.querySelector('input[name="answer"]:checked')) {
            alert('Please select an answer before moving to the next question.');
            return;
        }

        currentQuestionIndex++;
        if (currentQuestionIndex < data.length) {
            displayQuestion(data, currentQuestionIndex);
        } else {
            // Check if it's a revision quiz and handle completion
            
            if (isRevision) {
                console.log("Check isRevision is TRUE")
                // If there are more questions in the revision, show the next one
                completeRevisionQuiz();
            } else {
                sendData(response.data);
            }
        }
    });
    quizBox.appendChild(nextButton);
};


// Function to generate answer buttons as a column
const generateAnswerButtons = (questionAnswers) => {

    if (!Array.isArray(questionAnswers)) {
        console.error('Error: questionAnswers is not an array.');
        return '';
    }
    let buttonsHTML = '';
    questionAnswers.forEach(answer => {
        buttonsHTML += `
            <div class="quiz-answer">
                <input 
                    type="radio" 
                    class="ans" 
                    id="${answer.text}" 
                    name="answer" 
                    value="${answer.text}"
                >
                <label for="${answer.text}">${answer.text}</label>
            </div>
        `;
        if (answer.correct) {
            correctAnswer = answer.text;
            quizBox.dataset.correctAnswer = correctAnswer;
            // console.log(`Correct answer for question: ${answer.question} is ${answer.text}`);
        } 
    });
    return buttonsHTML;
}

// Function to save user's answer and display feedback
const saveUserAnswer = (data, index) => {
    const selectedAnswer = document.querySelector('input[name="answer"]:checked');

    if (!selectedAnswer) {
        // Handle the case where no answer is selected
        alert('Please select an answer before saving.');
        return;
    }

    if (selectedAnswer.value === correctAnswer) {
        // Only increment noCorrectAnswers if the answer is correct
        noCorrectAnswers++;
    }

    userAnswers.push({
        question: Object.keys(data[index])[0],
        selectedAnswer: selectedAnswer.value
    });

    // Display correctness feedback
    displayFeedback(data[index], selectedAnswer.value);
}

// Function to send data to the server
const sendData = (data) => {
    const elements = [...document.getElementsByClassName('ans')];
    const postData = {};
    postData['csrfmiddlewaretoken'] = csrf[0].value;

    if (userAnswers.length === noQuestions) {
        const postData = {};
        postData['csrfmiddlewaretoken'] = csrf[0].value;

        userAnswers.forEach(answer => {
            postData[answer.question] = answer.selectedAnswer;
        });

        $.ajax({
            type: 'POST',
            url: `${url}save/`,
            data: postData,
            success: function (response) {
                // Handle success, you can update UI or take further actions
                console.log("Success response of the POST AJAX request: ", response);
                // Display correctness feedback
                displayFeedback(data[currentQuestionIndex], postData['answer']);

                currentQuestionIndex++;
                if (currentQuestionIndex < data.length) {
                    // Continue to the next question if there are more
                    displayQuestion(data, currentQuestionIndex);
                } else {
                    // Display overall results if it's the last question
                    console.log("Response data: ", response.data)
                    displayOverallResults(response);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
};

// Function to display correctness feedback
const displayFeedback = (questionData, selectedAnswer) => {
    const feedbackDiv = document.createElement("div");
    feedbackDiv.className = 'feedback';

    if (selectedAnswer === correctAnswer) {
        feedbackDiv.innerHTML = `Your answer "${selectedAnswer}" is correct!`;
        feedbackDiv.classList.add('correct-feedback');
    } else {
        feedbackDiv.innerHTML = `Your answer "${selectedAnswer}" is incorrect. The correct answer is "${correctAnswer}".`;
        feedbackDiv.classList.add('incorrect-feedback');
    }

    quizBox.appendChild(feedbackDiv);
}


// Function to display overall results
const displayOverallResults = (response) => {
    // Hide the quiz form
    quizForm.classList.add('not-visible');
    // Call calculateScore and log the result
    const score = parseInt(calculateScore());

    // Check if the user passed the quiz based on the required score
    let didPass = false;
    console.log("Score: ", score)
    console.log("Required score to pass: ", requiredScore)
    if(score >= requiredScore){
        didPass = true;
    }
    console.log("didPass: ", didPass)
    
    // Display user's score
    scoreBox.innerHTML = `Your result is ${score}%!`;

    if (didPass) {
        // If the user passed, display individual results and revision option
        resultBox.innerHTML = 'You have passed the quiz!';
        let hasIncorrectAnswers = false;
        // Display individual results for each question
        userAnswers.forEach(answer => {
            const questionText = answer.question;
            const selectedAnswer = answer.selectedAnswer;

            const resDiv = document.createElement("div");

            // Check if the answer is correct or not answered
            if (response.results) {
                const resultData = response.results.find(result => Object.keys(result)[0] === questionText);

                if (resultData) {
                    const correctAnswer = resultData[questionText].correct_answer;
                    const isCorrect = selectedAnswer === correctAnswer;

                    if (!isCorrect) {
                        hasIncorrectAnswers = true; // Set the flag if there's any incorrect answer
                    }

                    if (isCorrect) {
                        resDiv.innerHTML = `<strong>${questionText}</strong><br>Your answer: ${selectedAnswer}`;
                        resDiv.style.backgroundColor = 'lightgreen'; // Correct answers displayed in light green
                    } else {
                        resDiv.innerHTML = `<strong>${questionText}</strong><br>Your answer: ${selectedAnswer}, Correct answer: ${correctAnswer}`;
                        resDiv.style.backgroundColor = 'lightcoral'; // Incorrect answers displayed in light coral
                    }
                } else {
                    resDiv.innerHTML = `<strong>${questionText}</strong><br>Your answer: ${selectedAnswer}`;
                    resDiv.style.backgroundColor = 'lightcoral'; // Not answered questions displayed in light coral
                }
            } else {
                console.error('Response results are undefined or null.');
            }

            // Additional styling for each result div
            resDiv.style.padding = '10px';
            resDiv.style.marginBottom = '5px';
            resDiv.style.marginLeft = '15px';
            resDiv.style.marginRight = '15px';
            resultBox.style.marginLeft = '15px';
            resultBox.style.marginBottom = '5px';
        

            resultBox.appendChild(resDiv);
        });
        $.ajax({
            type: 'POST',
            url:  "http://127.0.0.1:8000/quizes/update_current_quiz/",  // Replace with the actual URL for updating the current module
            data: { quiz_title: quizName },
            // headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
            console.log('Current quiz updated successfully');
            },
            error: function (error) {
            console.error('Error updating current quiz:', error);
            }
        });

        if (hasIncorrectAnswers) {
            // Add a paragraph about revision
            const revisionParagraph = document.createElement("p");
            revisionParagraph.style.marginLeft = '15px';
            revisionParagraph.textContent = "Now, let's reinforce your learning by revising some questions from the previous topic.";

            // Add a button to start the revision
            const startRevisionButton = document.createElement("button");
            startRevisionButton.type = 'button';
            startRevisionButton.className = 'btn btn-primary mt-3 ml-3';
            startRevisionButton.id = 'start-revision-button';
            startRevisionButton.textContent = 'Start Revision';
            startRevisionButton.addEventListener('click', () => {
                console.log("Revision Button Clicked!")
                generateRevisionQuiz()
                isRevision = true
                quizForm.classList.remove('not-visible');
                resultBox.classList.add('not-visible');
                scoreBox.classList.add('not-visible');
                currentQuestionIndex=0;
            });

            // Append the paragraph and button to the quizBox
            resultBox.appendChild(revisionParagraph);
            resultBox.appendChild(startRevisionButton);
        } else {
            completeRevisionQuiz()
        }
    } else {
        // If the user did not pass, display a message and a "Try Again" button
        resultBox.innerHTML = 'You did not pass. Try again.';
        resultBox.className = 'mt-3 ml-3';
        const tryAgainButton = document.createElement("button");
        tryAgainButton.type = 'button';
        tryAgainButton.className = 'btn btn-primary mt-3 ml-3';
        tryAgainButton.id = 'try-again-button';
        tryAgainButton.textContent = 'Try Again';
        tryAgainButton.addEventListener('click', () => {
            // Reload the quiz or take appropriate action to restart
            window.location.reload();
        });

        // Append the try again button to the resultBox
        resultBox.appendChild(tryAgainButton);
    }
};

// Function to generate and display the Revision Quiz
const generateRevisionQuiz = () => {
    console.log("I am inside of generateRevisionQuiz")
    // Make an AJAX request to get the randomly selected incorrect questions
    $.ajax({
        type: 'GET',
        url: `${url}get_incorrect_questions/`,
        success: function (incorrectQuestions) {
            // Display the Revision Quiz using the retrieved data
            displayRevisionQuiz(incorrectQuestions);
        },
        error: function (error) {
            console.log(error);
        }
    });
};


// Function to display the Revision Quiz
const displayRevisionQuiz = (incorrectQuestions) => {
    quizBox.innerHTML = '';  // Clear existing content
    // Display the current revision question
    const currentQuestionData = incorrectQuestions.data[currentQuestionIndex];
    const questionText = Object.keys(currentQuestionData)[0];
    const questionAnswers = currentQuestionData[questionText];

    quizBox.innerHTML += `
        <div class="question-progress ml-3">
            Revision Question ${currentQuestionIndex + 1} of ${incorrectQuestions.data.length}
        </div>
        <hr>
        <div class="quiz-container">
            <div class="quiz-question">
                <b>${questionText}</b>
            </div>
            <div class="quiz-answers">
                ${generateAnswerButtons(questionAnswers)}
            </div>
        </div>
    `;

    createButtons(incorrectQuestions.data);
};


const completeRevisionQuiz = () => {
     // Congratulations screen
     quizForm.classList.add('not-visible');
     quizBox.classList.add('not-visible');
     endBox.innerHTML= '';
     endBox.innerHTML += `
         <div class="congratulations-screen">
             <h2>Congratulations! You can continue learning about other currencies now!</h2>
             
         </div>
     `;
     endBox.className = 'mt-3 ml-3';
     document.getElementById('congratulations-button').style.display = 'inline-block';
};


// Function to calculate user's score
const calculateScore = () => {
    console.log("No of Questions: ", noQuestions)
    console.log("No of Correct Answers: ", noCorrectAnswers)
    const score = noQuestions > 0 ? (noCorrectAnswers / noQuestions) * 100 : 0;
    return score.toFixed(2);
}