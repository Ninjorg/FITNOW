function loadExercises() {
    const target = document.getElementById('targetSelect').value;
    
    fetch(`/exercises?target=${target}`)
        .then(response => response.json())
        .then(exercises => {
            const exerciseContainer = document.getElementById('exerciseContainer');
            exerciseContainer.innerHTML = ''; 

            exercises.forEach(exercise => {
                const gif = exercise.gifUrl;
                const name = exercise.name;
                const instructions = exercise.instructions;
                const equipment = exercise.equipment;

                const card = document.createElement('div');
                card.className = 'card';

                card.innerHTML = `
                    <h2>${name}</h2>
                    <img src="${gif}" alt="${name}">
                    <p><strong>Equipment:</strong> ${equipment}</p>
                    <p><strong>Instructions:</strong> ${instructions}</p>
                `;

                exerciseContainer.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Error loading exercises:', error);
        });
}
