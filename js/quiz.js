// Quiz interactivo para preguntas de certificación GCP Professional Data Engineer

class Quiz {
    constructor(containerId, questions) {
        this.container = document.getElementById(containerId);
        this.questions = questions;
        this.currentQuestion = 0;
        this.score = 0;
        this.answered = false;
        this.init();
    }

    init() {
        if (!this.container) {
            console.error('Contenedor de quiz no encontrado');
            return;
        }
        this.renderQuestion();
    }

    renderQuestion() {
        const question = this.questions[this.currentQuestion];
        
        let optionsHTML = '';
        question.options.forEach((option, index) => {
            optionsHTML += `
                <div class="quiz-option" data-index="${index}">
                    <input type="radio" 
                           id="option${index}" 
                           name="quiz-option" 
                           value="${index}"
                           ${this.answered ? 'disabled' : ''}>
                    <label for="option${index}">${option}</label>
                </div>
            `;
        });

        this.container.innerHTML = `
            <div class="quiz-card">
                <div class="quiz-header">
                    <h3>Pregunta ${this.currentQuestion + 1} de ${this.questions.length}</h3>
                    <div class="quiz-progress">
                        <div class="quiz-progress-bar" style="width: ${((this.currentQuestion + 1) / this.questions.length) * 100}%"></div>
                    </div>
                </div>
                
                <div class="quiz-question">
                    <p>${question.question}</p>
                </div>
                
                <div class="quiz-options">
                    ${optionsHTML}
                </div>
                
                <div class="quiz-feedback" id="quiz-feedback"></div>
                
                <div class="quiz-actions">
                    <button class="quiz-btn quiz-btn-submit" id="submitAnswer" ${this.answered ? 'disabled' : ''}>
                        Verificar Respuesta
                    </button>
                    ${this.currentQuestion < this.questions.length - 1 ? 
                        `<button class="quiz-btn quiz-btn-next" id="nextQuestion" style="display: none;">
                            Siguiente Pregunta →
                        </button>` : 
                        `<button class="quiz-btn quiz-btn-next" id="finishQuiz" style="display: none;">
                            Ver Resultados
                        </button>`
                    }
                </div>
                
                ${this.currentQuestion > 0 ? 
                    `<div class="quiz-score">
                        Puntuación actual: ${this.score} de ${this.currentQuestion}
                    </div>` : ''
                }
            </div>
        `;

        this.attachEventListeners();
    }

    attachEventListeners() {
        const submitBtn = document.getElementById('submitAnswer');
        const nextBtn = document.getElementById('nextQuestion');
        const finishBtn = document.getElementById('finishQuiz');
        const options = document.querySelectorAll('.quiz-option');

        // Seleccionar opción
        options.forEach(option => {
            option.addEventListener('click', () => {
                if (!this.answered) {
                    const radio = option.querySelector('input[type="radio"]');
                    radio.checked = true;
                    
                    // Remover clase selected de todas las opciones
                    options.forEach(opt => opt.classList.remove('selected'));
                    // Agregar clase selected a la opción clickeada
                    option.classList.add('selected');
                }
            });
        });

        // Verificar respuesta
        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                this.checkAnswer();
            });
        }

        // Siguiente pregunta
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.nextQuestion();
            });
        }

        // Finalizar quiz
        if (finishBtn) {
            finishBtn.addEventListener('click', () => {
                this.showResults();
            });
        }
    }

    checkAnswer() {
        const selectedOption = document.querySelector('input[name="quiz-option"]:checked');
        
        if (!selectedOption) {
            alert('Por favor selecciona una respuesta');
            return;
        }

        this.answered = true;
        const selectedIndex = parseInt(selectedOption.value);
        const question = this.questions[this.currentQuestion];
        const isCorrect = selectedIndex === question.correct;

        if (isCorrect) {
            this.score++;
        }

        // Mostrar feedback
        const feedbackDiv = document.getElementById('quiz-feedback');
        feedbackDiv.innerHTML = `
            <div class="feedback ${isCorrect ? 'correct' : 'incorrect'}">
                <div class="feedback-header">
                    <span class="feedback-icon">${isCorrect ? '✅' : '❌'}</span>
                    <strong>${isCorrect ? '¡Correcto!' : 'Incorrecto'}</strong>
                </div>
                <p class="feedback-explanation">${question.explanation}</p>
                ${!isCorrect ? `<p class="feedback-correct-answer"><strong>Respuesta correcta:</strong> ${question.options[question.correct]}</p>` : ''}
            </div>
        `;
        feedbackDiv.style.display = 'block';

        // Deshabilitar todas las opciones y marcar la correcta
        const options = document.querySelectorAll('.quiz-option');
        options.forEach((option, index) => {
            const radio = option.querySelector('input[type="radio"]');
            radio.disabled = true;
            
            if (index === question.correct) {
                option.classList.add('correct');
            } else if (index === selectedIndex && !isCorrect) {
                option.classList.add('incorrect');
            }
        });

        // Mostrar botón siguiente/finalizar
        document.getElementById('submitAnswer').style.display = 'none';
        const nextBtn = this.currentQuestion < this.questions.length - 1 ? 
            document.getElementById('nextQuestion') : 
            document.getElementById('finishQuiz');
        if (nextBtn) {
            nextBtn.style.display = 'inline-block';
        }
    }

    nextQuestion() {
        this.answered = false;
        this.currentQuestion++;
        this.renderQuestion();
    }

    showResults() {
        const percentage = Math.round((this.score / this.questions.length) * 100);
        let message = '';
        let resultClass = '';

        if (percentage >= 80) {
            message = '¡Excelente! Estás muy preparado para la certificación.';
            resultClass = 'excellent';
        } else if (percentage >= 60) {
            message = 'Buen trabajo. Revisa los temas donde fallaste.';
            resultClass = 'good';
        } else {
            message = 'Necesitas más práctica. Revisa la documentación oficial.';
            resultClass = 'needs-improvement';
        }

        this.container.innerHTML = `
            <div class="quiz-card quiz-results ${resultClass}">
                <div class="quiz-results-header">
                    <h2>Resultados del Quiz</h2>
                </div>
                
                <div class="quiz-results-score">
                    <div class="score-circle">
                        <svg viewBox="0 0 200 200">
                            <circle cx="100" cy="100" r="90" fill="none" stroke="#e0e0e0" stroke-width="20"/>
                            <circle cx="100" cy="100" r="90" fill="none" stroke="currentColor" stroke-width="20"
                                    stroke-dasharray="${2 * Math.PI * 90}"
                                    stroke-dashoffset="${2 * Math.PI * 90 * (1 - percentage / 100)}"
                                    transform="rotate(-90 100 100)"/>
                        </svg>
                        <div class="score-text">
                            <span class="score-percentage">${percentage}%</span>
                            <span class="score-fraction">${this.score}/${this.questions.length}</span>
                        </div>
                    </div>
                </div>
                
                <div class="quiz-results-message">
                    <p>${message}</p>
                </div>
                
                <div class="quiz-actions">
                    <button class="quiz-btn quiz-btn-primary" onclick="location.reload()">
                        🔄 Reintentar Quiz
                    </button>
                    <button class="quiz-btn quiz-btn-secondary" onclick="window.location.href='index.html'">
                        🏠 Volver al Inicio
                    </button>
                </div>
            </div>
        `;
    }
}

// Exportar para uso global
window.Quiz = Quiz;
