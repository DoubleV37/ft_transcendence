async function showSection(section) {
  try {
    const response = await fetch(section);

    if (!response.ok) {
      throw new Error('Network response failed with status code:' + response.status);
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

window.addEventListener('popstate', function(event) {
  if (event.state == null) {
    showSection('/');
  }
  else {
    showSection(event.state.section);
  }
});

function loadPage(url) {
  if (typeof(url) != 'string' || !url || url === currentUrl) {
    return ;
  }
  currentUrl = url;
  history.pushState({section: url}, '', url);
  showSection(url);
}
