async function Access_Denied() {
  error403 = true;
  observer.disconnect();
  del_current_event();
  header_DelEvents();
  document.getElementById('Header_content').innerHTML = '';
  document.getElementById('Footer_content').innerHTML = '';

  document.getElementById('content').innerHTML = `
      <div id=\"overlay\">
	    <div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
		<h3 class="welcome-to-pong">CSRF Cookie missing. Please go on the main page</h1>
	      <button bold; color: white; id=\"ReturnHomePage\"">Please, Return to the Home Page</button>
	</div>
      </div>`;

  let element = document.getElementById('ReturnHomePage');

  element.addEventListener('click', GoToHomePage);
}

async function	GoToHomePage() {
  let element = document.getElementById('ReturnHomePage');

  element.removeEventListener('click', GoToHomePage);

  await changeSection(`${ROUTE.HEADER}`, '#Header_content');
  await changeSection(`${ROUTE.FOOTER}`, '#Footer_content');
  header_SetEvents();
  await loadPage(`${ROUTE.HOME}`);
  home_SetEvents();

  const targetNode = document.querySelector('#content');
  const config = { childList: true, subtree: true };

  observer.observe(targetNode, config);
  error403 = false;
}
