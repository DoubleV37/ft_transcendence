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

async function changeSection(section, content) {
  let	tempDiv = document.createElement('div');
  tempDiv.innerHTML = await fetchSection(section);

  let fetchedContent = await tempDiv.querySelector(content);
  document.querySelector(content).innerHTML = await fetchedContent.innerHTML;
}

window.addEventListener('popstate', async function(event) {
  header_DelEvents();
  if (event.state == null) {
    await changeSection(`${ROUTE.HOME}`, '#content');
    await changeSection(`${ROUTE.HEADER}`, '#Header_content');
    currentUrl = `${ROUTE.HOME}`;
  }
  else {
    await changeSection(event.state.section, '#content');
    await changeSection(`${ROUTE.HEADER}`, '#Header_content'); //add sonme handler event here
    currentUrl = event.state.section;
  }
  header_SetEvents();
});

async function loadPage(url) {
  if (typeof(url) != 'string' || !url || url === currentUrl) {
    return ;
  }
  currentUrl = url;
  history.pushState({section: url}, '', url);
  await changeSection(url, '#content');
}
