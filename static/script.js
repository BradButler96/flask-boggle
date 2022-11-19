let score = 0;
let prevGuesses = [];

$('#submit-btn').click(async function(event) {
    // Gets users' guess 
    // Verifies guess is eligible
    // Updates and displays the response msg to user
    // Clears guess input
    event.preventDefault()
    guess = $('#guess-form-input').val()
    let res = await axios.get('/word_list', {params: {word: guess}})
    displayMsg(res.data.result, guess)
    $('#guess-form-input').val('')
})

function displayMsg(msg, guess) {
    // Determines what msg to display
    // Updates msg text
    if (msg == 'ok') {
        if (prevGuesses.includes(guess) == false) {
            prevGuesses.push(guess)
            updateScore(guess)
            $('#msg').removeClass()
            $('#msg').addClass('correct')
            $('#msg').text(`${guess} is correct!`)
        } else {
            $('#msg').removeClass()
            $('#msg').addClass('guessed')
            $('#msg').text(`You've already guessed ${guess}`)
        }
    } else if (msg == 'not-on-board') {
        $('#msg').removeClass()
        $('#msg').addClass('invalid')
        $('#msg').text(`${guess} is not on the board!`)

    } else {
        $('#msg').removeClass()
        $('#msg').addClass('invalid')
        $('#msg').text(`${guess} is not a word!`)
    }
}

function updateScore(guess) {
    // Updates user score
    let points = guess.length
    score += points
    $('#score').text(score)
}

async function saveScore() {
    // Sends user score to the server
    await axios.post('/score', {score: score})
}

function timer() {
    // Updates remaining time for game
    // Disables submit button when time is up
    // Sends user score to server
    let timeRemaining = parseFloat($('#timer').text())
    let timer = setInterval(() => {
        if (timeRemaining >= 0.1){
            timeRemaining = timeRemaining - 0.1
            $('#timer').text((timeRemaining).toFixed(1))
        } else {
            $('#timer').text('0.0')
            $('#submit-btn').prop('disabled', true)
            saveScore();
            clearInterval(timer)
        }
    }, 100)}

timer()

