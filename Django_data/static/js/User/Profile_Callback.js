async function  profile_SettingsCallBack() {
  try {
    await loadPage(`${ROUTE.SETTINGS}`);
    profileModal['modal'].hide();
  }
  catch (err) {
    console.log(`Error - profile_S: ${err}`);
  }
}

function  profile_closeModal() {
  profileModal['modal'].hide();
}

async function  profile_SkinsCallBack() {
  console.log("Skins: Do nothing for now");
}

async function  profile_HistoryCallBack() {
  console.log("History: Do nothing for now");
}

async function  profile_StatsCallBack() {
  console.log("Stats: Do nothing for now");
}

async function  profile_42AccCallBack() {
  console.log("42Acc: Do nothing for now");
}
