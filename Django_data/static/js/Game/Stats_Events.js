function stats_SetEvents () {

    manageGames();
    manageWins();
}

function manageGames() {
  let totalGames = document.getElementById('NbGames').textContent;
  totalGames = parseInt(totalGames, 10);

  const elL = document.getElementById("left-games");
  const elR = document.getElementById("right-games");

  let rGames = document.getElementById('regular-games').textContent;
  let tGames = document.getElementById('tournament-games').textContent;

  // Conversion des scores en nombres si nécessaire
  rGames = parseInt(rGames, 10);
  tGames = parseInt(tGames, 10);

  // Calculer le pourcentage de progression pour chaque joueur
  function calculateProgressGames(Games, totalGames) {
      if (Games === 0 && totalGames === 0) {
        return 50;
      }
      else if (Games === 0) {
          return 6;
      }
      // Sinon, calculer le pourcentage normal
      return (Games / totalGames) * 100;
  }

  // Mettre à jour la barre de progression pour chaque joueur
  async function updateProgressBarGames(Games, progressBarId) {
    let progressPercentage = calculateProgressGames(Games, totalGames);
    progressBarId.style.setProperty('--final-width', `${progressPercentage}%`);
  }

  // Mettre à jour les barres de progression
  updateProgressBarGames(rGames, elL);
  updateProgressBarGames(tGames, elR);
}

function manageWins() {
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
  function calculateProgressWins(Wins, totalWins) {
      if (Wins === 0 && totalWins === 0) {
        return 50;
      }
      else if (Wins === 0) {
          return 6;
      }
      // Sinon, calculer le pourcentage normal
      return (Wins / totalWins) * 100;
  }

  // Mettre à jour la barre de progression pour chaque joueur
  async function updateProgressBarWins(Wins, progressBarId) {
    let progressPercentage = calculateProgressWins(Wins, totalWins);
    progressBarId.style.setProperty('--final-width', `${progressPercentage}%`);
  }

  // Mettre à jour les barres de progression
  updateProgressBarWins(rWins, wL);
  updateProgressBarWins(tWins, wR);
}