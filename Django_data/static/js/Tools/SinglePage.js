async function showSection(section) {
  try {
    const response = await fetch(`${section}`);

    if (!response.ok) {
      throw new Error('Network response failed');
    }
    const text = await response.text();

    let	  tempDiv = document.createElement('div');
    tempDiv.innerHTML = text;

    let fetchedContent = tempDiv.querySelector('#content');
    document.querySelector(`#content`).innerHTML = fetchedContent.innerHTML;

  } catch (error) {
    console.error('ShowSection Error:', error);
  }
}

function clickButton(button) {
	showSection(button.dataset.section);
	history.pushState({section: button.dataset.section}, '');
}

window.onpopstate = function(event) {
	if (event.state == null) {
		showSection('')
		return
	}
	showSection(event.state.section)
}
