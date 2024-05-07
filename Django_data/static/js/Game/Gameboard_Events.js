function gameboard_SetEvents () {
    gameboard_Callbacks();
}

function gameboard_Callbacks () {

    const elL = document.getElementById("left");
    const elR = document.getElementById("right");
    
    let scoreL = document.getElementById('score-left').textContent;
    let scoreR = document.getElementById('score-right').textContent;

    // Conversion des scores en nombres si nécessaire
    scoreL = parseInt(scoreL, 10);
    scoreR = parseInt(scoreR, 10);

    let totalRounds = document.getElementById('NbRounds').textContent;
    totalRounds = parseInt(totalRounds, 10);
        
      // Calculer le pourcentage de progression pour chaque joueur
    function calculateProgress(score, totalRounds) {
      // Si le score est 0, retourner 1% pour indiquer une petite progression
      if (score === 0 && totalRounds === 0) {
        return 50;
      }
      else if (score === 0) {
          return 6;
      }
      // Sinon, calculer le pourcentage normal
      return (score / totalRounds) * 100;
    }

    // Mettre à jour la barre de progression pour chaque joueur
    function updateProgressBar(score, progressBarId) {
      let progressPercentage = calculateProgress(score, totalRounds);
      progressBarId.style.setProperty('--final-width', `${progressPercentage}%`);
    }

    // Mettre à jour les barres de progression
    updateProgressBar(scoreL, elL);
    updateProgressBar(scoreR, elR);
}