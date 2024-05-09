function stats_SetEvents () {
  manageGames();
  manageWins();
  const backArrow = document.getElementById("content").querySelector("#ModalBackArrow");
  console.log("Do i pass here ?");

  backArrow.onclick = async function () {
    let id = window.location.pathname.split("/").reverse();

    if (id[0] === "") {
      id = id[1];
    } else {
      id = id[0];
    }
    // get the id in the jwt cookie
    await changeSection(`${ROUTE.PROFILE}${id}/`, "#ProfileModal");
    await changeSection(`${ROUTE.FRIENDS_PROFILE}${id}/`, "#Friends_Profile");
    profileModal.modal.show();
  };
}

function manageGames () {
  let totalGames = document.getElementById("NbGames").textContent;
  totalGames = parseInt(totalGames, 10);

  const elL = document.getElementById("left-games");
  const elR = document.getElementById("right-games");

  let rGames = document.getElementById("regular-games").textContent;
  let tGames = document.getElementById("tournament-games").textContent;

  rGames = parseInt(rGames, 10);
  tGames = parseInt(tGames, 10);

  function calculateProgressGames (Games, totalGames) {
    if (Games === 0 && totalGames === 0) {
      return 50;
    } else if (Games === 0) {
      return 6;
    }
    return (Games / totalGames) * 100;
  }

  async function updateProgressBarGames (Games, progressBarId) {
    const progressPercentage = calculateProgressGames(Games, totalGames);
    progressBarId.style.setProperty("--final-width", `${progressPercentage}%`);
  }

  updateProgressBarGames(rGames, elL);
  updateProgressBarGames(tGames, elR);
}

function manageWins () {
  let totalWins = document.getElementById("Victories").textContent;
  totalWins = parseInt(totalWins, 10);

  const wL = document.getElementById("left-wins");
  const wR = document.getElementById("right-wins");

  let rWins = document.getElementById("regular-wins").textContent;
  let tWins = document.getElementById("tournament-wins").textContent;

  rWins = parseInt(rWins, 10);
  tWins = parseInt(tWins, 10);

  function calculateProgressWins (Wins, totalWins) {
    if (Wins === 0 && totalWins === 0) {
      return 50;
    } else if (Wins === 0) {
      return 6;
    }
    return (Wins / totalWins) * 100;
  }

  async function updateProgressBarWins (Wins, progressBarId) {
    const progressPercentage = calculateProgressWins(Wins, totalWins);
    progressBarId.style.setProperty("--final-width", `${progressPercentage}%`);
  }

  updateProgressBarWins(rWins, wL);
  updateProgressBarWins(tWins, wR);
}
