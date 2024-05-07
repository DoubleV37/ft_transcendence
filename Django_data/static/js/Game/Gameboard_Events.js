function gameboard_SetEvents () {
    gameboard_Callbacks();
}

function gameboard_Callbacks () {

    const elL = document.getElementById("left");
    const elR = document.getElementById("right");
    
    let scoreL = document.getElementById('score-left').textContent;
    let scoreR = document.getElementById('score-right').textContent;

    scoreL = parseInt(scoreL, 10);
    scoreR = parseInt(scoreR, 10);

    let totalRounds = document.getElementById('NbRounds').textContent;
    totalRounds = parseInt(totalRounds, 10);
        
    function calculateProgress(score, totalRounds) {
      if (score === 0 && totalRounds === 0) {
        return 50;
      }
      else if (score === 0) {
          return 6;
      }
      return (score / totalRounds) * 100;
    }

    function updateProgressBar(score, progressBarId) {
      let progressPercentage = calculateProgress(score, totalRounds);
      progressBarId.style.setProperty('--final-width', `${progressPercentage}%`);
    }

    updateProgressBar(scoreL, elL);
    updateProgressBar(scoreR, elR);
}