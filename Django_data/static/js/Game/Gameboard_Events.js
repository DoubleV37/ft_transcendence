function gameboard_SetEvents () {
  gameboard_Callbacks();
  const backArrow = document.getElementById("content").querySelector("#ModalBackArrow");

  backArrow.onclick = async function () {
    let id = window.location.pathname.split("/").reverse();

    const userid = document.getElementById("HEADER_IsAuth").getAttribute("data-id");

    await changeSection(`${ROUTE.PROFILE}${id[1]}/`, "#ProfileModal");
    if (parseInt(userid) !== parseInt(id[1])) {
      await changeSection(`${ROUTE.FRIENDS_PROFILE}${id[1]}/`, "#Friends_Profile");
    }
    profileModal.modal.show();
  };
}

function gameboard_Callbacks () {
  const elL = document.getElementById("left");
  const elR = document.getElementById("right");

  let scoreL = document.getElementById("score-left").textContent;
  let scoreR = document.getElementById("score-right").textContent;

  scoreL = parseInt(scoreL, 10);
  scoreR = parseInt(scoreR, 10);

  let totalRounds = document.getElementById("NbRounds").textContent;
  totalRounds = parseInt(totalRounds, 10);

  function calculateProgress (score, totalRounds) {
    if (score === 0 && totalRounds === 0) {
      return 50;
    } else if (score === 0) {
      return 6;
    }
    return (score / totalRounds) * 100;
  }

  function updateProgressBar (score, progressBarId) {
    const progressPercentage = calculateProgress(score, totalRounds);
    progressBarId.style.setProperty("--final-width", `${progressPercentage}%`);
  }

  updateProgressBar(scoreL, elL);
  updateProgressBar(scoreR, elR);
}
