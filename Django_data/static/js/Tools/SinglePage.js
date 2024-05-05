async function fetchSection (section, request = null) {
  let response;

  if (!request) {
    request = {
      method: "GET",
      headers: { load: false }
    };
    response = await fetch(section, request);
  } else {
    response = await fetch(section, request);
  }

  if (!response.ok) {
    const _status = response.status;
    if (_status === 498) {
      throw new Error(_status + ":" + (await response.text()));
    }
  }
  return response;
}

async function changeSection (section, content, otherContent = content) {
  const tempDiv = document.createElement("div");
  const response = await MakeRequest(section);
  tempDiv.innerHTML = await response.text();

  const fetchedContent = await tempDiv.querySelector(otherContent);
  document.querySelector(content).innerHTML = await fetchedContent.innerHTML;
}

window.addEventListener("popstate", async function (event) {
  if (error403 == true) {
    return;
  }
  del_current_event();
  const elem = document.getElementById("titleContent").getAttribute("data-content");
  if (elem === "GAME_LOCAL" || elem === "GAME_MATCH"
    || elem === "GAME_ROOM" || elem === "TOURNAMENT") {
    const targetNode = document.querySelector("#content");
    const config = { childList: true, subtree: true };

    observer.observe(targetNode, config);
  }
  header_DelEvents();
  await del_modal();
  if (event.state == null) {
    await changeSection(`${ROUTE.HOME}`, "#content");
    currentUrl = `${ROUTE.HOME}`;
  } else {
    await changeSection(event.state.section, "#content");
    currentUrl = event.state.section;
  }
  await changeSection(`${ROUTE.HEADER}`, "#Header_content");
  header_SetEvents();
});

async function loadPage (url) {
  if (url !== currentUrl) {
    currentUrl = url;
    history.pushState({ section: url }, "", url);
  }
  del_current_event();
  const elem = document.getElementById("titleContent").getAttribute("data-content");
  if (elem === "GAME_LOCAL" || elem === "GAME_MATCH"
    || elem === "GAME_ROOM" || elem === "TOURNAMENT") {
    const targetNode = document.querySelector("#content");
    const config = { childList: true, subtree: true };

    observer.observe(targetNode, config);
  }
  await changeSection(url, "#content");
}

async function MakeRequest (url, request = null) {
  try {
    const response = await fetchSection(url, request);

    if (response.status === 403) {
      Access_Denied();
    }
    return response;
  } catch (err) {
    return await authError(err.message, url, request);
  }
}

async function authError (message, url, request) {
  const _words = message.split(":");

  if (_words[0] === "498" && _words[1] === "Expired") {
    await fetchSection(`${ROUTE.JWTREFRESH}`);
    return await MakeRequest(url, request);
  } else {
    del_current_event();
    header_DelEvents();
    await changeSection(`${ROUTE.HEADER}`, "#Header_content");
    header_SetEvents();
    await loadPage(`${ROUTE.SIGNIN}`);
    throw new Error(`AUTH - ${_words[1]}`);
  }
}

async function del_modal () {
  if (avatarModal.active === true) {
    avatarModal.modal.hide();
  }
  if (TwofaModal.active === true) {
    const form = document.getElementById("TWOFA_Form");
    const formData = new FormData(form);
    await MakeRequest(`${ROUTE.TWOFA_E}`, {
      method: "POST",
      body: formData
    });
    TwofaModal.modal.hide();
  }
  if (TwofaCodeModal.active === true) {
    TwofaCodeModal.modal.hide();
  }
  if (profileModal.active === true) {
    profileModal.modal.hide();
  }
  if (friendsModal.active === true) {
    friendsModal.modal.hide();
  }
}
