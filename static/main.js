document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('feedback-form');
    const feedbackContainer = document.getElementById('feedback-container');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        const writingQuestion = document.getElementById('writing-question').value;
        const userWriting = document.getElementById('user-writing').value;

        // make api call to backend
        const response = await fetch('/api/generate_feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                writingQuestion: writingQuestion,
                userWriting: userWriting
            })
        });

        const responseData = await response.json();

        // Display the feedback 
        const feedbackElement = document.createElement('div');
        feedbackElement.innerHTML = `<h2>Feedback:</h2><p>${responseData.feedback}</p>`;
        feedbackContainer.appendChild(feedbackElement);

        // // Clear the input fields
        // document.getElementById('writing-question').value = '';
        // document.getElementById('user-writing').value = '';
    });
});
