function stats_SetEvents () {
    let totalGames = document.getElementById('NbGames').textContent;
    totalGames = parseInt(totalGames, 10);

	  const elL = document.getElementById("left-games");
    const elR = document.getElementById("right-games");
    
    let rGames = document.getElementById('regular-games').textContent;
    let tGames = document.getElementById('tournament-games').textContent;

    // Conversion des scores en nombres si nécessaire
    rGames = parseInt(rGames, 10);
    tGames = parseInt(tGames, 10);

    let totalWins = document.getElementById('Victories').textContent;
    totalWins = parseInt(totalWins, 10);

    const wL = document.getElementById("left-wins");
    const wR = document.getElementById("right-wins");
    
    let rWins = document.getElementById('regular-wins').textContent;
    let tWins = document.getElementById('tournament-wins').textContent;

    // Conversion des scores en nombres si nécessaire
    rWins = parseInt(rWins, 10);
    tWins = parseInt(tWins, 10);
        
      // Calculer le pourcentage de progression pour chaque joueur
    function calculateProgressGames(tGames, totalGames) {
      // Si le score est 0, retourner 1% pour indiquer une petite progression
      if (tGames === 0 && rGames != 0) {
          return 5;
      }
      else if (tGames != 0 && rGames === 0) {
          return 5;
      }
      else if (tGames === 0 && rGames === 0) {
          return 50;
      }
      // Sinon, calculer le pourcentage normal
      return (tGames / totalGames) * 100;
    }

    // Mettre à jour la barre de progression pour chaque joueur
    async function updateProgressBarGames(tGames, progressBarId) {
      let progressPercentage = calculateProgressGames(tGames, totalGames);
      progressBarId.style.width = `${progressPercentage}%`;
    }

    // Mettre à jour les barres de progression
    updateProgressBarGames(rGames, elL);
    updateProgressBarGames(tGames, elR);
        
      // Calculer le pourcentage de progression pour chaque joueur
    function calculateProgressWins(tWins, totalWins) {
      // Si le score est 0, retourner 1% pour indiquer une petite progression
      if (tWins === 0 && rWins != 0) {
          return 5;
      }
      else if (tWins != 0 && rWins === 0) {
          return 5;
      }
      else if (tWins === 0 && rWins === 0) {
          return 50;
      }
      // Sinon, calculer le pourcentage normal
      return (tWins / totalWins) * 100;
    }

    // Mettre à jour la barre de progression pour chaque joueur
    async function updateProgressBarWins(tWins, progressBarId) {
      let progressPercentage = calculateProgressWins(tWins, totalWins);
      progressBarId.style.width = `${progressPercentage}%`;
    }

    // Mettre à jour les barres de progression
    updateProgressBarWins(rWins, wL);
    updateProgressBarWins(tWins, wR);
}