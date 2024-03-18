async function Access_Denied() {
  //document.head.innerHTML = '';
  document.body.innerHTML = `
    <div id=\"content\">
      <div id=\"overlay\">
	    <div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
		<h3 class="welcome-to-pong">CSRF Cookie missing. Please go on the main page</h1>
	      <button bold; color: white; onclick="window.location.href='/'">Please, Return to the Home Page</button>
	</div>
      </div>
    </div>`
}
