async function fetchSection(section) {
  try {
    const response = await fetch(section);

    if (!response.ok) {
      throw new Error('Network response failed with status code:' + response.status);
    }
    const text = await response.text();
    
    return text;
  } catch (error) {
    console.error('ShowSection Error:', error);
  }
}

async function changeSection(section) {
  let	tempDiv = document.createElement('div');
  tempDiv.innerHTML = await fetchSection(section);

  let fetchedContent = tempDiv.querySelector('#content');
  document.querySelector(`#content`).innerHTML = fetchedContent.innerHTML;
}

window.addEventListener('popstate', function(event) {
  if (event.state == null) {
    changeSection('/');
  }
  else {
    changeSection(event.state.section);
  }
});

function loadPage(url) {
  if (typeof(url) != 'string' || !url || url === currentUrl) {
    return ;
  }
  currentUrl = url;
  history.pushState({section: url}, '', url);
  changeSection(url);
}
