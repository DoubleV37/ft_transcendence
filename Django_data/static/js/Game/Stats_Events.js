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

  rGames = parseInt(rGames, 10);
  tGames = parseInt(tGames, 10);

  function calculateProgressGames(Games, totalGames) {
      if (Games === 0 && totalGames === 0) {
        return 50;
      }
      else if (Games === 0) {
          return 6;
      }
      return (Games / totalGames) * 100;
  }

  async function updateProgressBarGames(Games, progressBarId) {
    let progressPercentage = calculateProgressGames(Games, totalGames);
    progressBarId.style.setProperty('--final-width', `${progressPercentage}%`);
  }

  updateProgressBarGames(rGames, elL);
  updateProgressBarGames(tGames, elR);
}

function manageWins() {
  let totalWins = document.getElementById('Victories').textContent;
  totalWins = parseInt(totalWins, 10);

  const wL = document.getElementById("left-wins");
  const wR = document.getElementById("right-wins");

  let aiWins = document.getElementById('victory_ia').textContent;
  let playerWins = document.getElementById('victory_player').textContent;

  aiWins = parseInt(aiWins, 10);
  playerWins = parseInt(playerWins, 10);

  function calculateProgressWins(Wins, totalWins) {
      if (Wins === 0 && totalWins === 0) {
        return 50;
      }
      else if (Wins === 0) {
          return 6;
      }
      return (Wins / totalWins) * 100;
  }

  async function updateProgressBarWins(Wins, progressBarId) {
    let progressPercentage = calculateProgressWins(Wins, totalWins);
    progressBarId.style.setProperty('--final-width', `${progressPercentage}%`);
  }

  updateProgressBarWins(aiWins, wL);
  updateProgressBarWins(playerWins, wR);
}
