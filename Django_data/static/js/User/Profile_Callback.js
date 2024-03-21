async function  profile_SettingsCallBack() {
  try {
    await loadPage(`${ROUTE.SETTINGS}`);
    profileModal.hide();
  }
  catch (err) {
    console.log(`Error - profile_S: ${err}`);
  }
}

function  profile_closeModal() {
  profileModal.hide();
}

async function  profile_SkinsCallBack() {
//  profileModal.hide();
//  await loadPage(`${ROUTE.}`);
  console.log("Skins: Do nothing for now");
}

async function  profile_HistoryCallBack() {
//  profileModal.hide();
//  await loadPage(`${ROUTE.}`);
  console.log("History: Do nothing for now");
}

async function  profile_StatsCallBack() {
//  profileModal.hide();
//  await loadPage(`${ROUTE.}`);
  console.log("Stats: Do nothing for now");
}

async function  profile_42AccCallBack() {
//  profileModal.hide();
//  await loadPage(`${ROUTE.}`);
  console.log("42Acc: Do nothing for now");
}
